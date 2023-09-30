import pyvista as pv
import pandas as pd
import os
from .video import record_video

def plotting(csv_path,image_path,point_cloud,plotter,max,first = False, method = 'u'):
    data = pd.read_csv(csv_path)
    point_cloud.points = data[['x1', 'x2', method]].values
    point_cloud[method] = data[method].values
    delaunay = point_cloud.delaunay_2d()
    plotter.add_mesh(delaunay, color='blue', scalars=method, cmap='jet', clim=[0, max])
    if first:
        plotter.camera_position = 'xy'
        plotter.camera.roll=180
    plotter.screenshot(image_path)
    return image_path

# project_path = 'C:\\github_repositories\\julia\\JPBapp\\'+'/app/scripts/'

def max_value_u(project_path,method='u'):
    m = 0
    for i in range(0000,100001,1000):
        file_path = 'data/data.{}.csv'.format(i)
        # print(project_path + file_path)
        if os.path.isfile(os.path.join(project_path, file_path)):
            data = pd.read_csv(project_path + file_path)
            m = max(data[method].max(),m)
    return m

def generate(method):
    project_path = os.getcwd()+'/app/scripts/'
    plotter = pv.Plotter(off_screen=True)
    # plotter.open_movie(project_path + 'output_video.mp4')  

    point_cloud = pv.PolyData()
    frames=[]
    first = True
    t=5
    max_u = max_value_u(project_path,method = method)
    # for i in range(0000,100001,1000):
    for i in range(0000+10000*t,10001+10000*t,1000):
        file_path = 'data/data.{}.csv'.format(i)
        print(file_path)
        if os.path.isfile(os.path.join(project_path, file_path)):
            frames.append(plotting(project_path + file_path, project_path +'frames/frame_{}.jpeg'.format(i),point_cloud,plotter,max_u,first=first,method = method))
            first=False
    plotter.close()

    record_video(image_folder=os.getcwd()+'/app/scripts/frames/',fps=5,video_name=project_path + 'output_video_{}.mp4'.format(method),images=frames)
    return '/static/output_video_{}.mp4'.format(method)