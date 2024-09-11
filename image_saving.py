import os
import cv2

from datetime import datetime
import time 

def get_resolution_dimensions(resolution_str):
    resolution_dimensions = {
        "HD2K": (2208, 1242),
        "HD1080": (1920, 1080),
        "HD720": (1280, 720),
        "VGA": (672, 376)
    }
    return resolution_dimensions.get(resolution_str, (2208, 1242))

current_date = datetime.now()
day = current_date.day
month = current_date.month
year = current_date.year

start_time = time.time()


def folderCrate(args):
    if not(os.path.exists("output")):
        os.mkdir("output")
    if not(os.path.exists("output/camera")):
        os.mkdir("output/camera")
    if not(os.path.exists(f"output/camera/{day}-{month}-{year}")):
        os.mkdir(f"output/camera/{day}-{month}-{year}")

    if args.frame_save:
        if not(os.path.exists(f"output/camera/{day}-{month}-{year}/leftImages")):
            os.mkdir(f"output/camera/{day}-{month}-{year}/leftImages")
        if not(os.path.exists(f"output/camera/{day}-{month}-{year}/rightImages")):
            os.mkdir(f"output/camera/{day}-{month}-{year}/rightImages")

    if args.video_save:    
        frame_size = get_resolution_dimensions(args.video_resolution)
        outLeft = cv2.VideoWriter(f"output/camera/{day}-{month}-{year}/leftCamera.mp4",
                             cv2.VideoWriter_fourcc(*'XVID'),args.frame_rate,frame_size)
        outRight = cv2.VideoWriter(f"output/camera/{day}-{month}-{year}/rightCamera.mp4",
                             cv2.VideoWriter_fourcc(*'XVID'),args.frame_rate,frame_size)
    else:
        outLeft = 1
        outRight = 1

    return outLeft,outRight
    

def frameSave(args,leftImage,rightImage,outLeft=None,outRight=None):
    global start_time
    if outLeft==None and outRight==None:
        outLeft,outRight = folderCrate(args)

    if args.frame_save:
        elapsed_time = time.time() - start_time
        if elapsed_time > args.frame_time:
            save_id = len(os.listdir(f"output/camera/{day}-{month}-{year}/leftImages"))+1
            cv2.imwrite(f"output/camera/{day}-{month}-{year}/leftImages/{save_id}.jpg",leftImage)
            cv2.imwrite(f"output/camera/{day}-{month}-{year}/rightImages/{save_id}.jpg",rightImage)
            start_time = time.time()

    if args.video_save:
        outLeft.write(leftImage)
        outRight.write(rightImage)
    
    return outLeft,outRight
    


