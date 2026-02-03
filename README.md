# 🔐 SecureVision – Client-Side Encryption Model

SecureVision is a privacy-focused video encryption and playback system that performs
**100% client-side cryptographic operations**, with **zero data transmission to servers**,
and provides **transparent client-visible audit logs**.

---

## 📌 System Overview

In this model:

- The client encrypts videos entirely in the browser using Web Crypto API
- No video data is ever uploaded to any server
- All encryption/decryption happens on the user's device
- Encrypted files are saved directly to the user's device
- For decryption, the process happens entirely client-side
- The decrypted video can be played in-browser or downloaded
- All major actions are logged and visible to the client

This architecture represents a **zero-knowledge encryption system** with complete client control.

---

## ✨ Features

- Client-side AES-256-GCM encryption and decryption using Web Crypto API
- Zero server communication for crypto operations
- Complete user privacy - no data leaves the device
- Client-controlled encryption and decryption keys
- Play or download decrypted video directly in browser
- Authenticated encryption with integrity protection
- Separate, user-visible detailed logs for:
  - Encryption
  - Decryption
  - Playback
  - Downloads  

---

## 🔐 Security Model

- Encryption Algorithm: **AES-256-GCM**
- Key Derivation: **SHA-256 (password-derived)**
- Cryptographic Execution: **100% Client-side (browser)**
- Data Transmission: ❌ None (completely offline after page load)
- Server Storage: ❌ None
- Key Storage: ❌ None (user must remember password)
- Integrity Protection: ✅ Yes (AES-GCM authentication)

> Complete zero-knowledge architecture - the server never sees any video data or keys.

---

## 📜 Client-Visible Audit Logs

The system provides **optional detailed logs** visible in the browser UI, including:

- Encryption start and completion
- Decryption start and completion
- File sizes and filenames
- Processing confirmations
- Playback events
- Download initiation and completion
- Error conditions (wrong key, corrupted file)

Logs can be **shown or hidden independently** for encryption and decryption.

---

## 🧰 Tech Stack

- **Backend:** Python (Flask) - serves static HTML only
- **Cryptography:** Web Crypto API (browser-native AES-GCM)
- **Frontend:** HTML5, JavaScript (client-side encryption)
- **Architecture:** Zero-knowledge, client-side processing

---

## 🏗 Architecture Summary

| Component | Responsibility |
|--------|---------------|
| Client | All encryption, decryption, file selection, playback, download |
| Server | Serves static HTML only (no crypto operations) |
| Storage | ❌ None on server |
| Data Transfer | ❌ No video data transmitted |
| Logs | Client-visible, non-persistent |

---

## 🎓 Academic Significance

This model demonstrates:

- True zero-knowledge architecture
- Client-side cryptographic operations using Web Crypto API
- Secure multimedia handling without any server involvement
- Client-managed file lifecycle with complete privacy
- Bandwidth efficiency (no uploads/downloads to server)
- Comparison-ready design alongside:
  - Server-side encryption models
  - Server-side storage models

---

## 💡 Key Benefits

1. **Zero Bandwidth Usage**: No video uploads/downloads to server
2. **Complete Privacy**: Server never sees video content or keys
3. **Offline Capable**: Works without internet after initial page load
4. **Fast Processing**: No network latency for encryption operations
5. **Scalable**: Server only serves static HTML (minimal resources)

---

## 🚀 Usage

1. Install dependencies: `pip install flask cryptography`
2. Run the server: `python app.py`
3. Open browser to `http://localhost:5000`
4. Select a video file and enter a password
5. Click "Encrypt & Download" - encryption happens in your browser
6. The encrypted file (.enc) is saved to your device
7. To decrypt: upload the .enc file, enter the same password, and play or download

**Important**: All encryption/decryption happens in your browser. The server only serves the HTML page!

---

## 🧠 Correct Technical Classification

> **Zero-knowledge client-side encryption with complete privacy and no server involvement in cryptographic operations.**

---

## ✅ Status

- Stable
- Fully functional
- Demonstration-ready
- Viva-ready
- Privacy-focused
- Bandwidth-efficient

---

## 🚀 Future Enhancements (Optional)

- Log export (TXT / JSON)
- Encryption & decryption timing metrics
- Password strength indicators
- Client-side hashing verification
- Role-based access controls

---

© SecureVision Project
