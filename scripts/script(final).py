import pyvista as pv
import pandas as pd
import os
import video

project_path = 'C:/github_repositories/julia/'

# plotter = pv.Plotter()
plotter = pv.Plotter(off_screen=True)
plotter.open_movie(project_path + 'output_video22.mp4')  

point_cloud = pv.PolyData()

def plotting(csv_path,image_path,first = False):
    data = pd.read_csv(csv_path)
    # point_cloud = pv.PolyData()
    point_cloud.points = data[['x1', 'x2', 'u']].values
    point_cloud['u'] = data['u'].values
    delaunay = point_cloud.delaunay_2d()
    plotter.add_mesh(delaunay, color='blue', scalars='u', cmap='jet', clim=[0, 0.0006])
    if first:
        plotter.camera_position = 'xy'
        plotter.camera.roll=180
    # plotter.write_frame()
    # plotter.show()
    plotter.screenshot(image_path)
    return image_path

frames=[]
# plotting(project_path + 'data/data.{}.csv'.format(100000), project_path +'frames2/frame_{}.jpeg'.format(100000),first=True)
first = True
for i in range(0000,100001,1000):
# for i in range(0000+10000*t,10001+10000*t,1000):
    file_path = 'data/data.{}.csv'.format(i)
    print(file_path)
    if os.path.isfile(os.path.join(project_path, file_path)):
        # frames.append(plotting(project_path + file_path, project_path +'frames2/frame_{}.jpeg'.format(i)))
        frames.append(plotting(project_path + file_path, project_path +'frames2/frame_{}.jpeg'.format(i),first=first))
        first=False

plotter.close()
# output_video_file = "output_video22.mp4"
# plotter.write_video(output_video_file, fps=10)

video.record_video(image_folder='C:/github_repositories/julia/frames2/',fps=5,video_name='output_video2.mp4',images=frames)