import cv2
import matplotlib.pyplot as plt
import numpy as np


width = 600 # in mm
height = 200 # in mm

schema = np.array([
    [0, 0],
    [width, 0],
    [width, height],
    [0, height]
])

registration_points = np.array([
    [550, 450],
    [1500, 400],
    [1500, 690],
    [550, 750]
])


src = registration_points.astype(np.float32)
target = schema.astype(np.float32)


cap = cv2.VideoCapture("/Users/matthieuvilain/Desktop/video-alignment-tool/demo.mp4")

transformation = cv2.getPerspectiveTransform(src, target)


total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


export_video = cv2.VideoWriter('demo_transfomed.mp4', 
                         cv2.VideoWriter_fourcc(*'MP4V'),
                         30, (width,height))

for _ in range(total_frames):
    
    #cap.set(cv2.CAP_PROP_POS_FRAMES, 1)
    ret, frame = cap.read()
    
    export_video.write( cv2.warpPerspective(frame, transformation, dsize=(width, height)) )
    

cap.release()
export_video.release()