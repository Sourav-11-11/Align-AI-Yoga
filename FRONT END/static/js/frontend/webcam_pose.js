(function () {
  const cfg = window.LIVE_POSE_CONFIG;
  if (!cfg) return;

  const poseSelect = document.getElementById(cfg.poseSelectId);
  const panel = document.getElementById(cfg.panelId);
  const startBtn = document.getElementById(cfg.startBtnId);
  const stopBtn = document.getElementById(cfg.stopBtnId);
  const video = document.getElementById(cfg.videoId);
  const canvas = document.getElementById(cfg.canvasId);
  const statusEl = document.getElementById(cfg.statusId);
  const scoreEl = document.getElementById(cfg.scoreId);
  const correctionsEl = document.getElementById(cfg.correctionsId);
  const tipsEl = document.getElementById(cfg.tipsId);
  const savedResultEl = document.getElementById("liveSavedResult");
  const savedSnapshotImgEl = document.getElementById("savedSnapshotImg");
  const savedSnapshotScoreEl = document.getElementById("savedSnapshotScore");
  const savedSnapshotPoseEl = document.getElementById("savedSnapshotPose");
  const savedSnapshotTimeEl = document.getElementById("savedSnapshotTime");
  const savedCorrectionsEl = document.getElementById("savedCorrections");
  const savedTipsEl = document.getElementById("savedTips");

  if (!poseSelect || !panel || !startBtn || !video || !canvas) {
    console.error("Webcam analysis: Missing required elements", {
      poseSelect: !!poseSelect,
      panel: !!panel,
      startBtn: !!startBtn,
      video: !!video,
      canvas: !!canvas
    });
    return;
  }

  const ctx = canvas.getContext("2d");
  let mediaStream = null;
  let pose = null;
  let running = false;
  let lastProcessTs = 0;
  let referenceCache = {};
  let currentReference = null;
  let currentTolerance = 5;
  // Evaluation config fetched from server
  let severityThresholds = null;
  let scoringWeights = null;
  let bestEvaluation = null;
  let bestAngles = null;
  let lastEvaluation = null;
  let stillPoseFrames = 0;
  let autoFinalized = false;

  const PROCESS_EVERY_MS = 150;
  const AUTO_FINALIZE_STILL_FRAMES = 10;

  // Snapshot tracking
  let highestScore = 0;
  let lastFrameAngles = null;
  let stillCounter = 0;
  let snapBtn = document.getElementById('snapBtn');
  const snapThreshold = 3; // Frames to consider still

  function setStatus(text) {
    if (statusEl) statusEl.textContent = text;
  }

  function setList(el, items) {
    if (!el) return;
    el.innerHTML = "";
    items.forEach((item) => {
      const li = document.createElement("li");
      li.textContent = item;
      el.appendChild(li);
    });
  }

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function calculateAngle(a, b, c) {
    const ba = [a.x - b.x, a.y - b.y];
    const bc = [c.x - b.x, c.y - b.y];

    const magBA = Math.hypot(ba[0], ba[1]);
    const magBC = Math.hypot(bc[0], bc[1]);
    if (magBA < 1e-6 || magBC < 1e-6) return null;

    const dot = ba[0] * bc[0] + ba[1] * bc[1];
    const cosine = clamp(dot / (magBA * magBC), -1, 1);
    const deg = (Math.acos(cosine) * 180) / Math.PI;
    return clamp(deg, 0, 180);
  }

  function calculateAngles(landmarks) {
    if (!window.PoseOverlay) {
      console.error("PoseOverlay not available");
      return {
        "Shoulder Angle": null,
        "Elbow Angle": null,
        "Hip Angle": null,
        "Knee Angle": null,
      };
    }

    const sideInfo = window.PoseOverlay.pickBestSide(landmarks);
    const m = sideInfo.map;

    const shoulder = landmarks[m.shoulder];
    const elbow = landmarks[m.elbow];
    const wrist = landmarks[m.wrist];
    const hip = landmarks[m.hip];
    const knee = landmarks[m.knee];
    const ankle = landmarks[m.ankle];

    const visThreshold = 0.3;
    const good = (...lms) => lms.every((lm) => lm && (lm.visibility || 0) >= visThreshold);

    return {
      "Shoulder Angle": good(elbow, shoulder, hip) ? calculateAngle(elbow, shoulder, hip) : null,
      "Elbow Angle": good(wrist, elbow, shoulder) ? calculateAngle(wrist, elbow, shoulder) : null,
      "Hip Angle": good(shoulder, hip, knee) ? calculateAngle(shoulder, hip, knee) : null,
      "Knee Angle": good(hip, knee, ankle) ? calculateAngle(hip, knee, ankle) : null,
    };
  }

  function severity(absDiff) {
    // Use server-side severity thresholds if available; fallback to defaults
    if (!severityThresholds) {
      // Fallback to backend values
      if (absDiff <= 5) return "perfect";
      if (absDiff <= 10) return "minor";
      if (absDiff <= 20) return "moderate";
      return "major";
    }

    if (absDiff <= severityThresholds.perfect) return "perfect";
    if (absDiff <= severityThresholds.minor) return "minor";
    if (absDiff <= severityThresholds.moderate) return "moderate";
    return "major";
  }

  function scoreFromSeverity(level) {
    // Use server-side scoring weights if available; fallback to defaults
    if (!scoringWeights) {
      // Fallback to backend values
      if (level === "perfect") return 100;
      if (level === "minor") return 85;
      if (level === "moderate") return 65;
      if (level === "major") return 35;
      if (level === "missing") return 0;
      return 0;
    }

    return scoringWeights[level] || 0;
  }

  function evaluatePose(angles, reference) {
    const result = {
      score: 0,
      severities: {},
      corrections: [],
      tips: [],
    };

    const scores = [];

    const phrase = {
      "Shoulder Angle": {
        increase: "Lift and open your chest slightly.",
        decrease: "Relax your shoulders down a little.",
      },
      "Elbow Angle": {
        increase: "Straighten your elbow slightly.",
        decrease: "Soften your elbow bend a little.",
      },
      "Hip Angle": {
        increase: "Lengthen through your hips and spine.",
        decrease: "HscoreFromSeverity("missing")ge a little deeper from your hips.",
      },
      "Knee Angle": {
        increase: "Straighten your knee slightly.",
        decrease: "Bend your knee a little more.",
      },
    };

    Object.keys(reference).forEach((joint) => {
      const target = reference[joint];
      const measured = angles[joint];

      if (typeof measured !== "number") {
        result.severities[joint] = "missing";
        result.corrections.push(`${joint}: landmark not clear. Reposition your body in frame.`);
        scores.push(60);
        return;
      }

      const diff = measured - target;
      const absDiff = Math.abs(diff);
      const level = severity(absDiff);
      result.severities[joint] = level;
      scores.push(scoreFromSeverity(level));

      if (level !== "perfect") {
        const direction = diff > 0 ? "decrease" : "increase";
        const base = phrase[joint] ? phrase[joint][direction] : "Adjust this joint slightly.";
        result.corrections.push(`${joint}: ${base} (Now ${measured.toFixed(1)}\u00b0, target ${target}\u00b0).`);
      }
    });

    result.score = scores.length ? Math.round(scores.reduce((a, b) => a + b, 0) / scores.length) : 0;

    if (result.score < 60) {
      result.tips = [
        "Engage your core for better stability.",
        "Move slower and hold the pose for 2-3 breaths.",
      ];
    } else if (result.score < 85) {
      result.tips = [
        "Keep your shoulders relaxed and neck neutral.",
        "Use steady breathing to maintain alignment.",
      ];
    } else {
      result.tips = [
        "Great alignment. Maintain this form consistently.",
        "Increase hold time gradually for better endurance.",
      ];
    }

    if (!result.corrections.length) {
      result.corrections = ["Great work. Your current alignment looks good."];
    }

    return result;
  }

  async function getReferenceForPose(poseName) {
    const key = (poseName || "").trim().toLowerCase();
    if (!key) {
      throw new Error("Please select a pose first.");
    }

    if (referenceCache[key]) {
      const cached = referenceCache[key];
      // Apply cached config values
      severityThresholds = cached.severity_thresholds;
      scoringWeights = cached.scoring_weights;
      return {
        reference: cached.reference_angles,
        tolerance: cached.angle_tolerance,
      };
    }

    const url = `${cfg.referenceApiUrl}?pose=${encodeURIComponent(key)}`;
    const res = await fetch(url, { headers: { Accept: "application/json" } });
    if (!res.ok) {
      throw new Error("Could not load reference angles for this pose.");
    }

    const payload = await res.json();
    
    // Extract evaluation config from API response
    severityThresholds = payload.severity_thresholds || null;
    scoringWeights = payload.scoring_weights || null;

    const parsed = {
      reference_angles: payload.reference_angles || {},
      angle_tolerance: typeof payload.angle_tolerance === "number" ? payload.angle_tolerance : 5,
      severity_thresholds: severityThresholds,
      scoring_weights: scoringWeights,
    };
    
    referenceCache[key] = parsed;
    
    return {
      reference: parsed.reference_angles,
      tolerance: parsed.angle_tolerance,
    };
  }

  function isStill(angles) {
    if (!lastFrameAngles) return false;
    
    let totalDiff = 0;
    Object.keys(angles).forEach((joint) => {
      const curr = angles[joint];
      const last = lastFrameAngles[joint];
      if (typeof curr === "number" && typeof last === "number") {
        totalDiff += Math.abs(curr - last);
      }
    });
    
    const averageDiff = totalDiff / Object.keys(angles).length;
    return averageDiff < 2; // Less than 2 degree change
  }

  function captureSnapshot(score, poseName, angles, severities) {
    // Create snapshot data
    const snapshot = {
      pose: poseName,
      score: Math.round(score),
      timestamp: new Date().toISOString(),
      angles: angles,
      severities: severities,
      imageData: canvas.toDataURL("image/jpeg", 0.8)
    };

    const feedback = lastEvaluation
      ? {
          corrections: [...lastEvaluation.corrections],
          tips: [...lastEvaluation.tips],
        }
      : {
          corrections: [],
          tips: [],
        };

    // Save to localStorage for dashboard
    try {
      let snapshots = JSON.parse(localStorage.getItem("poseSnapshots") || "[]");
      snapshots.push(snapshot);
      // Keep last 20 snapshots
      if (snapshots.length > 20) {
        snapshots = snapshots.slice(-20);
      }
      localStorage.setItem("poseSnapshots", JSON.stringify(snapshots));

      renderSavedSnapshot(snapshot, feedback);
      
      // Show confirmation
      setStatus(`✓ Snapshot saved! Score: ${Math.round(score)}%`);
      
      // Disable snap button briefly
      if (snapBtn) {
        snapBtn.disabled = true;
        setTimeout(() => {
          if (snapBtn) snapBtn.disabled = false;
        }, 1500);
      }
    } catch (err) {
      console.error("Failed to save snapshot:", err);
    }
  }

  function renderSavedSnapshot(snapshot, feedback) {
    if (!savedResultEl || !savedSnapshotImgEl) return;

    savedResultEl.style.display = "block";
    savedSnapshotImgEl.src = snapshot.imageData;
    if (savedSnapshotScoreEl) {
      savedSnapshotScoreEl.textContent = `${Math.round(snapshot.score)}%`;
    }
    if (savedSnapshotPoseEl) {
      savedSnapshotPoseEl.textContent = snapshot.pose || "Pose";
    }
    if (savedSnapshotTimeEl) {
      const time = new Date(snapshot.timestamp);
      savedSnapshotTimeEl.textContent = `Saved ${time.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}`;
    }

    setList(
      savedCorrectionsEl,
      feedback && feedback.corrections && feedback.corrections.length
        ? feedback.corrections.slice(0, 3)
        : ["No major corrections at capture time."],
    );
    setList(
      savedTipsEl,
      feedback && feedback.tips && feedback.tips.length
        ? feedback.tips.slice(0, 2)
        : ["Maintain your breathing and keep steady."],
    );
  }

  function lockBestResultAndSave(reasonText) {
    if (bestEvaluation) {
      scoreEl.textContent = `${bestEvaluation.score}`;
      setList(correctionsEl, bestEvaluation.corrections.slice(0, 4));
      setList(tipsEl, bestEvaluation.tips.slice(0, 3));

      if (bestEvaluation.score >= 70) {
        captureSnapshot(bestEvaluation.score, poseSelect.value, bestAngles || {}, bestEvaluation.severities || {});
      }

      setStatus(`${reasonText} Highest score: ${bestEvaluation.score}%`);
    } else {
      setStatus("No stable pose captured yet. Try again.");
    }
  }

  function endLiveStream() {
    running = false;
    startBtn.disabled = false;

    if (stopBtn) {
      stopBtn.disabled = true;
      stopBtn.style.display = "none";
    }

    if (snapBtn) {
      snapBtn.style.display = "none";
    }

    if (mediaStream) {
      mediaStream.getTracks().forEach((track) => track.stop());
      mediaStream = null;
    }

    video.srcObject = null;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  }

  async function setupPoseModel() {
    if (pose) return pose;

    if (!window.Pose) {
      setStatus("MediaPipe Pose library not loaded. Check internet connection.");
      throw new Error("window.Pose not available");
    }

    pose = new window.Pose({
      locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`,
    });

    pose.setOptions({
      modelComplexity: 1,
      smoothLandmarks: true,
      enableSegmentation: false,
      minDetectionConfidence: 0.55,
      minTrackingConfidence: 0.55,
    });

    pose.onResults((results) => {
      if (!running) return;

      const width = video.videoWidth || 640;
      const height = video.videoHeight || 480;
      if (canvas.width !== width || canvas.height !== height) {
        canvas.width = width;
        canvas.height = height;
      }

      const landmarks = results.poseLandmarks || [];
      const angles = landmarks.length ? calculateAngles(landmarks) : {
        "Shoulder Angle": null,
        "Elbow Angle": null,
        "Hip Angle": null,
        "Knee Angle": null,
      };

      let evaluation = {
        score: 0,
        severities: {},
        corrections: ["No pose detected. Step back and keep full body in frame."],
        tips: ["Ensure good lighting and enough distance from camera."],
      };

      if (landmarks.length && currentReference) {
        evaluation = evaluatePose(angles, currentReference);
      }

      lastEvaluation = {
        score: evaluation.score,
        corrections: [...evaluation.corrections],
        tips: [...evaluation.tips],
        severities: { ...evaluation.severities },
      };

      try {
        if (window.PoseOverlay) {
          window.PoseOverlay.drawOverlay(ctx, canvas.width, canvas.height, landmarks, angles, evaluation.severities);
        }
      } catch (drawErr) {
        console.error("Canvas drawing error:", drawErr);
      }

      scoreEl.textContent = `${evaluation.score}`;
      setList(correctionsEl, evaluation.corrections.slice(0, 4));
      setList(tipsEl, evaluation.tips.slice(0, 3));

      if (landmarks.length && currentReference && (!bestEvaluation || evaluation.score >= bestEvaluation.score)) {
        bestEvaluation = {
          score: evaluation.score,
          corrections: [...evaluation.corrections],
          tips: [...evaluation.tips],
          severities: { ...evaluation.severities },
        };
        bestAngles = { ...angles };
      }

      const poseStill = landmarks.length && currentReference ? isStill(angles) : false;
      if (poseStill) {
        stillPoseFrames += 1;
      } else {
        stillPoseFrames = 0;
      }

      if (!autoFinalized && stillPoseFrames >= AUTO_FINALIZE_STILL_FRAMES && bestEvaluation) {
        autoFinalized = true;
        endLiveStream();
        lockBestResultAndSave("Pose held steady. Final result ready.");
        return;
      }

      // Snapshot logic
      const currentScore = evaluation.score;
      
      // Show snap button if score is good (>70)
      if (snapBtn && currentScore > 70) {
        snapBtn.style.display = "block";
      }

      // Auto-snap at highest score
      if (currentScore > highestScore - 5) {
        highestScore = Math.max(highestScore, currentScore);
        
        if (isStill(angles)) {
          stillCounter++;
          if (stillCounter >= snapThreshold && currentScore > 70) {
            captureSnapshot(currentScore, poseSelect.value, angles, evaluation.severities);
            stillCounter = 0;
          }
        } else {
          stillCounter = 0;
        }
      }

      lastFrameAngles = JSON.parse(JSON.stringify(angles));
    });

    return pose;
  }

  async function processLoop(ts) {
    if (!running || !pose || !video.srcObject) return;

    if (!lastProcessTs || ts - lastProcessTs >= PROCESS_EVERY_MS) {
      lastProcessTs = ts;
      try {
        await pose.send({ image: video });
      } catch (err) {
        setStatus("Pose processing paused. Try restarting webcam.");
      }
    }

    window.requestAnimationFrame(processLoop);
  }

  async function startWebcam() {
    const selectedPose = poseSelect.value;
    if (!selectedPose) {
      setStatus("Select a pose first.");
      return;
    }

    try {
      const refData = await getReferenceForPose(selectedPose);
      currentReference = refData.reference;
      currentTolerance = refData.tolerance;
      void currentTolerance;
    } catch (err) {
      setStatus(err.message || "Failed to load pose reference.");
      return;
    }

    try {
      mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "user", width: { ideal: 960 }, height: { ideal: 540 } },
        audio: false,
      });

      video.srcObject = mediaStream;
      
      try {
        await video.play();
      } catch (playErr) {
        setStatus("Video playback failed: " + playErr.message);
        mediaStream.getTracks().forEach((track) => track.stop());
        return;
      }

      await setupPoseModel();

      // Reset snapshot tracking
      highestScore = 0;
      lastFrameAngles = null;
      stillCounter = 0;
      stillPoseFrames = 0;
      autoFinalized = false;
      bestEvaluation = null;
      bestAngles = null;
      lastEvaluation = null;
      if (snapBtn) {
        snapBtn.style.display = "none";
      }

      running = true;
      lastProcessTs = 0;
      startBtn.disabled = true;
      if (stopBtn) {
        stopBtn.style.display = "none";
        stopBtn.disabled = true;
      }
      setStatus("Live analysis running.");
      window.requestAnimationFrame(processLoop);
    } catch (err) {
      setStatus("Error: " + (err.message || "Could not access webcam. Check browser permissions."));
    }
  }

  function stopWebcam() {
    endLiveStream();
    lockBestResultAndSave("Analysis stopped.");

    // Reset live-only trackers while preserving locked display values.
    highestScore = 0;
    lastFrameAngles = null;
    stillCounter = 0;
    stillPoseFrames = 0;
    autoFinalized = false;
  }

  startBtn.addEventListener("click", startWebcam);
  
  if (stopBtn) {
    stopBtn.addEventListener("click", stopWebcam);
  }

  if (snapBtn) {
    snapBtn.addEventListener("click", () => {
      if (running) {
        const score = parseInt(scoreEl.textContent) || 0;
        captureSnapshot(score, poseSelect.value, lastFrameAngles || {}, {});
      }
    });
  }

  poseSelect.addEventListener("change", () => {
    currentReference = null;
    setStatus("Pose changed. Start webcam to analyze this pose.");
  });

  window.addEventListener("livePose:stop", stopWebcam);
  window.addEventListener("beforeunload", stopWebcam);
})();
