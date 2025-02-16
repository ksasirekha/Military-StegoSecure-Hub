import cv2
import os

def decrypt_image(encrypted_image_path, password):

    encrypted_img = cv2.imread(encrypted_image_path)
    
    if encrypted_img is None:
        raise Exception("Error: Could not read the encrypted image file")
    
    try:
        with open("metadata.txt", "r") as f:
            msg_length = int(f.readline().strip())
            stored_password = f.readline().strip()
    except:
        raise Exception("Error: Could not read metadata file")
    
    if password != stored_password:
        raise Exception("Error: Incorrect password")
    
    row = 0
    col = 0
    message = ""
    
    for i in range(msg_length):
        
        ascii_val = encrypted_img[row, col, 0]
        
        message += chr(ascii_val)
        
        col += 1
        if col >= encrypted_img.shape[1]:
            col = 0
            row += 1
    
    return message

if __name__ == "__main__":
    encrypted_image_path = input("Enter encrypted image path: ")
    password = input("Enter passcode for decryption: ")
    
    try:
        decrypted_message = decrypt_image(encrypted_image_path, password)
        print("Decrypted message:", decrypted_message)
    except Exception as e:
        print(f"An error occurred: {str(e)}")