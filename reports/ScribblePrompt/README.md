# ScribblePrompt

### Links

- [GitHub](https://github.com/ChuanfeiHu/ScribblePrompt)
- [Demo](https://huggingface.co/spaces/halleewong/ScribblePrompt)
- [Homepage](https://scribbleprompt.csail.mit.edu/)
- [Video](https://www.youtube.com/watch?v=L8CiAoHzPUE)

## Description
ScribblePrompt is an interactive segmentation tool designed to help users segment new structures in medical images using scribbles, clicks, and bounding boxes. Where the ROI (Region of interest) can be interactively adjusted via positive and negative scribbles/clicks or via bounding boxes.

## What was it trained on?

ScribblePrompt was designed with generalization in mind, and thus was trained on a diverse collection of 65 open-access biomedical datasets using both real and synthetic labels, covering a variety of medical modalities, such as MRI, CT, Ultrasound, OCT and Microscopy.

## Questions to have answerd
- How well does the model handle electron microscopy data?
- How well does the model handle synchrotron microscopy data?
- Can the model be fine-tuned?
- Can the model segment volumetric data?

## Results

### Test Images
Synchrotron 1          |  Synchrotron 2
:-------------------------:|:-------------------------:
![Figure 1](media/Synchrotron_1.png)  |  ![Figure 2](media/Synchrotron_2.png)

Electron Microscopy 1          |  Electron Microscopy 2
:-------------------------:|:-------------------------:
![Figure 1](media/agent.gif)  |  ![Figure 2](media/player.gif)

## Verdict

> Soon to come