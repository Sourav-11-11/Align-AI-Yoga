"""
Reference joint angles for 70+ yoga poses.

These values were calibrated from the training image dataset using
MediaPipe's left-side body landmarks. Each angle is the ideal joint
angle (in degrees) that a correctly performed pose should exhibit.

Angles:
  Shoulder Angle — at LEFT_SHOULDER: elbow → shoulder → hip
  Elbow Angle    — at LEFT_ELBOW:    wrist  → elbow   → shoulder
  Hip Angle      — at LEFT_HIP:      shoulder → hip   → knee
  Knee Angle     — at LEFT_KNEE:     hip    → knee    → ankle
"""

REFERENCE_ANGLES: dict[str, dict[str, float]] = {
    "adho mukha svanasana": {
        "Shoulder Angle": 179, "Elbow Angle": 170, "Hip Angle": 161, "Knee Angle": 157,
    },
    "adho mukha vriksasana": {
        "Shoulder Angle": 138, "Elbow Angle": 73, "Hip Angle": 180, "Knee Angle": 108,
    },
    "agnistambhasana": {
        "Shoulder Angle": 164, "Elbow Angle": 102, "Hip Angle": 66, "Knee Angle": 177,
    },
    "ananda balasana": {
        "Shoulder Angle": 177, "Elbow Angle": 171, "Hip Angle": 57, "Knee Angle": 179,
    },
    "anantasana": {
        "Shoulder Angle": 83, "Elbow Angle": 65, "Hip Angle": 72, "Knee Angle": 176,
    },
    "anjaneyasana": {
        "Shoulder Angle": 80, "Elbow Angle": 60, "Hip Angle": 60, "Knee Angle": 77,
    },
    "ardha bhekasana": {
        "Shoulder Angle": 78, "Elbow Angle": 167, "Hip Angle": 141, "Knee Angle": 83,
    },
    "ardha chandrasana": {
        "Shoulder Angle": 63, "Elbow Angle": 167, "Hip Angle": 176, "Knee Angle": 16,
    },
    "ardha matsyendrasana": {
        "Shoulder Angle": 37, "Elbow Angle": 113, "Hip Angle": 118, "Knee Angle": 40,
    },
    "ardha pincha mayurasana": {
        "Shoulder Angle": 149, "Elbow Angle": 168, "Hip Angle": 108, "Knee Angle": 86,
    },
    "ardha uttanasana": {
        "Shoulder Angle": 63, "Elbow Angle": 133, "Hip Angle": 118, "Knee Angle": 87,
    },
    "ashtanga namaskara": {
        "Shoulder Angle": 174, "Elbow Angle": 98, "Hip Angle": 171, "Knee Angle": 174,
    },
    "astavakrasana": {
        "Shoulder Angle": 107, "Elbow Angle": 154, "Hip Angle": 97, "Knee Angle": 69,
    },
    "baddha konasana": {
        "Shoulder Angle": 80, "Elbow Angle": 101, "Hip Angle": 130, "Knee Angle": 70,
    },
    "bakasana": {
        "Shoulder Angle": 96, "Elbow Angle": 108, "Hip Angle": 123, "Knee Angle": 90,
    },
    "bhairavasana": {
        "Shoulder Angle": 132, "Elbow Angle": 162, "Hip Angle": 163, "Knee Angle": 127,
    },
    "bhekasana": {
        "Shoulder Angle": 144, "Elbow Angle": 108, "Hip Angle": 172, "Knee Angle": 91,
    },
    "bitilasana": {
        "Shoulder Angle": 144, "Elbow Angle": 104, "Hip Angle": 177, "Knee Angle": 173,
    },
    "camatkarasana": {
        "Shoulder Angle": 73, "Elbow Angle": 103, "Hip Angle": 85, "Knee Angle": 97,
    },
    "chakravakasana": {
        "Shoulder Angle": 172, "Elbow Angle": 95, "Hip Angle": 174, "Knee Angle": 171,
    },
    "chaturanga dandasana": {
        "Shoulder Angle": 137, "Elbow Angle": 138, "Hip Angle": 106, "Knee Angle": 176,
    },
    "dandasana": {
        "Shoulder Angle": 127, "Elbow Angle": 60, "Hip Angle": 126, "Knee Angle": 180,
    },
    "dhanurasana": {
        "Shoulder Angle": 63, "Elbow Angle": 111, "Hip Angle": 177, "Knee Angle": 167,
    },
    "durvasasana": {
        "Shoulder Angle": 78, "Elbow Angle": 168, "Hip Angle": 102, "Knee Angle": 172,
    },
    "dwi pada viparita dandasana": {
        "Shoulder Angle": 116, "Elbow Angle": 155, "Hip Angle": 135, "Knee Angle": 175,
    },
    "eka pada koundinyanasana i": {
        "Shoulder Angle": 90, "Elbow Angle": 113, "Hip Angle": 83, "Knee Angle": 166,
    },
    "eka pada koundinyanasana ii": {
        "Shoulder Angle": 158, "Elbow Angle": 87, "Hip Angle": 52, "Knee Angle": 180,
    },
    "eka pada rajakapotasana ii": {
        "Shoulder Angle": 89, "Elbow Angle": 161, "Hip Angle": 168, "Knee Angle": 95,
    },
    "ganda bherundasana": {
        "Shoulder Angle": 94, "Elbow Angle": 173, "Hip Angle": 177, "Knee Angle": 173,
    },
    "garbha pindasana": {
        "Shoulder Angle": 88, "Elbow Angle": 144, "Hip Angle": 60, "Knee Angle": 95,
    },
    "garudasana": {
        "Shoulder Angle": 27, "Elbow Angle": 25, "Hip Angle": 28, "Knee Angle": 3,
    },
    "gomukhasana": {
        "Shoulder Angle": 118, "Elbow Angle": 87, "Hip Angle": 59, "Knee Angle": 53,
    },
    "hanumanasana": {
        "Shoulder Angle": 27, "Elbow Angle": 173, "Hip Angle": 156, "Knee Angle": 107,
    },
    "janu sirsasana": {
        "Shoulder Angle": 158, "Elbow Angle": 74, "Hip Angle": 103, "Knee Angle": 169,
    },
    "kapotasana": {
        "Shoulder Angle": 147, "Elbow Angle": 136, "Hip Angle": 165, "Knee Angle": 157,
    },
    "krounchasana": {
        "Shoulder Angle": 67, "Elbow Angle": 102, "Hip Angle": 160, "Knee Angle": 66,
    },
    "kurmasana": {
        "Shoulder Angle": 152, "Elbow Angle": 101, "Hip Angle": 108, "Knee Angle": 82,
    },
    "lolasana": {
        "Shoulder Angle": 168, "Elbow Angle": 171, "Hip Angle": 101, "Knee Angle": 175,
    },
    "makara adho mukha svanasana": {
        "Shoulder Angle": 88, "Elbow Angle": 144, "Hip Angle": 95, "Knee Angle": 60,
    },
    "makarasana": {
        "Shoulder Angle": 170, "Elbow Angle": 160, "Hip Angle": 175, "Knee Angle": 175,
    },
    "marichyasana i": {
        "Shoulder Angle": 80, "Elbow Angle": 150, "Hip Angle": 160, "Knee Angle": 90,
    },
    "marichyasana iii": {
        "Shoulder Angle": 170, "Elbow Angle": 100, "Hip Angle": 110, "Knee Angle": 85,
    },
    "marjaryasana": {
        "Shoulder Angle": 167, "Elbow Angle": 135, "Hip Angle": 90, "Knee Angle": 50,
    },
    "mayurasana": {
        "Shoulder Angle": 70, "Elbow Angle": 90, "Hip Angle": 100, "Knee Angle": 90,
    },
    "natarajasana": {
        "Shoulder Angle": 87, "Elbow Angle": 65, "Hip Angle": 50, "Knee Angle": 95,
    },
    "padangusthasana": {
        "Shoulder Angle": 65, "Elbow Angle": 95, "Hip Angle": 110, "Knee Angle": 100,
    },
    "parighasana": {
        "Shoulder Angle": 87, "Elbow Angle": 125, "Hip Angle": 80, "Knee Angle": 70,
    },
    "parivrtta janu sirsasana": {
        "Shoulder Angle": 90, "Elbow Angle": 115, "Hip Angle": 95, "Knee Angle": 100,
    },
    "parivrtta parsvakonasana": {
        "Shoulder Angle": 170, "Elbow Angle": 110, "Hip Angle": 80, "Knee Angle": 60,
    },
    "parivrtta trikonasana": {
        "Shoulder Angle": 160, "Elbow Angle": 85, "Hip Angle": 75, "Knee Angle": 50,
    },
    "parsva bakasana": {
        "Shoulder Angle": 105, "Elbow Angle": 83, "Hip Angle": 92, "Knee Angle": 177,
    },
    "parsvottanasana": {
        "Shoulder Angle": 177, "Elbow Angle": 177, "Hip Angle": 103, "Knee Angle": 177,
    },
    "phalakasana": {
        "Shoulder Angle": 131, "Elbow Angle": 58, "Hip Angle": 179, "Knee Angle": 179,
    },
    "prasarita padottanasana": {
        "Shoulder Angle": 83, "Elbow Angle": 178, "Hip Angle": 179, "Knee Angle": 178,
    },
    "purvottanasana": {
        "Shoulder Angle": 178, "Elbow Angle": 157, "Hip Angle": 147, "Knee Angle": 11,
    },
    "salabhasana": {
        "Shoulder Angle": 178, "Elbow Angle": 157, "Hip Angle": 179, "Knee Angle": 178,
    },
    "salamba bhujangasana": {
        "Shoulder Angle": 177, "Elbow Angle": 177, "Hip Angle": 103, "Knee Angle": 177,
    },
    "salamba sarvangasana": {
        "Shoulder Angle": 177, "Elbow Angle": 103, "Hip Angle": 177, "Knee Angle": 177,
    },
    "salamba sirsasana": {
        "Shoulder Angle": 178, "Elbow Angle": 158, "Hip Angle": 179, "Knee Angle": 179,
    },
    "savasana": {
        "Shoulder Angle": 167, "Elbow Angle": 164, "Hip Angle": 155, "Knee Angle": 158,
    },
    "simhasana": {
        "Shoulder Angle": 163, "Elbow Angle": 176, "Hip Angle": 108, "Knee Angle": 172,
    },
    "sukhasana": {
        "Shoulder Angle": 157, "Elbow Angle": 80, "Hip Angle": 179, "Knee Angle": 93,
    },
    "supta padangusthasana": {
        "Shoulder Angle": 50, "Elbow Angle": 63, "Hip Angle": 143, "Knee Angle": 85,
    },
    "supta virasana": {
        "Shoulder Angle": 99, "Elbow Angle": 125, "Hip Angle": 179, "Knee Angle": 167,
    },
    "tulasana": {
        "Shoulder Angle": 95, "Elbow Angle": 160, "Hip Angle": 98, "Knee Angle": 90,
    },
    "urdhva dhanurasana": {
        "Shoulder Angle": 158, "Elbow Angle": 131, "Hip Angle": 68, "Knee Angle": 127,
    },
    "urdhva hastasana": {
        "Shoulder Angle": 163, "Elbow Angle": 176, "Hip Angle": 108, "Knee Angle": 172,
    },
    "uttana shishosana": {
        "Shoulder Angle": 157, "Elbow Angle": 80, "Hip Angle": 179, "Knee Angle": 93,
    },
    "utthita ashwa sanchalanasana": {
        "Shoulder Angle": 50, "Elbow Angle": 63, "Hip Angle": 143, "Knee Angle": 85,
    },
    "utthita hasta padangustasana": {
        "Shoulder Angle": 179, "Elbow Angle": 135, "Hip Angle": 180, "Knee Angle": 77,
    },
    "utthita trikonasana": {
        "Shoulder Angle": 157, "Elbow Angle": 158, "Hip Angle": 120, "Knee Angle": 177,
    },
    "vajrasana": {
        "Shoulder Angle": 158, "Elbow Angle": 131, "Hip Angle": 68, "Knee Angle": 127,
    },
    "virabhadrasana i": {
        "Shoulder Angle": 178, "Elbow Angle": 177, "Hip Angle": 179, "Knee Angle": 176,
    },
    "virabhadrasana ii": {
        "Shoulder Angle": 180, "Elbow Angle": 170, "Hip Angle": 165, "Knee Angle": 176,
    },
    "virabhadrasana iii": {
        "Shoulder Angle": 112, "Elbow Angle": 177, "Hip Angle": 177, "Knee Angle": 177,
    },
    "virasana": {
        "Shoulder Angle": 111, "Elbow Angle": 112, "Hip Angle": 112, "Knee Angle": 111,
    },
    "vriksasana": {
        "Shoulder Angle": 177, "Elbow Angle": 177, "Hip Angle": 177, "Knee Angle": 177,
    },
    "yoganidrasana": {
        "Shoulder Angle": 93, "Elbow Angle": 111, "Hip Angle": 38, "Knee Angle": 171,
    },
}
