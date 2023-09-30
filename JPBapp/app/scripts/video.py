import cv2
import os

# image_folder = 'C:/github_repositories/medicine/julia/frames/'
# video_name = 'output_video1.mp4'
# images = ['frame_{}.jpeg'.format(i) for i in range(0000,100001,1000)]
# fps = 10

def record_video(image_folder,video_name,images,fps):
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    video = cv2.VideoWriter(video_name, 0, fps, (width,height))
    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))
    cv2.destroyAllWindows()
    video.release()

if __name__ == "__main__":
    pass