import pyvista as pv
import pandas as pd
import os
from .video import record_video
from datetime import datetime

def plotting(csv_path,image_path,point_cloud,plotter,max=0.001,first = False, method = 'u'):
    data = pd.read_csv(csv_path)
    point_cloud.points = data[['x1', 'x2', method]].values
    point_cloud[method] = data[method].values
    delaunay = point_cloud.delaunay_2d()
    plotter.clear()
    plotter.add_mesh(delaunay,  scalars=method, cmap='jet', clim=[0, max])
    if first:
        plotter.camera_position = 'xy'
        plotter.camera.roll=180
    text_position = (0.0, 0.0, 62.0)
    text = 't = ' + csv_path.split('.')[-2]
    plotter.add_text(text, position=text_position, font_size=20, color='black')
    plotter.screenshot(image_path)
    return image_path

# project_path = 'C:\\github_repositories\\julia\\JPBapp\\'+'/app/scripts/'

def max_value_u(project_path,method='u'):
    m = 0
    for i in range(0000,100001,1000):
        file_path = '/data/data.{}.csv'.format(i)
        # print(project_path + file_path)
        # if os.path.isfile(os.path.join(project_path, file_path)):
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
    t=8
    max_u = max_value_u(project_path,method = method)
    print(max_u)
    # for i in range(0000,100001,1000):
    for i in range(0000+10000*t,10001+10000*t,1000):
        file_path = 'data/data.{}.csv'.format(i)
        print(file_path)
        if os.path.isfile(os.path.join(project_path, file_path)):
            frames.append(plotting(project_path + file_path, project_path +'frames_{0}/frame_{1}.jpeg'.format(method, i),point_cloud,plotter,max_u,first=first,method = method))
            first=False
    plotter.close()

    now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    
    record_video(image_folder=os.getcwd()+'/app/scripts/frames_{0}/'.format(method),fps=5,video_name=project_path + '/video_{0}/output_video_{0}({1}).mp4'.format(method,now),images=frames)
    return 'static/scripts/video_{0}/output_video_{0}({1}).mp4'.format(method,now)