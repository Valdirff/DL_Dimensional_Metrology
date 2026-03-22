import os, shutil
from sklearn.model_selection import train_test_split

# Current folders
dir_good = "../data/good"
dir_defect = "../data/bad"
labels_good = "../data/labels_good"
labels_defect = "../data/labels_bad"

# Target folders mapped for YOLO architectures
base_out = "../data/dataset_yolo/"
splits = ["train", "val", "test"]

for split in splits:
    os.makedirs(os.path.join(base_out, "images", split), exist_ok=True)
    os.makedirs(os.path.join(base_out, "labels", split), exist_ok=True)

# List images
good_images = [f for f in os.listdir(dir_good) if f.endswith((".jpg",".png"))]
defect_images = [f for f in os.listdir(dir_defect) if f.endswith((".jpg",".png"))]

# Isolate splits per category independently maintaining 70/20/10 ratio
def perform_split(data_list, test_size=0.1, val_size=0.2):
    train_val, test = train_test_split(data_list, test_size=test_size, random_state=42)
    train, val = train_test_split(train_val, test_size=val_size/(1-test_size), random_state=42)
    return train, val, test

good_train, good_val, good_test = perform_split(good_images)
defect_train, defect_val, defect_test = perform_split(defect_images)

# Pool results
divisions = {
    "train": [("good", f) for f in good_train] + [("defective", f) for f in defect_train],
    "val":   [("good", f) for f in good_val]   + [("defective", f) for f in defect_val],
    "test":  [("good", f) for f in good_test]  + [("defective", f) for f in defect_test],
}

# Duplicate payload to YOLO boundaries
for split, files in divisions.items():
    for ftype, img in files:
        if ftype == "good":
            src_img_dir, src_lbl_dir = dir_good, labels_good
        else:
            src_img_dir, src_lbl_dir = dir_defect, labels_defect

        # Origin Paths
        path_img = os.path.join(src_img_dir, img)
        txt_name = img.replace(".jpg",".txt").replace(".png",".txt")
        path_lbl = os.path.join(src_lbl_dir, txt_name)

        # Destination Paths
        out_img = os.path.join(base_out, "images", split, img)
        out_lbl = os.path.join(base_out, "labels", split, txt_name)

        shutil.copy(path_img, out_img)
        shutil.copy(path_lbl, out_lbl)

print("✅ Dataset balanced and restructured identically matching YOLO prerequisites globally in 'dataset_yolo/'")
