# A 3D Biomedical Segmentation Hub

<figure>
  <p align="center">
    <img src="media/README/horns.gif" width=".75">
  </p>
  <figcaption align="center">A collection of state of the art resources for 3D interactive / semi-automatic segmentation within the biomedical domain</figcaption>
</figure>


## Why "A 3D Biomedical Segmentation Hub"?

This is a collection of papers and resources I curated for the RK-ESS project, which I'll maintain for the duration of the project with the latest advancements in the field.

### Motivation
- Addressing the increasing complexity of datasets, especially in 3D image segmentation.
- Emphasizing the development of interpretable deep models.
- Promoting the use of unsupervised learning models to minimize human intervention.
- Meeting the demand for real-time and memory-efficient models.
- Eliminating the bottleneck of 3D point-cloud segmentation.

## Contributing

If you think I have missed out on something (or) have any suggestions (papers, implementations and other resources), feel free to [pull a request]() or send me a direct message: [david.parham@alexandra.dk](mailto:david.parham@alexandra.dk)

Feedback and contributions are always welcome and appreciated!

## Table of Contents
- [A 3D Biomedical Segmentation Hub](#a-3d-biomedical-segmentation-hub)
  - [Why "A 3D Biomedical Segmentation Hub"?](#why-a-3d-biomedical-segmentation-hub)
    - [Motivation](#motivation)
  - [Contributing](#contributing)
  - [Table of Contents](#table-of-contents)
- [Backlog](#backlog)
  - [Foundation](#foundation)
    - [3D Interactive Segmentation](#3d-interactive-segmentation)
    - [3D Semi-automatic Segmentation](#3d-semi-automatic-segmentation)
  - [Papers](#papers)
    - [3D Interactive segmentation](#3d-interactive-segmentation-1)
    - [3D Semi-automatic segmentation](#3d-semi-automatic-segmentation-1)
    - [Uncategorized (Fully automated segmentation???)](#uncategorized-fully-automated-segmentation)
    - [Biomedical specific pretrained models](#biomedical-specific-pretrained-models)
  - [Datasets](#datasets)
  - [Knowledge Acquisition](#knowledge-acquisition)
    - [Typical Baseline Models](#typical-baseline-models)


# Backlog

- [x] Download the sample RK ESS demo dataset
- [ ] Download the full RK ESS dataset
  - [ ] **ERROR:** Folder is corrupted
    - [x] **SOLUTION?:** Request a different link from Søren or try the download from a different device (IN PROCESS)

- [x] Clone and build the [SAM repository](https://github.com/Jumpat/SegmentAnythingin3D/)
  - [ ] Test the code
    - [ ] **ERROR:** OS - Dependency incompatibility
      - [x] **SOLUTION?:** Create docker container
  - [ ] Adjust code (if necessary) so that it's compatible with the RK ESS data
- [ ] Clone and build the [DeepEdit repository](https://github.com/Project-MONAI/MONAILabel?utm_source=catalyzex.com)
  - [ ] Test the code
- [x] Maintain and beautify the README file
  - [ ] Complete the [dataset](#datasets) section
  - [ ] Move repo to alexandra org.
  - [ ] Beautify and update the [Knowledge aquisition](#knowledge-acquisition) and the [typical-baseline-models](#typical-baseline-models) sections

## Foundation
### 3D Interactive Segmentation
- **Definition**: 3D interactive segmentation involves user interaction and manipulation to delineate object boundaries in a three-dimensional (3D) image or volume. The user actively participates in the segmentation process by providing input, such as drawing or editing regions of interest, to guide the segmentation algorithm.

- **Example 1**: In a medical imaging application, a radiologist may use a 3D interactive segmentation tool to manually trace the boundaries of a tumor in a series of volumetric images. The tool provides real-time visualization and feedback, allowing the radiologist to adjust and refine the segmentation boundaries based on their expertise.

- **Example 2**: In computer graphics, a 3D artist might utilize an interactive segmentation tool to extract specific objects or regions from a 3D scene. By interacting with the software, the artist can select and refine the boundaries of objects in the scene, facilitating subsequent editing or compositing tasks.

<figure>
  <p align="center">
    <img src="media/README/Interactive_Segmentation.gif" width=".75">
  </p>
  <figcaption align="center"></figcaption>
</figure>

### 3D Semi-automatic Segmentation
- **Definition**: 3D semi-automatic segmentation combines the advantages of both manual interaction and automated algorithms. It involves an initial automatic segmentation step followed by user intervention to review and refine the results. The user interacts with the segmentation system to correct errors or provide additional guidance, improving the accuracy of the segmentation.

- **Example 1**: In a 3D medical imaging application, a semi-automatic segmentation approach may involve using an algorithm, such as region growing or active contours, to generate an initial segmentation of a specific anatomical structure. The user then reviews the segmentation results and adjusts boundaries as needed, ensuring accurate representation of the structure.

- **Example 2**: In a computer vision application for object recognition, a semi-automatic segmentation system might employ an automated algorithm to identify and outline objects of interest in a 3D scene. The user can interactively modify the generated segmentations, refining the boundaries or adding missing objects, to enhance the segmentation accuracy for subsequent processing steps.

<figure>
  <p align="center">
    <img src="media/README/Semi-Automatic.gif" width=".75">
  </p>
  <figcaption align="center"></figcaption>
</figure>

## Papers

### 3D Interactive segmentation
- [Segment Anything Model for Medical Image Analysis: an Experimental Study](https://arxiv.org/pdf/2304.10517.pdf) - Mazurowski, Maciej A. et al. Medical image analysis 89 (2023) :octocat: [**Click here for code**](https://github.com/mazurowski-lab/segment-anything-medical-evaluation)
- [Computer-Vision Benchmark Segment-Anything Model (SAM) in Medical Images: Accuracy in 12 Datasets](https://arxiv.org/pdf/2304.09324.pdf) - He, Sheng et al. (2023) :octocat: [**Click here for code**]()
- [When SAM Meets Medical Images: An Investigation of Segment Anything Model (SAM) on Multi-phase Liver Tumor Segmentation](https://arxiv.org/pdf/2304.08506.pdf) - Hu, Chuanfei and Xinde Li. ArXiv abs/2304.08506 (2023) :octocat: [**Click here for code**]()
- [Segment Anything in 3D with NeRFs](https://arxiv.org/pdf/2304.12308.pdf) - Cen, Jiazhong et al. ArXiv abs/2304.12308 (2023) :octocat: [**Click here for code**](https://github.com/Jumpat/SegmentAnythingin3D)
- [3DSAM-adapter: Holistic Adaptation of SAM from 2D to 3D for Portable Medical Image Segmentation](https://arxiv.org/pdf/2306.13465.pdf) - Gong, Shizhan et al. ArXiv abs/2306.13465 (2023) :octocat: [**Click here for code**](https://github.com/med-air/3DSAM-adapter)
- [TomoSAM: a 3D Slicer extension using SAM for tomography segmentation](https://arxiv.org/pdf/2306.08609.pdf) - Semeraro, Federico et al. ArXiv abs/2306.08609 (2023) :octocat: [**Click here for code**](https://github.com/fsemerar/SlicerTomoSAM)
- [SAM3D: Zero-Shot 3D Object Detection via Segment Anything Model](https://arxiv.org/pdf/2306.02245.pdf) - Zhang, Dingyuan et al. ArXiv abs/2306.02245 (2023) :octocat: [**Click here for code**](https://github.com/DYZhang09/SAM3D)
- [DeepEdit: Deep Editable Learning for Interactive Segmentation of 3D Medical Images](https://arxiv.org/abs/2305.10655) - Diaz-Pinto, Andrés et al. ArXiv abs/2305.10655 (2023) :octocat: [**Click here for code**](https://github.com/Project-MONAI/MONAILabel?utm_source=catalyzex.com)
- [Volumetric memory network for interactive medical image segmentation](https://www.sciencedirect.com/science/article/pii/S1361841522002316) - Zhou, Tianfei et al. Medical image analysis 83 (2022) :octocat: [**Click here for code**]()
- [i3Deep: Efficient 3D interactive segmentation with the nnU-Net](https://openreview.net/pdf?id=R420Pr5vUj3) - Gotkowski, Karol et al. International Conference on Medical Imaging with Deep Learning (2022) :octocat: [**Click here for code**](https://github.com/Karol-G/i3Deep)
- [iSegFormer: Interactive Segmentation via Transformers with Application to 3D Knee MR Images](https://arxiv.org/pdf/2112.11325.pdf) - Liu, Qin. ArXiv abs/2112.11325 (2021) :octocat: [**Click here for code**](https://github.com/uncbiag/iSegFormer)
- [Rapid Interactive and Intuitive Segmentation of 3D Medical Images Using Radial Basis Function Interpolation](https://www.mdpi.com/2313-433X/3/4/56) - Kurzendorfer, Tanja et al. J. Imaging 3 (2017) :octocat: [**Click here for code**]()

### 3D Semi-automatic segmentation
- [Segment Anything Model for Medical Image Analysis: an Experimental Study](https://arxiv.org/pdf/2304.10517.pdf) - Mazurowski, Maciej A. et al. Medical image analysis 89 (2023) :octocat: [**Click here for code**](https://github.com/mazurowski-lab/segment-anything-medical-evaluation)
- [Computer-Vision Benchmark Segment-Anything Model (SAM) in Medical Images: Accuracy in 12 Datasets](https://arxiv.org/pdf/2304.09324.pdf) - He, Sheng et al. (2023) :octocat: [**Click here for code**]()
- [When SAM Meets Medical Images: An Investigation of Segment Anything Model (SAM) on Multi-phase Liver Tumor Segmentation](https://arxiv.org/pdf/2304.08506.pdf) - Hu, Chuanfei and Xinde Li. ArXiv abs/2304.08506 (2023) :octocat: [**Click here for code**]()
- [Segment Anything in 3D with NeRFs](https://arxiv.org/pdf/2304.12308.pdf) - Cen, Jiazhong et al. ArXiv abs/2304.12308 (2023) :octocat: [**Click here for code**](https://github.com/Jumpat/SegmentAnythingin3D)
- [3DSAM-adapter: Holistic Adaptation of SAM from 2D to 3D for Portable Medical Image Segmentation](https://arxiv.org/pdf/2306.13465.pdf) - Gong, Shizhan et al. ArXiv abs/2306.13465 (2023) :octocat: [**Click here for code**](https://github.com/med-air/3DSAM-adapter)
- [TomoSAM: a 3D Slicer extension using SAM for tomography segmentation](https://arxiv.org/pdf/2306.08609.pdf) - Semeraro, Federico et al. ArXiv abs/2306.08609 (2023) :octocat: [**Click here for code**](https://github.com/fsemerar/SlicerTomoSAM)
- [SAM3D: Zero-Shot 3D Object Detection via Segment Anything Model](https://arxiv.org/pdf/2306.02245.pdf) - Zhang, Dingyuan et al. ArXiv abs/2306.02245 (2023) :octocat: [**Click here for code**](https://github.com/DYZhang09/SAM3D)
- [Seq2Link: an efficient and versatile solution for semi-automatic cell segmentation in 3D image stacks](https://www.nature.com/articles/s41598-023-34232-6) - Wen, Chentao et al. Scientific Reports 13 (2022) :octocat: [**Click here for code**]()
- [VAST (Volume Annotation and Segmentation Tool): Efficient Manual and Semi-Automatic Labeling of Large 3D Image Stacks](https://www.frontiersin.org/articles/10.3389/fncir.2018.00088/full) - Berger, Daniel Raimund et al. Frontiers in Neural Circuits 12 (2018) :octocat: [**Click here for code**](https://github.com/vastgroup/vast-tools)

### Uncategorized (Fully automated segmentation???)
- [SwinMM: Masked Multi-view with Swin Transformers for 3D Medical Image Segmentation](https://arxiv.org/pdf/2307.12591.pdf) - Wang, Yiqing et al. ArXiv abs/2307.12591 (2023) :octocat: [**Click here for code**](https://github.com/UCSC-VLAA/SwinMM/)
- [Dynamic Linear Transformer for 3D Biomedical Image Segmentation](https://arxiv.org/pdf/2206.00771.pdf) - Zhang, Zheyu and Ulas Bagci. ArXiv abs/2206.00771 (2022) :octocat: [**Click here for code**](https://github.com/freshman97/LinTransUNet)
- [Understanding the Tricks of Deep Learning in Medical Image Segmentation: Challenges and Future Directions](https://arxiv.org/pdf/2209.10307.pdf) - Zhang, Dong-Ming et al. (2022) :octocat: [**Click here for code**](https://github.com/hust-linyi/MedISeg?utm_source=catalyzex.com)
- [Beyond automatic medical image segmentation - the spectrum between fully manual and fully automatic delineation](https://iopscience.iop.org/article/10.1088/1361-6560/ac6d9c) - Trimpl, Michael Johann et al. Physics in Medicine & Biology 67 (2022) :octocat: [**Click here for code**]()
- [Recent advances and clinical applications of deep learning in medical image analysis](https://www.connectedpapers.com/main/7fc464470b441c691d10e7331b14a525bc79b8bb/3D-U%20Net%3A-Learning-Dense-Volumetric-Segmentation-from-Sparse-Annotation/derivative) - Chen, Xuxin et al. Medical image analysis 79 (2021) :octocat: [**Click here for code**]()
### Biomedical specific pretrained models




## Datasets
- [SA-1B](https://www.connectedpapers.com/main/7fc464470b441c691d10e7331b14a525bc79b8bb/3D-U%20Net%3A-Learning-Dense-Volumetric-Segmentation-from-Sparse-Annotation/derivative) - Kirillov, Alexander et al. ArXiv abs/2304.02643 (2023) :octocat: [**Click here for download**](https://ai.meta.com/datasets/segment-anything/)
- [MRI-Spine]
- MRI-Heart
- MRI-Prostate
- MRI-Brain
- MRI-Breast
- Xray-Chest
- Xray-Hip
- US-Breast
- US-Kidney
- US-Muscle
- US-Nerve
- US-Ovarian-Tumor
- Covid19
- LiDC
- HNSCC
- WORD
- ACDC
- BTCV
- TCIA-Covid19
- TCIA-Colon
- AbdomenCT-1K
- BraTS
- BUID
- CIR
- Kvasir
- ISIC
- LA
- Hippo
- KiTS21
- OAI-ZIB
- [Medical Decathlon](https://arxiv.org/pdf/2106.05735.pdf) - Antonelli, Michela et al. Nature Communications 13 (2021) :octocat: [**Click here for download**](https://medicaldecathlon.com/) - A-Kader HH, Ghishan FK. The Pancreas. Textbook of Clinical Pediatrics. (2012) :octocat: [**Click here for download**](https://competitions.codalab.org/competitions/17094)
- CT-Organ
- [PET-Whole-Body]
- [NIH - National Institute of Health](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7124086/)
- [LiTs](https://arxiv.org/pdf/1901.04056.pdf) - Bilic, Patrick et al. Medical image analysis 84 (2019) :octocat: [**Click here for download**](https://competitions.codalab.org/competitions/17094)

## Knowledge Acquisition
- [Unite.AI - Segment Anything Model in Computer Vision Gets a Massive Boost](https://www.unite.ai/segment-anything-model-computer-vision-gets-a-massive-boost/)
- [Towards Data Science - See What You SAM](https://towardsdatascience.com/see-what-you-sam-4eea9ad9a5de)
- [OpenReview - Segment Anything Model](https://openreview.net/pdf?id=iilLHaINUW)
- [HuggingFace - SAM Model Documentation](https://huggingface.co/docs/transformers/main/model_doc/sam)
- [YouTube - SAM Model Demo](https://www.youtube.com/watch?v=vZK45noZVIA)
- [GitHub - SAM-Medical-Imaging Implementation](https://github.com/amine0110/SAM-Medical-Imaging)
- [MarkTechPost - When SAM Meets NeRF: This AI Model Can Segment Anything in 3D](https://www.marktechpost.com/2023/05/22/when-sam-meets-nerf-this-ai-model-can-segment-anything-in-3d/)
- [GitHub - SegmentAnythingin3D](https://github.com/Jumpat/SegmentAnythingin3D)
- [GitHub Topics - Interactive Segmentation](https://github.com/topics/interactive-segmentation)
- [GitHub - SegmentAnything3D](https://github.com/Pointcept/SegmentAnything3D)
- [GitHub - SAM-3D-Selector](https://github.com/nexuslrf/SAM-3D-Selector)


### Typical Baseline Models
- nnU-Net baseline [https://arxiv.org/abs/1809.10486]
  - Automatic segmentation model
- U-Net
- U-Net++
- Attention U-Net
- Trans U-Net
- UCTransNet

<!-- ## License

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>. -->










