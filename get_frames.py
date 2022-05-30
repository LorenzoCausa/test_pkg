import cv2
import os
import sys

video_name_ext='DJI_0018.MOV'
video_name='DJI_0018'
vidcap = cv2.VideoCapture(video_name_ext)
count = 0
success,image = vidcap.read()
while success:
  success,image = vidcap.read()
  my_video_name= video_name+"_frame%d.jpg" % count
  frame_name=os.path.join("frames",my_video_name)
  #print(frame_name)
  cv2.imwrite(frame_name, image)     # save frame as JPEG file       
  print('Read a new frame: ', count,success)
  vidcap.set(cv2.CAP_PROP_POS_MSEC, count);
  count += 2000
