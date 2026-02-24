import cv2
import numpy as np
import mediapipe as mp

POSES_REFERENCE_ANGLES = {
     "adho mukha svanasana": {
        "Shoulder Angle": 179,
        "Elbow Angle": 170,
        "Hip Angle": 161,
        "Knee Angle": 157
    },
    "adho mukha vriksasana": {
        "Shoulder Angle": 138,
        "Elbow Angle": 73,
        "Hip Angle": 180,
        "Knee Angle": 108
    },
    "agnistambhasana": {
        "Shoulder Angle": 164,
        "Elbow Angle": 102,
        "Hip Angle": 66,
        "Knee Angle": 177
    },
    "ananda balasana": {
        "Shoulder Angle": 177,
        "Elbow Angle": 171,
        "Hip Angle": 57,
        "Knee Angle": 179
    },
    "anantasana": {
        "Shoulder Angle": 83,
        "Elbow Angle": 65,
        "Hip Angle": 72,
        "Knee Angle": 176
    },

    "anjaneyasana": {
        "Shoulder Angle": 80,
        "Elbow Angle": 60,
        "Hip Angle": 60,
        "Knee Angle": 77
    },
    "ardha bhekasana": {
        "Shoulder Angle": 78,
        "Elbow Angle": 167,
        "Hip Angle": 141,
        "Knee Angle": 83
    },
    "ardha chandrasana": {
        "Shoulder Angle": 63,
        "Elbow Angle": 167,
        "Hip Angle": 176,
        "Knee Angle": 16
    },
    "ardha matsyendrasana": {
        "Shoulder Angle": 37,
        "Elbow Angle": 113,
        "Hip Angle": 118,
        "Knee Angle": 40
    },
    "ardha pincha mayurasana": {
        "Shoulder Angle": 149,
        "Elbow Angle": 168,
        "Hip Angle": 108,
        "Knee Angle": 86
    },
    "ardha uttanasana": {
        "Shoulder Angle": 63,
        "Elbow Angle": 133,
        "Hip Angle": 118,
        "Knee Angle": 87
    },
    "ashtanga namaskara": {
        "Shoulder Angle": 174,
        "Elbow Angle": 98,
        "Hip Angle": 171,
        "Knee Angle": 174
    },
    "astavakrasana": {
        "Shoulder Angle": 107,
        "Elbow Angle": 154,
        "Hip Angle": 97,
        "Knee Angle": 69
    },
    "baddha konasana": {
        "Shoulder Angle": 80,
        "Elbow Angle": 101,
        "Hip Angle": 130,
        "Knee Angle": 70
    },
    "bakasana": {
        "Shoulder Angle": 96,
        "Elbow Angle": 108,
        "Hip Angle": 123,
        "Knee Angle": 90
    }, 

    "bhairavasana": {
        "Shoulder Angle": 132,
        "Elbow Angle": 162,
        "Hip Angle": 197,
        "Knee Angle": 127
    },
    "bhekasana": {
        "Shoulder Angle": 144,
        "Elbow Angle": 108,
        "Hip Angle": 172,
        "Knee Angle": 91
    },
    "bitilasana": {
        "Shoulder Angle": 144,
        "Elbow Angle": 104,
        "Hip Angle": 177,
        "Knee Angle": 173
    },
    "camatkarasana": {
        "Shoulder Angle": 73,
        "Elbow Angle": 103,
        "Hip Angle": 85,
        "Knee Angle": 97
    },
    "chakravakasana": {
        "Shoulder Angle": 172,
        "Elbow Angle": 95,
        "Hip Angle": 174,
        "Knee Angle": 171
    },
    "chaturanga dandasana": {
        "Shoulder Angle": 137,
        "Elbow Angle": 138,
        "Hip Angle": 106,
        "Knee Angle": 176
    },
    "dandasana": {
        "Shoulder Angle": 127,
        "Elbow Angle": 60,
        "Hip Angle": 126,
        "Knee Angle": 180
    },
    "dhanurasana": {
        "Shoulder Angle": 63,
        "Elbow Angle": 111,
        "Hip Angle": 177,
        "Knee Angle": 167
    },
    "durvasasana": {
        "Shoulder Angle": 78,
        "Elbow Angle": 168,
        "Hip Angle": 102,
        "Knee Angle": 172
    },
    "dwi pada viparita dandasana": {
        "Shoulder Angle": 116,
        "Elbow Angle": 155,
        "Hip Angle": 135,
        "Knee Angle": 175
    }, 

    "eka pada koundinyanasana i": {
        "Shoulder Angle": 90,
        "Elbow Angle": 113,
        "Hip Angle": 83,
        "Knee Angle": 166
    }, 



    "eka pada koundinyanasana ii": {
        "Shoulder Angle": 202,  # example value for shoulder angle
        "Elbow Angle": 87,      # example value for elbow angle
        "Hip Angle": 52,        # example value for hip angle
        "Knee Angle": 180       # example value for knee angle
    },
    "eka pada rajakapotasana ii": {
        "Shoulder Angle": 89,   # example value for shoulder angle
        "Elbow Angle": 161,     # example value for elbow angle
        "Hip Angle": 168,       # example value for hip angle
        "Knee Angle": 95        # example value for knee angle
    },
    "ganda bherundasana": {
        "Shoulder Angle": 94,   # example value for shoulder angle
        "Elbow Angle": 173,     # example value for elbow angle
        "Hip Angle": 177,       # example value for hip angle
        "Knee Angle": 173       # example value for knee angle
    }, 

    "garbha pindasana": {
        "Shoulder Angle": 88,
        "Elbow Angle": 144,
        "Hip Angle": 60,
        "Knee Angle": 95
    },
    "garudasana": {
        "Shoulder Angle": 27,
        "Elbow Angle": 25,
        "Hip Angle": 28,
        "Knee Angle": 3
    },
    "gomukhasana": {
        "Shoulder Angle": 118,
        "Elbow Angle": 87,
        "Hip Angle": 59,
        "Knee Angle": 53
    },
    "hanumanasana": {
        "Shoulder Angle": 27,
        "Elbow Angle": 173,
        "Hip Angle": 156,
        "Knee Angle": 107
    },
    "janu sirsasana": {
        "Shoulder Angle": 158,
        "Elbow Angle": 74,
        "Hip Angle": 103,
        "Knee Angle": 169
    },
    "kapotasana": {
        "Shoulder Angle": 147,
        "Elbow Angle": 136,
        "Hip Angle": 165,
        "Knee Angle": 157
    },
    "krounchasana": {
        "Shoulder Angle": 67,
        "Elbow Angle": 102,
        "Hip Angle": 160,
        "Knee Angle": 66
    },
    "kurmasana": {
        "Shoulder Angle": 152,
        "Elbow Angle": 101,
        "Hip Angle": 108,
        "Knee Angle": 82
    },
    "lolasana": {
        "Shoulder Angle": 168,
        "Elbow Angle": 171,
        "Hip Angle": 101,
        "Knee Angle": 175
    },
    "makara adho mukha svanasana": {
        "Shoulder Angle": 88,
        "Elbow Angle": 144,
        "Hip Angle": 95,
        "Knee Angle": 60
    }, 
    "marichyasana i": {
        "Shoulder Angle": 80,  # example value for shoulder angle
        "Elbow Angle": 150,    # example value for elbow angle
        "Hip Angle": 160,      # example value for hip angle
        "Knee Angle": 90,      # example value for knee angle
    },
    "marichyasana iii": {
        "Shoulder Angle": 170,
        "Elbow Angle": 100,
        "Hip Angle": 110,
        "Knee Angle": 85,
    },
    "marjaryasana": {
        "Shoulder Angle": 167,
        "Elbow Angle": 135,
        "Hip Angle": 90,
        "Knee Angle": 50,
    },
    "mayurasana": {
        "Shoulder Angle": 70,
        "Elbow Angle": 90,
        "Hip Angle": 100,
        "Knee Angle": 90,
    },
    "natarajasana": {
        "Shoulder Angle": 87,
        "Elbow Angle": 65,
        "Hip Angle": 50,
        "Knee Angle": 95,
    },
    "padangusthasana": {
        "Shoulder Angle": 65,
        "Elbow Angle": 95,
        "Hip Angle": 110,
        "Knee Angle": 100,
    },
    "parighasana": {
        "Shoulder Angle": 87,
        "Elbow Angle": 125,
        "Hip Angle": 80,
        "Knee Angle": 70,
    },
    "parivrtta janu sirsasana": {
        "Shoulder Angle": 90,
        "Elbow Angle": 115,
        "Hip Angle": 95,
        "Knee Angle": 100,
    },
    "parivrtta parsvakonasana": {
        "Shoulder Angle": 170,
        "Elbow Angle": 110,
        "Hip Angle": 80,
        "Knee Angle": 60,
    },
    "parivrtta trikonasana": {
        "Shoulder Angle": 160,
        "Elbow Angle": 85,
        "Hip Angle": 75,
        "Knee Angle": 50,
    },

    "parsva bakasana": {
        "Shoulder Angle": 105,  # Shoulder angle for the first pose
        "Elbow Angle": 83,      # Elbow angle for the first pose
        "Hip Angle": 92,        # Hip angle for the first pose
        "Knee Angle": 177       # Knee angle for the first pose
    },
    "parsvottanasana": {
        "Shoulder Angle": 177,  # Shoulder angle for the second pose
        "Elbow Angle": 177,     # Elbow angle for the second pose
        "Hip Angle": 103,       # Hip angle for the second pose
        "Knee Angle": 177       # Knee angle for the second pose
    },
    "phalakasana": {
        "Shoulder Angle": 131,  # Shoulder angle for the third pose
        "Elbow Angle": 58,      # Elbow angle for the third pose
        "Hip Angle": 179,       # Hip angle for the third pose
        "Knee Angle": 179       # Knee angle for the third pose
    },
    "prasarita padottanasana": {
        "Shoulder Angle": 277,  # Shoulder angle for the fourth pose
        "Elbow Angle": 178,     # Elbow angle for the fourth pose
        "Hip Angle": 179,       # Hip angle for the fourth pose
        "Knee Angle": 178       # Knee angle for the fourth pose
    },
    "purvottanasana": {
        "Shoulder Angle": 178,  # Shoulder angle for the fifth pose
        "Elbow Angle": 157,     # Elbow angle for the fifth pose
        "Hip Angle": 147,       # Hip angle for the fifth pose
        "Knee Angle": 11        # Knee angle for the fifth pose
    },
    "salabhasana": {
        "Shoulder Angle": 178,  # Shoulder angle for the sixth pose
        "Elbow Angle": 157,     # Elbow angle for the sixth pose
        "Hip Angle": 179,       # Hip angle for the sixth pose
        "Knee Angle": 178       # Knee angle for the sixth pose
    },
    "salamba bhujangasana": {
        "Shoulder Angle": 177,  # Shoulder angle for the seventh pose
        "Elbow Angle": 177,     # Elbow angle for the seventh pose
        "Hip Angle": 103,       # Hip angle for the seventh pose
        "Knee Angle": 177       # Knee angle for the seventh pose
    },
    "salamba sarvangasana": {
        "Shoulder Angle": 177,  # Shoulder angle for the eighth pose
        "Elbow Angle": 103,     # Elbow angle for the eighth pose
        "Hip Angle": 177,       # Hip angle for the eighth pose
        "Knee Angle": 177       # Knee angle for the eighth pose
    },
    "salamba sirsasana": {
        "Shoulder Angle": 178,  # Shoulder angle for the ninth pose
        "Elbow Angle": 158,     # Elbow angle for the ninth pose
        "Hip Angle": 179,       # Hip angle for the ninth pose
        "Knee Angle": 179       # Knee angle for the ninth pose
    },
    "savasana": {
        "Shoulder Angle": 167,  # Shoulder angle for the tenth pose
        "Elbow Angle": 164,     # Elbow angle for the tenth pose
        "Hip Angle": 155,       # Hip angle for the tenth pose
        "Knee Angle": 158       # Knee angle for the tenth pose
    }, 

    "simhasana": {
        "Shoulder Angle": 163, 
        "Elbow Angle": 176, 
        "Knee Angle": 172,
        "Hip Angle": 108
    },

    "sukhasana": {
        "Shoulder Angle": 157, 
        "Elbow Angle": 80, 
        "Knee Angle": 93, 
        "Hip Angle": 179
    },
     "supta padangusthasana": {
        "Shoulder Angle": 50, 
        "Elbow Angle": 297, 
        "Knee Angle": 85, 
        "Hip Angle": 143
    },

    "supta virasana": {
        "Shoulder Angle": 99, 
        "Elbow Angle": 125, 
        "Knee Angle": 167,
        "Hip Angle": 179
    },
    "urdhva dhanurasana": {
        "Shoulder Angle": 158, 
        "Elbow Angle": 131, 
        "Knee Angle": 127, 
        "Hip Angle": 68
    },

    "urdhva hastasana": {
        "Shoulder Angle": 163, 
        "Elbow Angle": 176, 
        "Knee Angle": 172, 
        "Hip Angle": 108
    },
    "uttana shishosana": {
        "Shoulder Angle": 157, 
        "Elbow Angle": 80, 
        "Knee Angle": 93, 
        "Hip Angle": 179
    },
    "utthita ashwa sanchalanasana": {
        "Shoulder Angle": 50, 
        "Elbow Angle": 297, 
        "Knee Angle": 85, 
        "Hip Angle": 143
    },
    "utthita hasta padangustasana": {
        "Shoulder Angle": 179, 
        "Elbow Angle": 135, 
        "Knee Angle": 77, 
        "Hip Angle": 180
    },
    "utthita trikonasana": {
        "Shoulder Angle": 157, 
        "Elbow Angle": 158, 
        "Knee Angle": 177, 
        "Hip Angle": 120
    },
    "vajrasana": {
        "Shoulder Angle": 158, 
        "Elbow Angle": 131, 
        "Knee Angle": 127, 
        "Hip Angle": 68
    },
    "virabhadrasana i": {
        "Shoulder Angle": 178, 
        "Elbow Angle": 177, 
        "Knee Angle": 176, 
        "Hip Angle": 179
    },
    "virabhadrasana ii": {
        "Shoulder Angle": 180, 
        "Elbow Angle": 170, 
        "Knee Angle": 176, 
        "Hip Angle": 165
    }, 

    "virabhadrasana iii": {
        "Shoulder Angle": 112, 
        "Elbow Angle": 177, 
        "Knee Angle": 177, 
        "Hip Angle": 177
    },
    "virasana": {
        "Shoulder Angle": 111, 
        "Elbow Angle": 112, 
        "Knee Angle": 111, 
        "Hip Angle": 112
    },
    "vriksasana": {
        "Shoulder Angle": 177, 
        "Elbow Angle": 177, 
        "Knee Angle": 177, 
        "Hip Angle": 177
    },
    "yoganidrasana": {
        "Shoulder Angle": 267, 
        "Elbow Angle": 111, 
        "Knee Angle": 171, 
        "Hip Angle": 322
    },
}

# Function to calculate the angle between three points
def calculate_angle(a, b, c):
    a = np.array(a)  # First point
    b = np.array(b)  # Second point (vertex)
    c = np.array(c)  # Third point
    ba = a - b
    bc = c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    return np.degrees(angle)

# Function to provide dynamic correction suggestions based on angle differences
def provide_correction_suggestion(detected_angles, reference_angles):
    corrections = []
    for joint, detected_angle in detected_angles.items():
        reference_angle = reference_angles.get(joint)
        if reference_angle:
            angle_diff = detected_angle - reference_angle
            if angle_diff < -5:
                corrections.append(f"Increase the {joint} angle by {abs(angle_diff):.2f}°")
            elif angle_diff > 5:
                corrections.append(f"Decrease the {joint} angle by {abs(angle_diff):.2f}°")
            else:
                corrections.append(f"The {joint} angle is correct.")
        else:
            corrections.append(f"{joint} angle is not available in the reference data.")
    return corrections

# Function to process the image and calculate angles
def process_image(image_path, pose_name):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Initialize Mediapipe Pose
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=True, model_complexity=2, min_detection_confidence=0.5)

    # Process the image to detect pose landmarks
    results = pose.process(image_rgb)

    # Check if landmarks are detected
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        h, w, _ = image.shape  # Get image dimensions for scaling

        # Extract coordinates of key points
        points = {
            "left_shoulder": [int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x * w),
                              int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y * h)],
            "left_elbow": [int(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x * w),
                           int(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y * h)],
            "left_wrist": [int(landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x * w),
                           int(landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y * h)],
            "left_hip": [int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].x * w),
                         int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].y * h)],
            "left_knee": [int(landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x * w),
                         int(landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y * h)],
            "left_ankle": [int(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x * w),
                           int(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y * h)],
        }

        # Calculate angles
        detected_angles = {
            "Shoulder Angle": calculate_angle(points["left_elbow"], points["left_shoulder"], points["left_hip"]),
            "Elbow Angle": calculate_angle(points["left_wrist"], points["left_elbow"], points["left_shoulder"]),
            "Hip Angle": calculate_angle(points["left_shoulder"], points["left_hip"], points["left_knee"]),
            "Knee Angle": calculate_angle(points["left_hip"], points["left_knee"], points["left_ankle"]),
        }

        # Compare with reference angles for the pose
        reference_angles = POSES_REFERENCE_ANGLES.get(pose_name)
        if reference_angles:
            corrections = provide_correction_suggestion(detected_angles, reference_angles)
            return corrections
        else:
            return ["Pose reference data not available."]
    else:
        return ["No pose landmarks detected in the image."]

# Example usage:
image_path = r'data\yoganidrasana\21-0.png' 
pose_name = "yoganidrasana"  
correction_feedback = process_image(image_path, pose_name)

for correction in correction_feedback:
    print(correction)
