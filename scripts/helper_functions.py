import glob
import os

import h5py
import numpy as np
from tqdm.auto import tqdm


def make_dir(target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
        print(f"Successfully created the directory {target_dir}")
    else:
        print(f"The directory {target_dir} is already present.")


def process_image_paths(SOURCE_DIR, TARGET_DIR, IMAGE_PATTERN):
    import re

    make_dir(TARGET_DIR)

    image_paths = glob.glob(os.path.join(SOURCE_DIR, "*", IMAGE_PATTERN))
    matches = []
    paths = []

    regex_list = [
        rf"{SOURCE_DIR}/ZStep_([0-9]+)/([0-9]+)-([A-Z0-9]+)-([0-9])-([0-9x]+)_([A-Z0-9]+)_s([0-9]+)_w([0-9]).TIF",
        rf"{SOURCE_DIR}/ZStep_([0-9]+)/([0-9]+)-([A-Z0-9]+)-([0-9])-([Plate0-9]+)-([0-9])-([0-9x]+)-([A-Z]+)_([A-Z0-9]+)_s([0-9]+)_w([0-9]).TIF",
        rf"{SOURCE_DIR}/ZStep_([0-9]+)/([0-9]+)-([A-Z0-9]+)-([0-9])-([0-9x]+)-([A-Z]+)-([A-Z0-9]+)_([A-Z0-9]+)_s([0-9]+)_w([0-9]).TIF",
    ]

    for regex in regex_list:
        IMAGE_REGEX = re.compile(regex)
        if IMAGE_REGEX.match(image_paths[0]):
            break

    for path in tqdm(image_paths):
        if match := IMAGE_REGEX.findall(path):
            matches.append(match[0])
            paths.append(path)

    matches = np.array(matches)

    return matches


def reduce_array(array):
    # Find unique rows in the array
    unique_rows = np.unique(array, axis=0)

    # Find columns that change in value
    changing_columns = np.where(np.any(unique_rows[:-1] != unique_rows[1:], axis=0))[0]

    return array[:, changing_columns]


def collect_data(source, WH):
    from preprocessing import preprocess_img

    return [preprocess_img(file, WH) for file in tqdm(source, total=len(source))]


def _viz_with_open3d(xyz, attrs, z_space):
    import open3d as o3d

    xyz = np.concatenate(xyz)
    attrs = np.concatenate(attrs, axis=1).transpose()

    # Create Open3D point cloud
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(xyz)
    # pcd.colors = o3d.utility.Vector3dVector(attrs[:, :3])

    # Set point size
    pcd.paint_uniform_color([0.2, 0.2, 0.2])
    pcd.scale(z_space / 2, center=(0, 0, 0))

    # Visualize the point cloud
    o3d.visualization.draw_geometries([pcd])


def _viz_with_pyvista(xyz, attrs, z_space):
    import pyvista as pv

    xyz = np.concatenate(xyz)
    attrs = np.concatenate(attrs, axis=1).transpose()

    # Create PyVista point cloud
    points = xyz[:, :3]
    point_cloud = pv.PolyData(points)
    point_cloud["attributes"] = attrs[:, :3]

    # Set point size
    point_cloud.point_size = z_space / 2

    # Visualize the point cloud
    point_cloud.plot()


def _viz_with_vtk(xyz, attrs, z_space):
    import vtk

    xyz = np.concatenate(xyz)
    attrs = np.concatenate(attrs, axis=1).transpose()

    # Create VTK point cloud
    points = vtk.vtkPoints()
    vertices = vtk.vtkCellArray()

    for point in xyz:
        ID = points.InsertNextPoint(point)
        vertices.InsertNextCell(1)
        vertices.InsertCellPoint(ID)

    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetVerts(vertices)

    # Create VTK mapper and actor
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(0.2, 0.2, 0.2)
    actor.SetScale(z_space / 2, z_space / 2, z_space / 2)

    # Create VTK renderer, render window, and interactor
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(1.0, 1.0, 1.0)

    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    # Visualize the point cloud
    render_window.Render()
    interactor.Start()


vis_tools = {"open3D": _viz_with_open3d, "pyvista": _viz_with_pyvista, "vtk": _viz_with_vtk}


def visualize_point_cloud(DATA, N=60000, thrs=None, z_space=1 / 500, vis_tool="open3D"):
    if thrs is None:
        thrs = [1000, 700, 1400, 700]

    D = DATA
    xyz = []
    attrs = []

    for i, ds in enumerate(D):
        xy_inds = np.argwhere((ds > np.array(thrs)[:, None, None]).sum(axis=0) > 0)
        inds = np.random.choice(len(xy_inds), size=min(N, len(xy_inds)), replace=False)
        xy = xy_inds[inds] / 2048

        attr = ds[:, xy_inds[:, 0], xy_inds[:, 1]]
        attr = attr[:, inds]

        xyz.append(np.hstack((xy, np.ones((len(xy), 1)) * i * z_space)))
        attrs.append(attr)

    if attrs:
        vis_tools.get(vis_tool)(xyz, attrs, z_space)
    else:
        print("No attributes available for visualization.")




