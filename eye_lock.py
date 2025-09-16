
import mediapipe as mp
import cv2
import numpy as np
import os
import shutil
import subprocess
import uuid



model_path = "./face_landmarker_v2_with_blendshapes.task"

BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.IMAGE,
    num_faces=3
)
landmarker = FaceLandmarker.create_from_options(options)


def align_to_fixed_eyes(image, lm, ref_left_eye, ref_right_eye, canvas_size=1024):
    """Align a face to fixed eye positions on a canvas."""
    h, w, _ = image.shape

    # Current eyes
    left_eye = np.array([lm[468].x * w, lm[468].y * h])
    right_eye = np.array([lm[473].x * w, lm[473].y * h])

    # Compute rotation
    dx = right_eye[0] - left_eye[0]
    dy = right_eye[1] - left_eye[1]
    angle = np.degrees(np.arctan2(dy, dx))

    # Compute scale to match reference eye distance
    eye_dist = np.linalg.norm(right_eye - left_eye)
    ref_eye_dist = np.linalg.norm(np.array(ref_right_eye) - np.array(ref_left_eye))
    scale = ref_eye_dist / eye_dist

    # Midpoints
    eye_center = (left_eye + right_eye) / 2
    ref_center = (np.array(ref_left_eye) + np.array(ref_right_eye)) / 2

    # Transformation: rotate + scale + translate
    M = cv2.getRotationMatrix2D(tuple(eye_center), angle, scale)
    M[0,2] += (ref_center[0] - eye_center[0])
    M[1,2] += (ref_center[1] - eye_center[1])

    # Optional: place on large canvas
    offset_x = canvas_size//2 - int(ref_center[0])
    offset_y = canvas_size//2 - int(ref_center[1])
    M[0,2] += offset_x
    M[1,2] += offset_y

    aligned = cv2.warpAffine(image, M, (canvas_size, canvas_size), flags=cv2.INTER_CUBIC)
    return aligned


def process_images_fixed_eyes(files, output_folder="./aligned_fixed_eyes", canvas_size=1024):
    """Process a list of image files and align faces with fixed eyes."""
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder, exist_ok=True)
    
    ref_left_eye, ref_right_eye = None, None

    for idx, in_path in enumerate(files):
        image = cv2.imread(in_path)
        if image is None:
            continue

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
        result = landmarker.detect(mp_image)

        # Skip if no face or multiple faces
        if not result.face_landmarks:
            continue
        if len(result.face_landmarks) > 1:
            continue

        lm = result.face_landmarks[0]

        # First frame: define reference eyes
        if ref_left_eye is None or ref_right_eye is None:
            h, w, _ = image.shape
            ref_left_eye = (int(lm[468].x * w), int(lm[468].y * h))
            ref_right_eye = (int(lm[473].x * w), int(lm[473].y * h))

        aligned = align_to_fixed_eyes(image, lm, ref_left_eye, ref_right_eye, canvas_size)

        out_path = os.path.join(output_folder, f"{idx:04d}.png")
        cv2.imwrite(out_path, aligned)

import os
import uuid
import subprocess

def create_timelapse(input_folder="./aligned_fixed_eyes", output_folder="./download", fps_in=10, fps_out=30):
    """
    Create a timelapse video using FFmpeg and a file list (handles missing numbers)
    Output is hidden unless FFmpeg fails.
    """
    os.makedirs(output_folder, exist_ok=True)

    # Get all image files sorted
    images = sorted([
        f for f in os.listdir(input_folder)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ])

    if not images:
        print("No images found in folder:", input_folder)
        return None

    # Create temporary file list for FFmpeg
    file_list_path = "./file_list.txt"
    with open(file_list_path, "w") as f:
        for img in images:
            f.write(f"file '{os.path.join(input_folder, img)}'\n")

    random_str = str(uuid.uuid4())[:6]
    output_path = os.path.join(output_folder, f"{random_str}.mp4")

    # FFmpeg command using file list
    command = [
        "ffmpeg",
        "-y",
        "-r", str(fps_in),          # input frame rate
        "-f", "concat",
        "-safe", "0",
        "-i", file_list_path,
        "-c:v", "libx264",
        "-r", str(fps_out),         # output frame rate
        "-pix_fmt", "yuv420p",
        output_path
    ]

    # Run FFmpeg, hide output
    result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(file_list_path)  # clean up

    if result.returncode == 0:
        return output_path
    else:
        print("FFmpeg failed. Command was:")
        print(" ".join(command))
        return None


def EyeLock_Timelapse(selfies_folder, aligned_folder="./aligned_fixed_eyes", output_folder="./download",image_duraion=0.1):
    """Wrapper: process selfies from a folder and create a timelapse."""
    files = sorted([
        os.path.join(selfies_folder, f)
        for f in os.listdir(selfies_folder)
        if f.lower().endswith((".jpg", ".png", ".jpeg"))
    ])
    process_images_fixed_eyes(files, aligned_folder, canvas_size=1024)
    output_video = create_timelapse(aligned_folder, output_folder,fps_in=image_duraion*100)
    print("Final video:", output_video)
    return output_video


# if __name__ == "__main__":
#     timelapse_video = EyeLock_Timelapse("./selfies")
#     print("Timelapse video saved at:", timelapse_video)
