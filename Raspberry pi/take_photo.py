import cv2
import os

def create_dataset_directory(base_dir="dataset"):
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        print(f"[INFO] Created base directory: {base_dir}")

def main():
    user_name = input("Enter the user name (ID) for registration: ").strip()
    
    if not user_name:
        print("[ERROR] Name cannot be empty.")
        return

    base_dir = "dataset"
    create_dataset_directory(base_dir)
    
    user_path = os.path.join(base_dir, user_name)
    
    if not os.path.exists(user_path):
        os.makedirs(user_path)
        print(f"[INFO] Created directory for user: {user_path}")
    else:
        print(f"[INFO] Directory already exists: {user_path}")

    print("[INFO] Starting video stream...")
    print("[INSTRUCTION] Press 's' to save a photo. Press 'q' to quit.")
    
    cam = cv2.VideoCapture(0)

    cam.set(3, 640)
    cam.set(4, 480)

    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("[ERROR] Failed to grab frame")
            break

        cv2.imshow("Biometric Enrollment - Press 's' to Save", frame)

        k = cv2.waitKey(1)

        if k % 256 == 113:
            print("[INFO] Exiting registration...")
            break
        
        elif k % 256 == 115:
            img_name = f"{user_path}/image_{img_counter}.jpg"
            cv2.imwrite(img_name, frame)
            print(f"[SUCCESS] {img_name} saved!")
            img_counter += 1

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()