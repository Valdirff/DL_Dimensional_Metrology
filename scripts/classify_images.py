import cv2
import os
import shutil
from pathlib import Path

# ====== CONFIG ======
BASE = Path("data")
DIR_ORG   = BASE / "raw"
DIR_GOOD  = BASE / "good"
DIR_BAD = BASE / "bad"

EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".webp"}
MAX_SIDE = 1300

# Overlay appearance
FONT_SCALE = 0.5       
THICKNESS  = 1         
BOX_ALPHA  = 0.35      
BOX_PAD    = 6         
SHOW_INSTRUCTIONS = False   
# =====================

def ensure_dirs():
    for d in [DIR_ORG, DIR_GOOD, DIR_BAD]:
        d.mkdir(parents=True, exist_ok=True)

def list_images():
    return [p.name for p in sorted(DIR_ORG.iterdir()) if p.suffix.lower() in EXTS]

def unique_dest_path(dst_dir: Path, filename: str) -> Path:
    base = Path(filename).stem
    ext  = Path(filename).suffix
    cand = dst_dir / filename
    k = 1
    while cand.exists():
        cand = dst_dir / f"{base}_{k}{ext}"
        k += 1
    return cand

def move_file(src: Path, dst_dir: Path) -> Path:
    dst = unique_dest_path(dst_dir, src.name)
    shutil.move(str(src), str(dst))
    return dst

def undo_last_action(history):
    if not history:
        print("⚠️ Nothing to undo.")
        return False
    last = history.pop()
    if last["dst"].exists():
        back = unique_dest_path(last["src"].parent, last["src"].name)
        shutil.move(str(last["dst"]), str(back))
        print(f"↩️ Undone: {last['dst'].name} moved back to {back}")
        return True
    print("⚠️ Could not undo (file not found).")
    return False

def resize_to_fit(img):
    h, w = img.shape[:2]
    m = max(h, w)
    if m <= MAX_SIDE:
        return img
    scale = MAX_SIDE / m
    return cv2.resize(img, (int(w*scale), int(h*scale)), interpolation=cv2.INTER_AREA)

def draw_overlay(img, lines, tl=(10, 10)):
    """Draws a compact box with instructions."""
    overlay = img.copy()
    sizes = [cv2.getTextSize(t, cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, THICKNESS)[0] for t in lines]
    w = max(s[0] for s in sizes) + 2*BOX_PAD
    h = sum(s[1] for s in sizes) + (len(lines)-1)*4 + 2*BOX_PAD
    x1, y1 = tl
    x2, y2 = x1 + w, y1 + h
    cv2.rectangle(overlay, (x1, y1), (x2, y2), (0,0,0), -1)
    img[:] = cv2.addWeighted(overlay, BOX_ALPHA, img, 1-BOX_ALPHA, 0)
    
    y = y1 + BOX_PAD + sizes[0][1]
    for t, s in zip(lines, sizes):
        cv2.putText(img, t, (x1 + BOX_PAD, y), cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, (255,255,255), THICKNESS, cv2.LINE_AA)
        y += s[1] + 4

def show_image_with_overlay(img_path: Path, index: int, total: int, show_instr: bool):
    img = cv2.imread(str(img_path))
    if img is None:
        print(f"⚠️ Could not open: {img_path}")
        return False
    img = resize_to_fit(img)

    line1 = f"{index+1}/{total} | {img_path.name}"
    if show_instr:
        line2 = "[g]=good  [b]=bad  [SPACE]=undo  [i]=hide help  [q/ESC]=exit"
        draw_overlay(img, [line1, line2])
    else:
        draw_overlay(img, [line1])

    cv2.imshow("Classifier", img)
    return True

def main():
    ensure_dirs()
    files = list_images()
    if not files:
        print("No images found in 'data/raw'.")
        return

    print("Controls: [g]=good, [b/B]=bad, [SPACE]=undo, [i]=toggle help, [q/ESC]=exit")
    print(f"Total found in raw/: {len(files)}")

    history = []
    i = 0
    window = "Classifier"
    cv2.namedWindow(window, cv2.WINDOW_AUTOSIZE)
    show_instr = SHOW_INSTRUCTIONS

    while i < len(files):
        name = files[i]
        path = DIR_ORG / name
        if not path.exists():
            i += 1
            continue

        if not show_image_with_overlay(path, i, len(files), show_instr):
            i += 1
            cv2.waitKey(10)
            continue

        key = cv2.waitKey(0) & 0xFF

        if key in (ord('q'), 27):
            print("Exiting...")
            break
        elif key == ord('i'):      
            show_instr = not show_instr
            cv2.destroyWindow(window)
        elif key == ord('g'):
            dst = move_file(path, DIR_GOOD)
            history.append({"src": DIR_ORG / name, "dst": dst})
            print(f"✅ {name} → good/")
            i += 1
            cv2.destroyWindow(window)
        elif key in (ord('b'), ord('B')):
            dst = move_file(path, DIR_BAD)
            history.append({"src": DIR_ORG / name, "dst": dst})
            print(f"❌ {name} → bad/")
            i += 1
            cv2.destroyWindow(window)
        elif key == 32:  
            undone = undo_last_action(history)
            if undone:
                i = max(0, i - 1)
            cv2.destroyWindow(window)
        else:
            print("Unrecognized key. Use: g / b(B) / space / i / q(ESC).")

    cv2.destroyAllWindows()
    print("Done!")

if __name__ == "__main__":
    main()
