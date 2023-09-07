# Use the desired base image
FROM pytorch/pytorch:1.12.1-cuda11.3-cudnn8-runtime

# Set metadata
LABEL maintainer="David Anthony Parham <david.parham@alexandra.dk>"
LABEL version="1.0"
LABEL description="This Dockerfile creates a containerized version of the associated GitHub repository (https://github.com/Jumpat/SegmentAnythingin3D) to enhance reproducibility and ease of use."
# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Clone the GitHub repository
RUN git clone https://github.com/Jumpat/SegmentAnythingin3D.git /app/SegmentAnythingin3D

# Install SAM
WORKDIR /app/SegmentAnythingin3D/dependencies
RUN mkdir sam_ckpt && cd sam_ckpt && \
    wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth && \
    git clone https://github.com/facebookresearch/segment-anything.git && \
    pip install -e ./segment-anything

# Install Grounding-DINO
WORKDIR /app/SegmentAnythingin3D/dependencies
RUN git clone https://github.com/IDEA-Research/GroundingDINO.git && \
    pip install -e ./GroundingDINO

# Download weights
WORKDIR /app/SegmentAnythingin3D/dependencies/GroundingDINO/weights
RUN wget https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth

# Set the default command
CMD ["bash"]