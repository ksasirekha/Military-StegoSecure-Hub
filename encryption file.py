import cv2
import os
import numpy as np

def encrypt_image(image_path, message, password):
    
    img = cv2.imread(image_path)
    
    if img is None:
        raise Exception("Error: Could not read the image file")
    
    # Check if image is large enough for the message
    if img.shape[0] * img.shape[1] < len(message):
        raise Exception("Error: Image is too small to embed the message")
    
    encrypted_img = img.copy()
    
    row = 0
    col = 0
    
    for char in message:
        
        ascii_val = ord(char) % 256
        
        encrypted_img[row, col, 0] = ascii_val
        
        col += 1
        if col >= img.shape[1]:
            col = 0
            row += 1
    
    encrypted_path = "encryptedImage.png"
    cv2.imwrite(encrypted_path, encrypted_img)
    
    with open("metadata.txt", "w") as f:
        f.write(f"{len(message)}\n{password}")
    
    print(f"Image encrypted successfully. Saved as {encrypted_path}")
    return encrypted_path

if __name__ == "__main__":
    image_path = input("Enter image path: ")
    message = input("Enter secret message: ")
    password = input("Enter a passcode: ")
    
    try:
        encrypted_file = encrypt_image(image_path, message, password)
        print(f"Message encrypted in {encrypted_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        