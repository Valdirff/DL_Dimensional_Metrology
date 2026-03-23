import cv2
import os

# Directories
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
defect_images_folder = os.path.join(SCRIPT_DIR, "../data/bad/")
good_images_folder = os.path.join(SCRIPT_DIR, "../data/good/")
defect_labels_folder = os.path.join(SCRIPT_DIR, "../data/labels_bad/")
good_labels_folder = os.path.join(SCRIPT_DIR, "../data/labels_good/")
os.makedirs(defect_labels_folder, exist_ok=True)
os.makedirs(good_labels_folder, exist_ok=True)

# Global Variables
drawing = False
ix, iy = -1, -1
boxes = []

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, boxes, img, clone

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img = clone.copy()
            for (xmin, ymin, xmax, ymax) in boxes:
                cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 0, 0), 2)
            cv2.rectangle(img, (ix, iy), (x, y), (0, 0, 0), 2)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(img, (ix, iy), (x, y), (0, 0, 0), 2)
        boxes.append((min(ix, x), min(iy, y), max(ix, x), max(iy, y)))

def save_yolo_format(file_name, boxes, width, height):
    txt_path = os.path.join(defect_labels_folder, file_name.replace(".jpg", ".txt").replace(".png", ".txt"))
    with open(txt_path, "w") as f:
        for (xmin, ymin, xmax, ymax) in boxes:
            x_center = ((xmin + xmax) / 2) / width
            y_center = ((ymin + ymax) / 2) / height
            w = (xmax - xmin) / width
            h = (ymax - ymin) / height
            f.write(f"0 {x_center} {y_center} {w} {h}\n")


# ====================================================
# 1) ANNOTATE DEFECTIVE IMAGES
# ====================================================
arquivos = sorted([f for f in os.listdir(defect_images_folder) if f.endswith((".jpg", ".png"))])
i = 0

while 0 <= i < len(arquivos):
    file = arquivos[i]
    path = os.path.join(defect_images_folder, file)
    img = cv2.imread(path)
    clone = img.copy()
    boxes = []

    cv2.namedWindow("image", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback("image", draw_rectangle)

    while True:
        cv2.imshow("image", img)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"):  # save and next
            save_yolo_format(file, boxes, img.shape[1], img.shape[0])
            print(f"Saved: {file} -> {len(boxes)} defects")
            i += 1
            break

        elif key == ord("r"):  # reset boxes
            img = clone.copy()
            boxes = []
            print("Resetting all boxes.")

        elif key == ord("z"):  # undo last box
            if boxes:
                boxes.pop()
                img = clone.copy()
                for (xmin, ymin, xmax, ymax) in boxes:
                    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 0, 0), 2)
                print("Last box removed.")
            else:
                print("No boxes to remove.")

        elif key == ord("b"):  # go back to previous
            print("Returning to previous image...")
            i = max(0, i - 1)
            break

        elif key == ord("q"):  # quit instantly
            print("Exiting program...")
            cv2.destroyAllWindows()
            exit(0)

    cv2.destroyAllWindows()

# ====================================================
# 2) GENERATE EMPTY TXT FOR GOOD IMAGES
# ====================================================
for file in os.listdir(good_images_folder):
    if file.endswith((".jpg", ".png")):
        txt_path = os.path.join(good_labels_folder, file.replace(".jpg", ".txt").replace(".png", ".txt"))
        if not os.path.exists(txt_path):
            with open(txt_path, "w") as f:
                pass
            print(f"Generated empty template for generic un-annotated image: {file}")
