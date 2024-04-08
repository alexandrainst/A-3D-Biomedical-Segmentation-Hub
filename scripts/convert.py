import h5py
import numpy as np
from vtk import vtkFloatArray, vtkImageData, vtkXMLImageDataWriter


def numpy_to_vtk_and_save(numpy_array, output_file):
    vtk_image_data = vtkImageData()
    vtk_image_data.SetDimensions(numpy_array.shape)
    vtk_image_data.SetSpacing(1.0, 1.0, 1.0)
    vtk_image_data.SetOrigin(0.0, 0.0, 0.0)

    # Flatten the volume data and set it to the VTK image
    vtk_data_array = vtkFloatArray()
    vtk_data_array.SetNumberOfComponents(1)
    vtk_data_array.SetNumberOfTuples(numpy_array.size)
    vtk_data_array.SetVoidArray(numpy_array.flatten(), numpy_array.size, 1)

    vtk_image_data.GetPointData().SetScalars(vtk_data_array)

    # Save the VTK file with compression
    writer = vtkXMLImageDataWriter()
    writer.SetFileName(output_file)
    writer.SetCompressorTypeToZLib()  # Use zlib compression
    writer.SetInputData(vtk_image_data)
    writer.Write()


def hdf5_to_vtk_and_save(hdf5_file_path, output_file):
    with h5py.File(hdf5_file_path, "r") as h5_file:
        numpy_array = h5_file["volume_dataset"][:]  # Adjust the dataset name as needed

    numpy_to_vtk_and_save(numpy_array, output_file)


if __name__ == "__main__":
    # hdf5_file_path = "../data/aske/wup1/preprocessed_data/preprocessed_data.hdf5"
    # output_file = "output_volume_from_hdf5.vtk"
    # hdf5_to_vtk_and_save(hdf5_file_path, output_file)

    data_array = np.random.rand(3, 4, 3)
    output_file = "output_volume_compressed.vtk"
    numpy_to_vtk_and_save(data_array, output_file)
