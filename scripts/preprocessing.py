import cv2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from scipy import ndimage as ndi
from skimage import measure
from skimage.feature import peak_local_max
from skimage.filters import rank, threshold_otsu
from skimage.morphology import disk
from skimage.segmentation import watershed


def preprocess_img(img_path_or_array: str | np.ndarray, target_size: int) -> np.ndarray:
    """Preprocesses an image by resizing it to a square shape and converting it to grayscale format.

    :param img_path_or_array: The path to the image file or a NumPy array.
    :param target_size: The desired width and height for the image.

    :return: The preprocessed grayscale image.
    """
    if isinstance(img_path_or_array, str):
        img = cv2.imread(img_path_or_array, cv2.IMREAD_GRAYSCALE)
    elif isinstance(img_path_or_array, np.ndarray):
        img = img_path_or_array
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        raise TypeError("img_path_or_array must be a string or a NumPy array")

    target_size = abs(target_size)
    if img.shape[0] != target_size:
        img = cv2.resize(img, (target_size, target_size), interpolation=cv2.INTER_AREA)

    return img


def create_plot(img_gray, thresh):
    _, ax = plt.subplots(nrows=1, ncols=2, figsize=(10, 10))
    ax[0].imshow(img_gray, cmap="gray")
    ax[0].set_title("Original Image")
    ax[1].imshow(thresh, cmap="gray")
    ax[1].set_title("Thresholded Image")
    plt.show()


def simple_thresholding(img_gray: np.ndarray, thresh_value: int = 127, plot: bool = False) -> np.ndarray:
    """Applies Simple thresholding to an input grayscale image and optionally plots the original and thresholded images.

    :param img_gray: The input grayscale image.
    :param background: Background value to be subtracted from the image before thresholding (default is 0).
    :param plot: If True, the original and thresholded images will be displayed using matplotlib (default is False).

    :return: The thresholded image.
    """
    _, thresh = cv2.threshold(img_gray, thresh_value, 255, cv2.THRESH_BINARY)
    if plot:
        create_plot(img_gray, thresh)

    return thresh


def otsu_thresholding(img_gray: np.ndarray, plot: bool = False) -> np.ndarray:
    """Applies Otsu's thresholding to an input grayscale image and optionally plots the original and thresholded images.

    :param img_gray: The input grayscale image.
    :param background: Background value to be subtracted from the image before thresholding (default is 0).
    :param plot: If True, the original and thresholded images will be displayed using matplotlib (default is False).

    :return: The thresholded image.
    """

    _, thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    if plot:
        create_plot(img_gray, thresh)

    return thresh


def adaptive_thresholding(
    img_gray: np.ndarray, block_size: int = 27, constant_offset: int = 1, plot: bool = False
) -> np.ndarray:
    """Draws contours on a copy of the input image and displays both images using matplotlib.
    :param img_gray: The input image in grayscale format.
    """

    # apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, constant_offset
    )

    if plot:
        create_plot(img_gray, thresh)

    return thresh


def hybrid_thresholding(
    img_gray: np.ndarray, block_size: int = 27, constant_offset: int = 1, plot: bool = False
) -> np.ndarray:
    """Draws contours on a copy of the input image and displays both images using matplotlib.
    :param img_gray: The input image in grayscale format.
    """

    # apply Otsu thresholding to estimate global threshold
    _, thresh_global = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # apply adaptive thresholding using local threshold values
    thresh_adaptive = cv2.adaptiveThreshold(
        img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, constant_offset
    )

    # combine global and local thresholds using bitwise AND
    thresh = cv2.bitwise_and(thresh_global, thresh_adaptive)

    if plot:
        create_plot(img_gray, thresh)

    return thresh


def local_otsu_thresholding(img: np.ndarray, background: int = 0, plot: bool = False) -> None:
    rcParams["font.size"] = 9

    radius = 100
    selem = disk(radius)

    local_otsu = rank.otsu(img - background, selem)
    threshold_global_otsu = threshold_otsu(img)
    global_otsu = img >= threshold_global_otsu

    if plot:
        fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(2, 2, figsize=(8, 5), sharex=True, sharey=True)
        ax0.set_title("Original")
        ax0.axis("off")

        fig.colorbar(ax1.imshow(local_otsu, cmap=plt.cm.gray), ax=ax1, orientation="horizontal")
        ax1.set_title("Local Otsu (radius=%d)" % radius)
        ax1.axis("off")

        ax2.imshow(img - background >= local_otsu, cmap=plt.cm.gray)
        ax2.set_title("Original >= Local Otsu")
        ax2.axis("off")

        ax3.imshow(global_otsu, cmap=plt.cm.gray)
        ax3.set_title("Global Otsu (threshold = %d)" % threshold_global_otsu)
        ax3.axis("off")

        plt.tight_layout()


def simple_thresholding_with_watershed(img_gray: np.ndarray, background: int = 0, plot: bool = False) -> None:
    """Applies scikit-image watershed segmentation on the input grayscale image.
    Displays the original, distance, and segmented images side by side using matplotlib.

    :param img_gray: The input image in grayscale format.
    :param background: The background intensity to be subtracted before watershed.
    """

    # Threshold the input image
    _, thresh = cv2.threshold(img_gray - background, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Calculate distance transform of the thresholded image
    distance = ndi.distance_transform_edt(thresh)

    # Find local maxima in the distance transform as markers
    coords = peak_local_max(distance, footprint=np.ones((3, 4)), labels=thresh)
    mask = np.zeros(distance.shape, dtype=bool)
    mask[tuple(coords.T)] = True
    markers, _ = ndi.label(mask)

    # Apply scikit-image watershed segmentation
    labels = watershed(-distance, markers, mask=thresh)

    if plot:
        # Display the images side by side
        fig, axes = plt.subplots(ncols=3, figsize=(9, 3), sharex=True, sharey=True)
        ax = axes.ravel()

        ax[0].imshow(img_gray, cmap=plt.cm.gray)
        ax[0].set_title("Original")

        ax[1].imshow(-distance, cmap=plt.cm.gray)
        ax[1].set_title("Distances")

        ax[2].imshow(labels, cmap=plt.cm.nipy_spectral, alpha=0.5)
        ax[2].set_title("Watershed Segmented")

        for a in ax:
            a.set_axis_off()

        fig.tight_layout()
        plt.show()

    return labels


def watershed_segmentation_with_contours(img_gray: np.ndarray, background: int = 0, plot: bool = False) -> None:
    """Applies scikit-image watershed segmentation on the input grayscale image.
    Displays the original image with superimposed contours of the segmented cells using matplotlib.

    :param img_gray: The input image in grayscale format.
    :param background: The background intensity to be subtracted before watershed.
    """

    _, img = cv2.threshold(img_gray - background, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # denoise image
    denoised = rank.median(img, disk(1))

    # find continuous region (low gradient -
    # where less than 10 for this image) --> markers
    # disk(5) is used here to get a more smooth image
    markers = rank.gradient(denoised, disk(4)) < 10
    markers = ndi.label(markers)[0]

    # local gradient (disk(2) is used to keep edges thin)
    gradient = rank.gradient(denoised, disk(5))

    # process the watershed
    labels = watershed(gradient, markers)

    if plot:
        # Extract and iterate through labeled cells (contours)
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.imshow(img_gray, cmap="gray")

        print(np.unique(labels))

        for label in np.unique(labels):
            if label == 0:
                continue  # Skip background

            mask = labels == label
            contour = measure.find_contours(mask, level=0.5)[0]

            # Process the contour or extract the ROI
            # For example, calculate area, perimeter, centroid, etc.
            # Here, we'll plot the contour on the image
            ax.plot(contour[:, 1], contour[:, 0], linewidth=2, c="r")

        ax.axis("image")
        ax.set_xticks([])
        ax.set_yticks([])
        plt.show()

    return labels


import cv2
import matplotlib.pyplot as plt
import numpy as np


def create_plot(img_gray, img_with_square):
    """Helper function to create a plot with contours."""
    plt.figure(figsize=(12, 6))
    plt.subplot(121), plt.imshow(img_gray, cmap="gray")
    plt.title("Original Image")
    plt.subplot(122), plt.imshow(img_with_square, cmap="gray")
    plt.title("Thresholded Image with Centered Square")


def adaptive_thresholding_with_square(
    img_gray: np.ndarray, block_size: int = 27, constant_offset: int = 1, plot: bool = False
) -> np.ndarray:
    """Applies adaptive thresholding and adds a red square to the image.
    :param img_gray: The input image in grayscale format.
    :param block_size: The block size for adaptive thresholding.
    :param constant_offset: Constant subtracted from the mean.
    :param plot: Whether to plot the images.
    :return: The thresholded image.
    """

    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, constant_offset
    )

    if plot:
        # Convert the grayscale image to RGB
        img_rgb = cv2.cvtColor(cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR), cv2.COLOR_BGR2RGB)

        # Create a copy of the RGB image to draw the red square
        img_with_square = img_rgb.copy()

        # Get the dimensions of the image
        height, width = img_with_square.shape[:2]

        # Calculate the coordinates for the centered square
        square_size = min(height, width, block_size)
        start_x = (width - square_size) // 2
        start_y = (height - square_size) // 2

        # Draw a red square on the image
        cv2.rectangle(
            img_with_square, (start_x, start_y), (start_x + square_size, start_y + square_size), (255, 0, 0), -1
        )

        # Display the original image and the image with the red square
        create_plot(img_gray, img_with_square)
        create_plot(img_gray, thresh)

    return thresh
