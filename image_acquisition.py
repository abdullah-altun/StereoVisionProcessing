import pyzed.sl as sl
import numpy as np
import time
from image_saving import frameSave

def get_zed_resolution(resolution_str):
    resolution_map = {
        "HD2K": sl.RESOLUTION.HD2K,
        "HD1080": sl.RESOLUTION.HD1080,
        "HD720": sl.RESOLUTION.HD720,
        "VGA": sl.RESOLUTION.VGA
    }
    return resolution_map.get(resolution_str, sl.RESOLUTION.HD2K)

def cameraRead(args):
    zed = sl.Camera()

    init_params = sl.InitParameters()
    init_params.camera_resolution = get_zed_resolution(args.video_resolution)
    init_params.camera_fps = 30

    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print(f"Kamerayı başlatma hatası: {err}")
        exit(-1)

    left_image = sl.Mat()
    right_image = sl.Mat()

    start_time = time.time()

    outLeft = None
    outRigth = None

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        if zed.grab() == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_image(left_image, sl.VIEW.LEFT)
            zed.retrieve_image(right_image, sl.VIEW.RIGHT)
            left_frame = left_image.get_data()
            right_frame = right_image.get_data()

            if (args.frame_save)|(args.video_save):
                outLeft,outRigth = frameSave(args,left_frame[:,:,:-1],right_frame[:,:,:-1],outLeft,outRigth)
                if elapsed_time >= args.save_time:
                    print("Süre doldu, fonksiyon çalışmayı durdurdu.")
                    if args.video_save:
                        outLeft.release()
                        outRigth.release()
                    break
                    