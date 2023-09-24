import pyvista as pv
import pandas as pd
import os
import video 

project_path = 'C:/github_repositories/medicine/julia/'

plotter = pv.Plotter()
# plotter = pv.Plotter(off_screen=True)
def plotting(csv_path,image_path,first = False):
    data = pd.read_csv(csv_path)
    point_cloud = pv.PolyData()
    point_cloud.points = data[['x1', 'x2', 'u']].values
    point_cloud['u'] = data['u'].values
    delaunay = point_cloud.delaunay_2d()
    plotter.add_mesh(delaunay, scalars='u', cmap='jet')
    # if first:
    plotter.camera_position = 'xy'
    plotter.camera.roll=180
    plotter.show(auto_close=False, interactive=False,screenshot=image_path)
    return image_path

# plotting(project_path+'data/data.0.csv',project_path+'frames2/frame_0.jpeg',True)
frames=[]

t = 0
# for i in range(0000,100001,1000):
for i in range(0000+10000*t,10001+10000*t,1000):
    file_path = 'data/data.{}.csv'.format(i)
    print(file_path)
    if os.path.isfile(os.path.join(project_path, file_path)):
        frames.append(plotting(project_path + file_path, project_path +'frames2/frame_{}.jpeg'.format(i)))        

video.record_video(image_folder='C:/github_repositories/medicine/julia/frames2/',fps=5,video_name='output_video2.mp4',images=frames)