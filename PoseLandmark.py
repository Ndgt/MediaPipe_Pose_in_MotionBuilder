from pyfbsdk import *
import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# For static images:
IMAGE_FILES = []
BG_COLOR = (192, 192, 192) # gray
with mp_pose.Pose(
    static_image_mode=True,
    model_complexity=2,
    enable_segmentation=True,
    min_detection_confidence=0.5) as pose:
  for idx, file in enumerate(IMAGE_FILES):
    image = cv2.imread(file)
    image_height, image_width, _ = image.shape
    # Convert the BGR image to RGB before processing.
    results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    if not results.pose_landmarks:
      continue
    print(
        f'Nose coordinates: ('
        f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * image_width}, '
        f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * image_height})'
    )

    annotated_image = image.copy()
    # Draw segmentation on the image.
    # To improve segmentation around boundaries, consider applying a joint
    # bilateral filter to "results.segmentation_mask" with "image".
    condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
    bg_image = np.zeros(image.shape, dtype=np.uint8)
    bg_image[:] = BG_COLOR
    annotated_image = np.where(condition, annotated_image, bg_image)
    # Draw pose landmarks on the image.
    mp_drawing.draw_landmarks(
        annotated_image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)
    # Plot pose world landmarks.
    mp_drawing.plot_landmarks(
        results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

# For webcam input:
cap = cv2.VideoCapture(0)

# Create list of each　element
mark = [0]*33
xPos = [0]*33
yPos = [0]*33
zPos = [0]*33

# create marker in MotionBuilder 
mark[0] = FBModelMarker("marker0")
mark[0].Show = True
mark[0].Scaling = FBVector3d(2,2,2)

for i in range(11,17):
  mark[i] = FBModelMarker("marker%d"%(i))
  mark[i].Show = True
  mark[i].Scaling = FBVector3d(2,2,2)

for j in range(23,29):
  mark[j] = FBModelMarker("marker%d"%(j))
  mark[j].Show = True
  mark[j].Scaling = FBVector3d(2,2,2)

for j in range(31,33):
  mark[j] = FBModelMarker("marker%d"%(j))
  mark[j].Show = True
  mark[j].Scaling = FBVector3d(2,2,2)

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    #get Landmarks'position and expand them
    xPos[0] = -180*(results.pose_landmarks.landmark[0].x)
    yPos[0] = -180*(results.pose_landmarks.landmark[0].y)
    zPos[0] = results.pose_landmarks.landmark[0].z

    for i in range(11,17):
      xPos[i] = -180*(results.pose_landmarks.landmark[i].x)
      yPos[i] = -180*(results.pose_landmarks.landmark[i].y)
      zPos[i] = results.pose_landmarks.landmark[i].z

    for j in range(23,29):
      xPos[j] = -180*(results.pose_landmarks.landmark[j].x)
      yPos[j] = -180*(results.pose_landmarks.landmark[j].y)
      zPos[j] = results.pose_landmarks.landmark[j].z

    for j in range(31,33):
      xPos[j] = -180*(results.pose_landmarks.landmark[j].x)
      yPos[j] = -180*(results.pose_landmarks.landmark[j].y)
      zPos[j] = results.pose_landmarks.landmark[j].z

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
      
    # apply Nose's position to marker's position
    mark[0].Translation = FBVector3d(xPos[0], yPos[0], zPos[0])
    for i in range(11,17):
      mark[i].Translation = FBVector3d(xPos[i], yPos[i], zPos[i])  
    for j in range(23,29):
      mark[j].Translation = FBVector3d(xPos[j], yPos[j], zPos[j])  
    for j in range(31,33):
      mark[j].Translation = FBVector3d(xPos[j], yPos[j], zPos[j])  
    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))

    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()