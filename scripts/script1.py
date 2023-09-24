import pyvista as pv
import pandas as pd
import os
import video 

project_path = 'C:/github_repositories/medicine/julia/'

def plotting(csv_path,image_path):
    data = pd.read_csv(csv_path)
    plotter = pv.Plotter(off_screen=True)
    point_cloud = pv.PolyData()
    point_cloud.points = data[['x1', 'x2', 'u']].values
    point_cloud['u'] = data['u'].values
    delaunay = point_cloud.delaunay_2d()
    plotter.add_mesh(delaunay, scalars='u', cmap='jet')
    plotter.camera_position = 'xy'
    plotter.camera.roll=180
    plotter.show(screenshot=image_path)
    return image_path

frames=[]

t = 5
for i in range(0000,100001,1000):
# for i in range(0000+10000*t,10001+10000*t,1000):
    csv_path = project_path + 'data/data.{}.csv'.format(i)
    img_path = project_path + 'frames/frame_{}.jpeg'.format(i)
    print(csv_path)
    frames.append(plotting(csv_path, img_path))

video.record_video(image_folder = project_path + 'frames/', fps=10, video_name = project_path + 'output_video1.mp4', images = frames)