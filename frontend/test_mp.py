import mediapipe
print("mediapipe version:", mediapipe.__version__)
try:
    from mediapipe import solutions
    print("OK: from mediapipe import solutions")
    print("solutions.pose:", solutions.pose)
except Exception as e:
    print("ERROR importing solutions:", e)

try:
    import mediapipe.solutions.pose as pose
    print("OK: import mediapipe.solutions.pose works")
except Exception as e:
    print("ERROR importing mediapipe.solutions.pose:", e)
