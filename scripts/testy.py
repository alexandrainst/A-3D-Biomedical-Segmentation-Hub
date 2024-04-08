import csv
import itertools

import arrow
import cv2
import numpy as np
from matplotlib import pyplot as plt


def comparison_plot(img1, img2, title1, titl2, cmap1="gray", cmap2="gray"):
    # Create a figure with two subplots
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    axes[0].imshow(img1, cmap=cmap1)
    axes[0].set_title(title1)
    axes[0].axis("off")

    axes[1].imshow(img2, cmap=cmap2)
    axes[1].set_title(titl2)
    axes[1].axis("off")

    # Adjust the spacing between the subplots
    plt.tight_layout()

    # Display the plots
    plt.show()


def apply_equalization_and_stretching(img, min_intensity=0, max_intensity=255, plot=False):
    # Apply histogram equalization to enhance contrast
    equalized_image = cv2.equalizeHist(img)

    # Apply contrast stretching to boost pixel intensity
    stretched_image = np.interp(
        equalized_image, (equalized_image.min(), equalized_image.max()), (min_intensity, max_intensity)
    )

    if plot:
        comparison_plot(img, stretched_image, "Grayscale Image", "Stretched Image")

    return stretched_image


def thresh_refinement(img, plot=False):
    # Define the size threshold to filter out small speckles
    min_region_size = 30  # Adjust this value as needed

    # Erosion to remove small speckles
    kernel = np.ones((15, 15), np.uint8)
    eroded_image = cv2.erode(img, kernel, iterations=1)

    # Dilation to reconnect the remaining pixels
    dilated_image = cv2.dilate(eroded_image, kernel, iterations=1)

    # Convert the dilated image to CV_8U data type
    dilated_image = dilated_image.astype(np.uint8)

    # Connected Component Analysis to label regions
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(dilated_image, connectivity=8)

    # Filter regions by size
    filtered_image = np.zeros(dilated_image.shape, dtype=np.uint8)
    for i in range(1, num_labels):  # Skip the background label (0)
        region_size = stats[i, cv2.CC_STAT_AREA]
        if region_size >= min_region_size:
            filtered_image[labels == i] = 255

    if plot:
        comparison_plot(img, filtered_image, "Grayscale Image", "Refined Image")

    return filtered_image


def local_normalization(img, kernel_size=(21, 21), plot=False):
    # Convert to floating-point for more accurate calculations
    img_float = img.astype(np.float32)

    # Apply local normalization using a box filter
    img_normalized = cv2.boxFilter(img_float, -1, ksize=kernel_size)

    # Convert back to 8-bit unsigned integer
    img_normalized = np.uint8(img_normalized)

    if plot:
        comparison_plot(img, img_normalized, "Grayscale Image", "Normalized Image")

    return img_normalized


def extract_crop_coordinates(img):
    # Get the dimensions of the image
    height, width = img.shape

    # Iterate through each pixel and append its value to the list
    for y, x in itertools.product(range(height), range(width)):
        pixel_value = img[y, x]

        if pixel_value > 240:
            return y, x


def count_black_pixels(image):
    # Count black pixels (pixel values equal to 0)
    black_pixel_count = np.count_nonzero(image == 0)

    return black_pixel_count


def local_timestamp():
    # Set the timezone to Copenhagen
    copenhagen_timezone = "Europe/Copenhagen"
    # Get the current timestamp using Arrow with the specified timezone
    return arrow.now(copenhagen_timezone).format("YYYY-MM-DD@HH:mm:ss")


def convert_slice_stats_to_csv(data, file_name):
    headers = ("id", "area", "aspect_ratio", "dispersion", "depth")
    csv_filename = f"{file_name}_{local_timestamp()}.csv"

    with open(csv_filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()

        for key, value in data.items():
            row = {field: value.get(field, "") for field in headers[1:]}
            row["id"] = key
            writer.writerow(row)


def convert_volume_stats_to_csv(data, file_name):
    headers = (
        "min_air_pockets",
        "max_air_pockets",
        "min_air_pocket_size",
        "max_air_pocket_size",
        "min_black_pixel_count",
        "max_black_pixel_count",
        "min_air_pocket_percentage",
        "max_air_pocket_percentage",
        "min_air_pocket_depth",
        "max_air_pocket_depth",
    )
    csv_filename = f"{file_name}_{local_timestamp()}.csv"

    with open(csv_filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerow(data)


def plot_histogram(image):
    # Calculate histogram
    hist, bins = np.histogram(image.flatten(), bins=256, range=[0, 256])

    # Plot histogram
    plt.plot(hist, color="gray")
    plt.xlabel("Pixel Intensity")
    plt.ylabel("Frequency")
    plt.title("Pixel Intensity Histogram")

    # Set x-axis ticks at 10-step intervals
    plt.xticks(np.arange(0, 256, step=10), rotation=60)
    # Add a dashed horizontal red line at y=0
    plt.axhline(0, color="red", linestyle="--")
    plt.show()


def match_image_dimensions(image1, image2):
    # Get the dimensions of the first image
    height1, width1 = image1.shape

    # Get the dimensions of the second image
    height2, width2 = image2.shape

    # Calculate the dimensions of the padded image
    target_height = max(height1, height2)
    target_width = max(width1, width2)

    # Create a new image with the dimensions of the padded image and fill it with white
    padded_image = np.ones((target_height, target_width), dtype=np.uint8) * 255

    # Paste the second image onto the padded image
    padded_image[:height2, :width2] = image2

    return padded_image


# def cropped_image(img, plot=False):
#     enhanced_img = apply_equalization_and_stretching(img)
#     thresh_img = simple_thresholding(enhanced_img, thresh_value=250, plot=False)
#     refined_img = thresh_refinement(thresh_img)
#     cutoff_row, _ = extract_crop_coordinates(refined_img)
#     cropped_image = img[:cutoff_row, :]

#     cropped_image_with_padding = match_image_dimensions(img, cropped_image)
#     if plot:
#         # Create a figure with two subplots
#         fig, axes = plt.subplots(1, 2, figsize=(12, 6))

#         # Plot the grayscale image in the first subplot
#         axes[0].imshow(img, cmap="gray")
#         axes[0].axhline(y=cutoff_row, color="r", linestyle="--", label="Cropping Line")
#         axes[0].set_title("Original Image")
#         axes[0].axis("off")
#         axes[0].legend()

#         # Plot the stretched image in the second subplot
#         axes[1].imshow(cropped_image_with_padding, cmap="gray")
#         axes[1].set_title("Cropped Image")
#         axes[1].axis("off")

#         # Adjust the spacing between the subplots
#         plt.tight_layout()

#         # Display the plots
#         plt.show()

#     return cropped_image
