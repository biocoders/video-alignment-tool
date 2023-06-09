import cv2
import matplotlib.pyplot as plt
import numpy as np

class VideoAlignment:

    fileName = ""
    startFrame = 0
    endFrame = -1
    error = ""
    width = 600
    height = 200
    cap = None


    def __init__(self, filename, startframe = 0, endframe = -1):
        self.fileName = filename
        self.startFrame = startframe
        self.endFrame = endframe
        return
    
    def SetDimensions(self, width, height):
        self.width = width
        self.height = height

    def DisplayFrame(self, frameNumber):
        self.cap = cv2.VideoCapture(self.fileName)
        cap = self.cap
        if not self.cap.isOpened():
            self.error = "File not exists"
            return
        numOfFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if frameNumber >= numOfFrames - 1:
            frameNumber = numOfFrames - 1
        cap.set(cv2.CAP_PROP_POS_FRAMES, frameNumber) 
        ret, frame = cap.read()
        if not ret:
            self.error = "File not read"
            return
        frame = np.flip(frame, axis=2)
        plt.imshow(frame)

    def TransformVideo(self, registration_points):
        if self.cap == None:
            self.cap = cv2.VideoCapture(self.fileName)
        cap = self.cap
        if not cap.isOpened():
            self.error = "File not exists"
            return

        schema = np.array([
            [0, 0],
            [self.width, 0],
            [self.width, self.height],
            [0, self.height]
        ])

        src = registration_points.astype(np.float32)
        target = schema.astype(np.float32)
        M = cv2.getPerspectiveTransform(src, target)

        numOfFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if self.endFrame < 0 or self.endFrame >= numOfFrames - 1:
            self.endFrame = numOfFrames - 1
        cap.set(cv2.CAP_PROP_POS_FRAMES, self.startFrame) 

        images = []
        for i in range(self.endFrame - self.startFrame + 1):
            ret, frame = cap.read()
            if not ret:
                self.error = "Error in reading frame "+ i + self.startFrame
                return
            frame = np.flip(frame, axis=2)
            transformed_image = cv2.warpPerspective(frame, M, dsize=(self.width, self.height))
            images.append(transformed_image)

        frame_rate = cap.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('transformed.mp4', fourcc, frame_rate, (self.width, self.height))
 
        for i in range(len(images)):
            out.write(images[i])
        out.release()

    

