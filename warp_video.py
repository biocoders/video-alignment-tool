import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
from tqdm import tqdm


os.chdir("/Users/matthieuvilain/Desktop/video-alignment-tool")

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
fps= float(cap.get(cv2.CAP_PROP_FPS))

transformation = cv2.getPerspectiveTransform(src, target)


total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


export_video = cv2.VideoWriter('demo_transfomed.mp4', 
                         cv2.VideoWriter_fourcc(*'MP4V'),
                         fps, (width,height))


for _ in tqdm(range(total_frames)):
    
    #cap.set(cv2.CAP_PROP_POS_FRAMES, 1)
    ret, frame = cap.read()
    
    export_video.write( cv2.warpPerspective(frame, transformation, dsize=(width, height)) )
    

cap.release()
export_video.release()