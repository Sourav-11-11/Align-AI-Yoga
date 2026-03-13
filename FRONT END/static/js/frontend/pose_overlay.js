(function () {
  const LEFT = {
    shoulder: 11,
    elbow: 13,
    wrist: 15,
    hip: 23,
    knee: 25,
    ankle: 27,
  };

  const RIGHT = {
    shoulder: 12,
    elbow: 14,
    wrist: 16,
    hip: 24,
    knee: 26,
    ankle: 28,
  };

  const CONNECTORS = [
    ["shoulder", "elbow"],
    ["elbow", "wrist"],
    ["shoulder", "hip"],
    ["hip", "knee"],
    ["knee", "ankle"],
  ];

  const ANGLE_JOINT = {
    "Shoulder Angle": "shoulder",
    "Elbow Angle": "elbow",
    "Hip Angle": "hip",
    "Knee Angle": "knee",
  };

  const SEVERITY_COLORS = {
    perfect: "#3EDB6D",
    minor: "#F6C945",
    moderate: "#F0A83A",
    major: "#F15A5A",
    missing: "#9EA3AD",
  };

  function pxPoint(lm, width, height) {
    return {
      x: lm.x * width,
      y: lm.y * height,
      visibility: typeof lm.visibility === "number" ? lm.visibility : 0,
    };
  }

  function pickBestSide(landmarks) {
    const build = (indices) => {
      const points = {};
      let visibilitySum = 0;
      ["shoulder", "elbow", "wrist", "hip", "knee", "ankle"].forEach((joint) => {
        const lm = landmarks[indices[joint]];
        points[joint] = lm;
        visibilitySum += (lm && typeof lm.visibility === "number") ? lm.visibility : 0;
      });
      return { points, visibilitySum };
    };

    const left = build(LEFT);
    const right = build(RIGHT);
    return right.visibilitySum > left.visibilitySum ? { side: "right", map: RIGHT } : { side: "left", map: LEFT };
  }

  function drawOverlay(ctx, width, height, landmarks, angles, severities) {
    if (!ctx || width <= 0 || height <= 0) {
      console.warn("Invalid canvas context or dimensions");
      return;
    }

    ctx.clearRect(0, 0, width, height);

    if (!landmarks || !landmarks.length) {
      return;
    }

    const best = pickBestSide(landmarks);

    CONNECTORS.forEach(([a, b]) => {
      const la = landmarks[best.map[a]];
      const lb = landmarks[best.map[b]];
      if (!la || !lb) return;
      if ((la.visibility || 0) < 0.3 || (lb.visibility || 0) < 0.3) return;

      ctx.beginPath();
      ctx.moveTo(la.x * width, la.y * height);
      ctx.lineTo(lb.x * width, lb.y * height);
      ctx.strokeStyle = "rgba(238, 229, 209, 0.75)";
      ctx.lineWidth = 3;
      ctx.stroke();
    });

    ["shoulder", "elbow", "wrist", "hip", "knee", "ankle"].forEach((joint) => {
      const lm = landmarks[best.map[joint]];
      if (!lm) return;

      const angleName = Object.keys(ANGLE_JOINT).find((name) => ANGLE_JOINT[name] === joint);
      const severity = angleName ? (severities[angleName] || "perfect") : "perfect";
      const color = SEVERITY_COLORS[severity] || SEVERITY_COLORS.perfect;

      const x = lm.x * width;
      const y = lm.y * height;

      ctx.beginPath();
      ctx.arc(x, y, 6, 0, Math.PI * 2);
      ctx.fillStyle = color;
      ctx.fill();
      ctx.lineWidth = 1.5;
      ctx.strokeStyle = "rgba(18, 14, 10, 0.8)";
      ctx.stroke();

      if (angleName && typeof angles[angleName] === "number") {
        ctx.font = "bold 13px Poppins, sans-serif";
        ctx.fillStyle = "#FFFFFF";
        ctx.strokeStyle = "rgba(0,0,0,0.55)";
        ctx.lineWidth = 3;
        const label = `${Math.round(angles[angleName])}\u00b0`;
        ctx.strokeText(label, x + 8, y - 8);
        ctx.fillText(label, x + 8, y - 8);
      }
    });

    ctx.font = "600 12px Poppins, sans-serif";
    ctx.fillStyle = "rgba(255, 255, 255, 0.85)";
    ctx.fillText(`Side: ${best.side}`, 12, 20);
  }

  window.PoseOverlay = {
    drawOverlay,
    pickBestSide,
    LEFT,
    RIGHT,
  };
})();
