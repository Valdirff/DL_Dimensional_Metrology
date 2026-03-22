# Deep Learning for Dimensional Metrology: CNN & YOLOv8 Framework 🔍

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![YOLO](https://img.shields.io/badge/YOLOv8-00FFFF?style=for-the-badge&logo=yolo&logoColor=black)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Ultralytics](https://img.shields.io/badge/Ultralytics-000000?style=for-the-badge)

An advanced Deep Learning solution applied to **Automated Visual Metrology** in industrial environments. This project automates the inspection of digitized complex mechanical parts through two distinct architectures: a Custom Convolutional Neural Network (1D/2D CNN) for binary anomaly classification, and the YOLOv8 architectural framework for precise spatial defect localization.

This codebase was developed in parallel with academic research correlating Industrial Engineering, Dimensional Metrology and Computer Vision. 

> 🔒 **Proprietary Data Notice:** The visual components, CAD dimensional point-clouds, and labeled datasets used during this study belong to a private industrial production facility. To comply with IP restrictions and confidentiality agreements, the raw image datasets (`dados/`) have been strictly ignored from the repository. This source serves purely as a portfolio demonstration of the computational architecture and programmatic flow.

---

## ⚙️ Core Architectures Developed

### 1. The Anomaly Classifier (Custom CNN)
Instead of treating images statically, the raw dimensional heatmap comparisons (color-scaled geometrical deviation maps) were fed into a Custom CNN.
- **Workflow:** Images resized to 128x128 pixels, unified RGB matrices, scaled 0-1.
- **Architecture Base:** 3 sequenced blocks of Convolutions (3x3 windows, 32->64->128 layout) with `ReLU`, dimensional squash via `MaxPooling 2x2`.
- **Classification Head:** Dense connected layer of 256 neurons, `Dropout(0.5)` for regularization enforcing non-memorized logic, capped by a final `Sigmoid` output.
- **Results:** By expanding the dataset via manual simulated CAD rotations/translations to 800+ images, the architecture organically conquered a massive **97% Diagnostic Accuracy**.

### 2. The Spatial Locator (YOLOv8-Nano)
While a CNN flags *if* a part is broken, industrial lines require coordinates.
- **Formulation:** Manual Region of Interest (ROI) labeling was mapped leveraging OpenCV onto the generic YOLO spatial tensor schema.
- **Transfer Learning Integration:** Ultralytics YOLOv8`n` backbone pre-trained on `COCO` was frozen and strictly fine-tuned for geometric material absence/excess mapping mapping over 150 epochs. 
- **Results:** Achieved high geometric intersection scoring (**71.7% IoU threshold coverage** over challenging topological terrains) pushing the boundary of autonomous visual QA. 

---

## 📂 Repository Structure

The actual operational scripts from testing, parsing to training have been meticulously curated and organized:

```text
├── .gitignore                   # Protects proprietary data mapping
├── README.md                    # Project index
├── requirements.txt             
│
├── notebooks/                   # Core Training environments (Jupyter)
│   ├── 01_CNN_Binary_Classification.ipynb
│   └── 02_YOLO_Defect_Localization.ipynb
│
├── scripts/                     # Data Extraction & Inference Toolkit
│   ├── classificar_imagens.py   # Final Inference / Execution Loop
│   ├── yolo_labels.py           # Custom OpenCV Annotation Engine
│   └── yolo_selecao.py          # YOLO Image/Tensor dataset structure parser
│
└── docs/                        # Research and Analytical Textual context
    └── TCC_Manuscript.txt       # The academic backbone establishing the logic 

```

---

## 🛠️ Usage Methodology

Although the local dataset references are scrubbed, the training structures are universally applicable to generic manufacturing datasets (e.g. Castings, Plastic mold extrusions):

**1. Install Ultralytics and dependencies:**
```bash
pip install -r requirements.txt
```

**2. Setup the YOLO environment:**
To bootstrap YOLO onto your new generic dataset, assure your structure aligns with:
```bash
data/
 ├── images/ (train, val, test)
 └── labels/ (train, val, test)
```
Update boundaries and classes in the standalone `data.yaml`.

**3. Test the Inference Engine:**
Supply new arbitrary images into the deployment script allowing `classificar_imagens.py` to route them correctly through the PyTorch layers.
