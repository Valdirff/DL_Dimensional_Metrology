import cv2
import numpy as np
import os

def create_synthetic_deviation_map(filename, defect=False):
    # Base "nominal" surface map (cool colors: cyan/blue)
    img = np.ones((400, 600, 3), dtype=np.uint8) * 200
    img[:, :, 0] = 255  # Blue channel maxed
    img[:, :, 1] = 250  # Green channel high
    
    # Add fake CAD grid/mesh lines
    for i in range(0, 600, 50):
        cv2.line(img, (i, 0), (i, 400), (180, 200, 255), 1)
    for j in range(0, 400, 50):
        cv2.line(img, (0, j), (600, j), (180, 200, 255), 1)
        
    if defect:
        # Simulate material excess/anomaly (warm colors: red/yellow gradient blob)
        center = (np.random.randint(200, 400), np.random.randint(100, 300))
        radius = np.random.randint(30, 80)
        cv2.circle(img, center, radius, (0, 0, 255), -1)  # Solid red core (OpenCV uses BGR)
        cv2.circle(img, center, radius + 20, (0, 100, 255), 15) # Orange halo
        cv2.circle(img, center, radius + 40, (0, 200, 255), 10) # Yellow halo
        
        # Add some random black specks mimicking scan noise on the defect
        for _ in range(50):
            pt = (center[0] + np.random.randint(-radius, radius), center[1] + np.random.randint(-radius, radius))
            cv2.circle(img, pt, 2, (0, 0, 0), -1)
            
    cv2.putText(img, "SYNTHETIC DEVIATION MAP", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2)
    cv2.putText(img, "(FOR DEMO PURPOSES ONLY)", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50,50,50), 1)
    
    return img

def main():
    out_dir = "../data/raw"
    os.makedirs(out_dir, exist_ok=True)
    
    print("Generating synthetic dummy dataset for demonstration...")
    
    # 5 Conforming images
    for i in range(1, 6):
        img_name = f"nominal_part_{i}.png"
        img = create_synthetic_deviation_map(img_name, defect=False)
        cv2.imwrite(os.path.join(out_dir, img_name), img)
        print(f"Generated {img_name} (Conforming)")
        
    # 5 Defective images
    for i in range(1, 6):
        img_name = f"defective_part_{i}.png"
        img = create_synthetic_deviation_map(img_name, defect=True)
        cv2.imwrite(os.path.join(out_dir, img_name), img)
        print(f"Generated {img_name} (Defective)")
        
    print("\n✅ Done! Synthetic maps saved to 'data/raw/'.")
    print("You can now safely run 'python scripts/classify_images.py' to test the interactive sorter.")

if __name__ == "__main__":
    main()
