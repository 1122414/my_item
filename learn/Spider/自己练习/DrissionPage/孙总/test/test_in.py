import os

current_path = os.path.dirname(os.path.abspath(__file__))
if ('保研潜规则 #保研#考研#信息差'+'.mp4') in os.listdir(os.path.join(current_path,'../','video_data')):
  print('yes')