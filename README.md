# 🔐 SecureVision – Client-Side Encryption Model

SecureVision is a privacy-preserving video storage and playback system where **all encryption and decryption are performed on the client side**, and the server acts only as a **zero-knowledge encrypted storage provider**.

---

## 📌 System Overview

In this version:

- Videos are encrypted **locally in the user’s browser**
- The encryption password **never leaves the client**
- Only encrypted video files (`.enc`) are uploaded to the server
- The server cannot decrypt or view the video content
- Decryption occurs **in-memory on the client** during playback

This architecture follows **zero-trust and zero-knowledge security principles** used in modern cloud systems.

---

## ✨ Features

- Client-side AES-256-GCM video encryption  
- Password-based key derivation using PBKDF2 (SHA-256)  
- Zero-knowledge server-side encrypted storage  
- In-memory client-side decryption for secure playback  
- Authenticated encryption with integrity protection  

---

## 🔐 Security Model

- Encryption Algorithm: **AES-256-GCM**
- Key Derivation Function: **PBKDF2 (SHA-256)**
- Cryptographic Operations: **Client (Browser)**
- Password Storage/Transmission: ❌ Never stored or sent
- Server Trust Assumption: **Untrusted / Zero-Knowledge**

> Even if the server is compromised, encrypted video data remains confidential.

---

## 🧰 Tech Stack

- **Frontend:** HTML5, JavaScript
- **Cryptography:** Web Crypto API (AES-GCM, PBKDF2)
- **Backend:** Python (Flask)
- **Storage:** Server-side encrypted file storage

---

## 🌿 Branch Information

This implementation is available in the following Git branch:
