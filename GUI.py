import streamlit as st
import cv2
import numpy as np
import os
from cryptography.fernet import Fernet

def generate_key(password):
    return Fernet.generate_key()

def aes_encrypt(message, password):
    key = Fernet.generate_key()
    cipher = Fernet(key)
    encrypted_message = cipher.encrypt(message.encode())
    return encrypted_message, key

def aes_decrypt(encrypted_message, key):
    cipher = Fernet(key)
    decrypted_message = cipher.decrypt(encrypted_message).decode()
    return decrypted_message

def encrypt_image(image, message, password):
    encrypted_message, key = aes_encrypt(message, password)
    img = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise Exception("Error: Could not read the image file")
    if img.shape[0] * img.shape[1] < len(encrypted_message):
        raise Exception("Error: Image is too small to embed the message")

    encrypted_img = img.copy()
    row, col = 0, 0
    for byte in encrypted_message:
        encrypted_img[row, col, 0] = byte
        col += 1
        if col >= img.shape[1]:
            col = 0
            row += 1

    with open("metadata.txt", "w") as f:
        f.write(f"{len(encrypted_message)}\n{password}\n{key.decode()}")

    return encrypted_img

def decrypt_image(image, password):
    img = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)
    with open("metadata.txt", "r") as f:
        msg_length = int(f.readline().strip())
        stored_password = f.readline().strip()
        key = f.readline().strip()
    if password != stored_password:
        raise Exception("Error: Incorrect password")
    row, col = 0, 0
    encrypted_message = bytes()
    for i in range(msg_length):
        encrypted_message += bytes([img[row, col, 0]])
        col += 1
        if col >= img.shape[1]:
            col = 0
            row += 1
    decrypted_message = aes_decrypt(encrypted_message, key.encode())
    return decrypted_message

st.title("Military StegoSecure Hub")
choice = st.sidebar.selectbox("Select an option", ["Encrypt", "Decrypt"])

if choice == "Encrypt":
    uploaded_image = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg", "bmp", "tiff"])
    message = st.text_area("Enter the message to hide")
    password = st.text_input("Enter a passcode", type="password")
    if st.button("Encrypt Message"):
        if uploaded_image and message and password:
            encrypted_img = encrypt_image(uploaded_image, message, password)
            is_success, buffer = cv2.imencode(".png", encrypted_img)
            st.image(encrypted_img, caption="Encrypted Image")
            st.download_button("Download Encrypted Image", data=buffer.tobytes(), file_name="encrypted_image.png", mime="image/png")
        else:
            st.error("Please provide all inputs.")

if choice == "Decrypt":
    uploaded_image = st.file_uploader("Upload an Encrypted Image", type=["png", "jpg", "jpeg", "bmp", "tiff"])
    password = st.text_input("Enter the passcode", type="password")
    if st.button("Decrypt Message"):
        if uploaded_image and password:
            try:
                decrypted_message = decrypt_image(uploaded_image, password)
                st.success(f"Decrypted Message: {decrypted_message}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.error("Please provide all inputs.")
