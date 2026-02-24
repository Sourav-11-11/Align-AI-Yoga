from flask import *
import mysql.connector, joblib, random, string, base64, pickle
import pandas as pd
import numpy as np
from datetime import datetime
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from flask_mail import Mail, Message
import pandas as pd 
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import svds
import os,random,shutil
import cv2
import os
import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import json
import math
import os
from PIL import Image


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
        "Shoulder Angle": 202, 
        "Elbow Angle": 87,      
        "Hip Angle": 52,      
        "Knee Angle": 180     
    },
    "eka pada rajakapotasana ii": {
        "Shoulder Angle": 89,  
        "Elbow Angle": 161,     
        "Hip Angle": 168,     
        "Knee Angle": 95      
    },
    "ganda bherundasana": {
        "Shoulder Angle": 94,  
        "Elbow Angle": 173,     
        "Hip Angle": 177,     
        "Knee Angle": 173     
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
        "Shoulder Angle": 80, 
        "Elbow Angle": 150,    
        "Hip Angle": 160,    
        "Knee Angle": 90,    
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
        "Shoulder Angle": 105,  
        "Elbow Angle": 83,      
        "Hip Angle": 92,       
        "Knee Angle": 177     
    },
    "parsvottanasana": {
        "Shoulder Angle": 177, 
        "Elbow Angle": 177,   
        "Hip Angle": 103,      
        "Knee Angle": 177      
    },
    "phalakasana": {
        "Shoulder Angle": 131,  
        "Elbow Angle": 58,     
        "Hip Angle": 179,      
        "Knee Angle": 179       
    },
    "prasarita padottanasana": {
        "Shoulder Angle": 277,  
        "Elbow Angle": 178,     
        "Hip Angle": 179,       
        "Knee Angle": 178      
    },
    "purvottanasana": {
        "Shoulder Angle": 178, 
        "Elbow Angle": 157,
        "Hip Angle": 147,       
        "Knee Angle": 11      
    },
    "salabhasana": {
        "Shoulder Angle": 178,  
        "Elbow Angle": 157,    
        "Hip Angle": 179,     
        "Knee Angle": 178     
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


def process_image(image_path, pose_name):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Initialize Mediapipe Pose
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=True, model_complexity=2, min_detection_confidence=0.5)

    # Process the image to detect pose landmarks
    results = pose.process(image_rgb)
    print(6666666666666666666666666, results)

    # Check if landmarks are detected
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        print(7777777777777777777777777777777, landmarks)
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
        print(555555555555555555, reference_angles)
        if reference_angles:
            corrections = provide_correction_suggestion(detected_angles, reference_angles)
        else:
            corrections = ["Pose reference data not available."]

        # Draw points on the image
        for key, point in points.items():
            cv2.circle(image, tuple(point), 5, (0, 255, 0), -1)  # Draw points in green

        # Draw lines connecting joints
        cv2.line(image, tuple(points["left_shoulder"]), tuple(points["left_elbow"]), (255, 0, 0), 2)  # Blue line
        cv2.line(image, tuple(points["left_elbow"]), tuple(points["left_wrist"]), (255, 0, 0), 2)
        cv2.line(image, tuple(points["left_shoulder"]), tuple(points["left_hip"]), (255, 0, 0), 2)
        cv2.line(image, tuple(points["left_hip"]), tuple(points["left_knee"]), (255, 0, 0), 2)
        cv2.line(image, tuple(points["left_knee"]), tuple(points["left_ankle"]), (255, 0, 0), 2)

        # Annotate angles on the image
        for joint, angle in detected_angles.items():
            if "Elbow" in joint:
                key_point = "left_elbow"
            elif "Hip" in joint:
                key_point = "left_hip"
            elif "Knee" in joint:
                key_point = "left_knee"
            else:
                key_point = "left_shoulder"
            if key_point in points:
                cv2.putText(image, f"{int(angle)}\u00B0", tuple(points[key_point]),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)  # White text for angles

        # Save the annotated image
        annotated_image_filename = f"annotated_{pose_name}.png"
        annotated_image_path = os.path.join('static', 'saved_images', annotated_image_filename)
        cv2.imwrite(annotated_image_path, image)

        return corrections, annotated_image_filename  # Return corrections and the image filename
    else:
        return ["No pose landmarks detected in the image."], None




app = Flask(__name__)
app.secret_key = 'yoga' 

# Initialize Flask-Mail
mail = Mail(app)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    port="3306",
    database='yoga'
)

mycursor = mydb.cursor()

def executionquery(query,values):
    mycursor.execute(query,values)
    mydb.commit()
    return

def retrivequery1(query,values):
    mycursor.execute(query,values)
    data = mycursor.fetchall()
    return data

def retrivequery2(query):
    mycursor.execute(query)
    data = mycursor.fetchall()
    return data
    


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        c_password = request.form['c_password']

        # img = request.files['img']
        # binary_data = img.read()

        if password == c_password:
            query = "SELECT email FROM users"
            exist_data = retrivequery2(query)
            exist_email_list = [i[0] for i in exist_data]

            if email not in exist_email_list:
                query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
                values = (name, email, password)
                executionquery(query, values)

                return render_template('login.html', message="Successfully Registered!")
            return render_template('register.html', message="This email ID already exists!")
        return render_template('register.html', message="Confirm password does not match!")
    return render_template('register.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        
        query = "SELECT * FROM users WHERE email = %s"
        values = (email,)
        user_data = retrivequery1(query, values)

        if user_data:
            if password == user_data[0][3]:
                session["user_id"] = user_data[0][0]
                session["user_name"] = user_data[0][1]
                session["user_email"] = user_data[0][2]

                return redirect("/home")
            return render_template('login.html', message="Invalid Password!!")
        return render_template('login.html', message="This email ID does not exist!")
    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('home.html')

### yoga module

def recommend_poses(mood, u, sigma, vt, top_n=3):
    mood_idx = mood_to_idx[mood]
    mood_latent_features = np.dot(u[mood_idx, :], sigma)
    pose_scores = np.dot(mood_latent_features, vt)

    top_pose_indices = np.argsort(pose_scores)[::-1][:top_n]
    recommended_poses = [poses[idx] for idx in top_pose_indices]

    return recommended_poses


df = pd.read_csv("dataset/Recommendation_yoga_data.csv")

moods = df['Mood Before'].unique()
poses = df['Yoga Practice'].unique()

mood_to_idx = {mood: idx for idx, mood in enumerate(moods)}
pose_to_idx = {pose: idx for idx, pose in enumerate(poses)}

interaction_matrix = csr_matrix((len(mood_to_idx), len(pose_to_idx)), dtype=int)
interaction_matrix_float = interaction_matrix.astype('float32')

for _, row in df.iterrows():
    mood_idx = mood_to_idx[row['Mood Before']]
    pose_idx = pose_to_idx[row['Yoga Practice']]
    interaction_matrix_float[mood_idx, pose_idx] += 1

num_features = min(interaction_matrix_float.shape) - 1  # Choose a suitable number of features
u, sigma, vt = svds(interaction_matrix_float, k=num_features)
sigma_diag_matrix = np.diag(sigma)


@app.route('/yoga1', methods=['POST','GET'])
def yoga1():
    if request.method=='POST':
        mood = request.form['mood']

        recommended_poses = recommend_poses(mood, u, sigma_diag_matrix, vt, top_n=3)

        main_folder_path = os.path.join(os.getcwd(),'data')
        to_copy_path = os.path.join(os.getcwd(),'static','img')

        files_to_send = []
        for folder in recommended_poses:
            to_search_folder = os.path.join(main_folder_path,folder)
            for temp in os.walk(to_search_folder):
                single_file_name = random.choice(temp[2])
                files_to_send.append((f'/static/img/{single_file_name}',folder))
                shutil.copyfile(os.path.join(to_search_folder,single_file_name) , os.path.join(to_copy_path,single_file_name))
                break

        return render_template('yoga2.html', files = files_to_send, mood = mood)
    return render_template('yoga1.html')


import os
import cv2
import numpy as np
import mediapipe as mp


@app.route('/yoga2', methods=["POST", "GET"])
def yoga2():
    print("started")
    prd_result = ""
    annotated_image_filename = ""
    
    if request.method == "POST":
        user_id = session["user_id"]
        user_name = session["user_name"]
        user_email = session["user_email"]

        pose_name = request.form.get("pose_name")
        print(11111111111111111111, pose_name)
        mood = request.form['mood']
        myfile = request.files['img']
        fn = myfile.filename

        # Ensure the filename is secure
        from werkzeug.utils import secure_filename
        fn = secure_filename(fn)

        # Define paths
        saved_images_path = os.path.join('static', 'saved_images')
        if not os.path.exists(saved_images_path):
            os.makedirs(saved_images_path)

        mypath = os.path.join(saved_images_path, fn)
        myfile.save(mypath)

        pose_name=pose_name.lower()
        correction_feedback, annotated_image_filename  = process_image(mypath, pose_name)
        prd_result=[]

        for correction in correction_feedback:
            # print(correction)
            prd_result.append(correction)
            
        print(00000000000000000000000000000,prd_result)

        return render_template('yoga3.html', feedback=prd_result, image_name=annotated_image_filename if annotated_image_filename else fn)
    return render_template('yoga3.html')


@app.route('/dashboard', methods=["POST","GET"])
def dashboard():
    user_email = session["user_email"]
    if request.method=="POST":
        frm_date = request.form['frm_date']
        to_date = request.form['to_date']

        query = "SELECT * FROM dashboard WHERE email = %s AND (date BETWEEN %s AND %s)"
        values = (user_email, frm_date, to_date)
        dashboard_data = retrivequery1(query, values)

    else:
        query = "SELECT * FROM dashboard WHERE email = %s"
        values = (user_email,)
        dashboard_data = retrivequery1(query, values)

    dashboard_list = []
    for item in dashboard_data:
        dashboard_list.append({
            'id': item[0],
            'user_name': item[1],
            'user_email': item[2],
            'mood_name': item[3],
            'yoga_name': item[4],
            'uploaded_img': base64.b64encode(item[5]).decode('utf-8'),
            'corrected_img': base64.b64encode(item[6]).decode('utf-8'),
            'feedback': item[7],
            'date': item[8]
        })

    return render_template('dashboard.html', dashboard_data = dashboard_list)


@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

if __name__ == '__main__':
    app.run(debug = True)