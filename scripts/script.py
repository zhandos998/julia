import pyvista as pv
import pandas as pd
import numpy as np
import os

dir_path = 'C:\\Users\\zhandos998\\Desktop\\julia\\data\\'
filenames = []

plotter = pv.Plotter()
plotter.open_movie('movie.mp4')  
# Создание объекта PyVista
point_cloud = pv.PolyData()

# for i in range(0,100001,1000):
for i in range(0,10001,1000):
    # check if current file_path is a file
    file_path = 'data.{}.csv'.format(i)
    # print(file_path)
    if os.path.isfile(os.path.join(dir_path, file_path)):
        # Загрузка CSV-файла
        data = pd.read_csv('C:\\Users\\zhandos998\\Desktop\\julia\\data\\' + file_path)
        print(file_path)

        # Установка координатных данных
        point_cloud.points = data[['x1', 'x2', 'u']].values
        point_cloud['u'] = data['u'].values

        delaunay = point_cloud.delaunay_2d()

        plotter.add_mesh(delaunay, color='blue', scalars='u', cmap='jet')

        plotter.camera_position = 'xy'
        plotter.camera.roll=180
        for _ in range(10):
            plotter.write_frame()  
        # pv.plot(record='movie.mp4', off_screen=True, window_size=(800, 600), interactive=False, fps=fps)

        # plotter.show()

# output_video_file = "output_video.mp4"

# # Define the frame rate (fps)
# fps = 10

# # Render the scene as an MP4 video
# pv.plot(record=output_video_file, off_screen=True, window_size=(800, 600), interactive=False, fps=fps)

plotter.close()