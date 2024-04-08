import logging
from os import PathLike
from pathlib import Path
from typing import Dict, Tuple, Union

import cv2
import tifffile as tiff
from helper_functions import collect_data, h5py_load, h5py_save
from matplotlib import pyplot as plt
from numpy import asarray, ndarray, uint8
from tqdm import tqdm

# Constants
DATASET_PATHS = {
    "WUP1": "HA1100_1.712um_WUP1_bulk_b__pag-0.49_0.30_",
    "WUP2": "HA1100_1.712um_WUP2_outer-edge_pag-0.39_0.41_",
    "WUP3": "HA1100_1.712um_WUP3_inner-edge_pag-0.48_0.55_",
}

BASE_DIR = "/media/davidparham/Elements/ESRF_BM18/PROCESSED_DATA/"
DATA_PATH_TEMPLATE_1 = "../data/aske/{}/preprocessed_data/preprocessed_data.hdf5"
DATA_PATH_TEMPLATE_2 = "../data/aske/{}/preprocessed_data/preprocessed_data.tif"
PARENT_DIR = "../data/aske/"

# Set up logging
logging.basicConfig(level=logging.INFO)


def create_folder_structure(base_folder: str | PathLike) -> None:
    """Create the folder structure for the given base folder.

    :param base_folder: The base folder to create the structure for.
    :return: None
    """

    # Check if the main folder exists
    if not base_folder.exists():
        base_folder.mkdir(parents=True)
        logging.info(f"Created base folder: {base_folder}")

    # Check and create subfolders
    subfolders = ["csv_files", "preprocessed_data"]
    for subfolder in subfolders:
        subfolder_path = base_folder / subfolder
        if not subfolder_path.exists():
            subfolder_path.mkdir()
            logging.info(f"Created subfolder: {subfolder_path}")


def initialize_dataset(
    path: str, name: str, length: int | None = None, width: None = None, save: bool = False
) -> ndarray:
    """Load or create and save a lightly preprocessed dataset.

    :param path: The file path for the dataset.
    :param name: The name of the dataset.
    :param length: The number of images to include in the dataset. Defaults to None.
    :param width: The width of the images. Defaults to None.
    :param save: Whether to save the dataset or not. Defaults to False.
    :return: The loaded or newly created dataset.
    """

    create_folder_structure(Path(path).parent.parent)

    if Path(path).exists():
        return h5py_load(path)

    dataset_source_dir = Path(BASE_DIR) / DATASET_PATHS.get(name)
    image_paths = sorted([str(file) for file in dataset_source_dir.glob("*.tif")])

    wh = width or cv2.imread(image_paths[0], cv2.IMREAD_UNCHANGED).shape[0]

    selected_image_paths = image_paths[:length] if length is not None else image_paths

    data = asarray(collect_data(selected_image_paths, wh))

    if save:
        h5py_save(path, data)

    return data


def tiffstack(path: str, name: str, length: int | None = None, width: None = None, save: bool = False) -> ndarray:
    """Load or create and save a lightly preprocessed dataset.

    :param path: The file path for the dataset.
    :param name: The name of the dataset.
    :param length: The number of images to include in the dataset. Defaults to None.
    :param width: The width of the images. Defaults to None.
    :param save: Whether to save the dataset or not. Defaults to False.
    :return: The loaded or newly created dataset.
    """

    create_folder_structure(Path(path).parent.parent)

    if Path(path).exists():
        return tiff.imread(path)

    dataset_source_dir = Path(BASE_DIR) / DATASET_PATHS.get(name)
    tiff_stack = []

    for image_path in tqdm(sorted(dataset_source_dir.glob("*.tif"))[:length]):
        img = tiff.imread(image_path)

        # Check dtype and convert to uint8 if not already
        if img.dtype != uint8:
            img = (img / img.max() * 255).astype(uint8)

        wh = width or img.shape[0]
        resized_img = cv2.resize(img, (wh, wh))
        tiff_stack.append(resized_img)

    tiff_stack = asarray(tiff_stack)
    if save:
        # Save as a 3D TIFF stack
        tiff.imwrite(path, tiff_stack, bigtiff=True, volumetric=True)

    return tiff_stack


def visualize_first_slice(tiff_stack: ndarray) -> None:
    plt.imshow(tiff_stack[0], cmap="gray")
    plt.title("First Slice of TIFF Stack")
    plt.show()


def update_slice_stats(
    slice_stats: Dict[str, dict],
    num_labels: int,
    stats: ndarray,
    center_x: int,
    center_y: int,
    centroids: ndarray,
) -> Tuple[Dict[str, dict], int, int, int]:
    """Update the statistics of each slice based on the connected components.

    :param slice_stats: Dictionary containing the statistics of each slice.
    :param num_labels: Number of connected components in the image.
    :param stats: Array containing the statistics of each connected component.
    :param center_x: X-coordinate of the center of the image.
    :param center_y: Y-coordinate of the center of the image.
    :param centroids: Array containing the centroids of each connected component.
    :return: Updated slice_stats dictionary, total_areas, max_area, and min_area.
    """

    total_areas = 0
    min_area, max_area = float("inf"), 0

    for i in range(1, num_labels):
        width, height = stats[i, cv2.CC_STAT_WIDTH], stats[i, cv2.CC_STAT_HEIGHT]
        area = stats[i, cv2.CC_STAT_AREA]
        total_areas += area
        max_area = max(max_area, area)
        min_area = min(min_area, area)

        (cX, cY) = centroids[i]
        centroid_key = f"{int(cX)}-{int(cY)}"
        dispersion = ((cX - center_x) ** 2 + (cY - center_y) ** 2) ** 0.5

        if centroid_key not in slice_stats:
            slice_stats[centroid_key] = {"area": [], "aspect_ratio": [], "dispersion": [], "depth": 0}

        slice_stats[centroid_key]["area"].append(area)
        slice_stats[centroid_key]["aspect_ratio"].append(round((height / width), 4))
        slice_stats[centroid_key]["dispersion"].append(round(dispersion, 4))
        slice_stats[centroid_key]["depth"] += 1

    return slice_stats, total_areas, max_area, min_area


def update_volume_stats(
    volume_stats: Dict[str, Union[int, float]],
    num_labels: int,
    min_area: int,
    max_area: int,
    volume_black_pixel_count: int,
    areas: list[int],
) -> Dict[str, Union[int, float]]:
    """Update the volume statistics based on the connected components.

    :param volume_stats: Dictionary containing the volume statistics.
    :param num_labels: Number of connected components in the image.
    :param min_area: Minimum area of a connected component.
    :param max_area: Maximum area of a connected component.
    :param volume_black_pixel_count: Total volume of the image.
    :param areas: List of areas of each connected component.
    :return: Updated volume_stats dictionary.
    """

    volume_stats["min_air_pockets"] = min(num_labels, volume_stats["min_air_pockets"])
    volume_stats["max_air_pockets"] = max(num_labels, volume_stats["max_air_pockets"])
    volume_stats["min_air_pocket_size"] = min(min_area, volume_stats["min_air_pocket_size"])
    volume_stats["max_air_pocket_size"] = max(max_area, volume_stats["max_air_pocket_size"])
    volume_stats["min_black_pixel_count"] = min(volume_black_pixel_count, volume_stats["min_black_pixel_count"])
    volume_stats["max_black_pixel_count"] = max(volume_black_pixel_count, volume_stats["max_black_pixel_count"])
    volume_stats["min_air_pocket_percentage"] = min(
        (areas * 100 / volume_black_pixel_count), volume_stats["min_air_pocket_percentage"]
    )
    volume_stats["max_air_pocket_percentage"] = max(
        (areas * 100 / volume_black_pixel_count), volume_stats["max_air_pocket_percentage"]
    )

    return volume_stats


if __name__ == "__main__":
    target_dataset = "WUP2"
    # dataset_path = DATA_PATH_TEMPLATE_1.format(target_dataset.lower())
    # loaded_data = initialize_dataset(dataset_path, target_dataset, 10)
    # print(type(loaded_data), len(loaded_data), loaded_data)
    dataset_path = DATA_PATH_TEMPLATE_2.format(target_dataset.lower())
    tiff_stack = tiffstack(dataset_path, target_dataset, width=1028, save=True)

    visualize_first_slice(tiff_stack)
