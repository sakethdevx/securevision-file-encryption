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
- PBKDF2-HMAC-SHA256 key derivation with random salt and 150,000 iterations
- Zero server communication for crypto operations
- Complete user privacy - no data leaves the device
- Client-controlled encryption and decryption keys
- Play or download decrypted video directly in browser
- Self-contained encrypted package metadata (`.enc`) with KDF and crypto parameters
- File-level SHA-256 integrity verification after decryption
- Offline verification mode (no decryption): verifies encrypted payload hash from metadata
- Blockchain-style SHA-256 hash chain for tamper-evident UI audit logs
- Cryptographic proof panel with live algorithm, KDF, integrity and performance metrics
- Separate, user-visible detailed logs for:
  - Encryption
  - Decryption
  - Playback
  - Downloads  

---

## 🔐 Security Model

- Encryption Algorithm: **AES-256-GCM**
- Key Derivation: **PBKDF2-HMAC-SHA256 + random salt + 150,000 iterations**
- Cryptographic Execution: **100% Client-side (browser)**
- Data Transmission: ❌ None (completely offline after page load)
- Server Storage: ❌ None
- Key Storage: ❌ None (user must remember password)
- Integrity Protection: ✅ Yes (AES-GCM authentication + SHA-256 file hash verification)

Encrypted `.enc` package contains:

- Format marker (`SV01`)
- Metadata length + metadata JSON
- Salt, nonce (IV), KDF iterations, algorithm and file hash
- AES-GCM ciphertext payload

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

Each log line is linked using a **previous-hash → current-hash** chain (SHA-256),
making tampering detectable.

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
| Logs | Client-visible, hash-chained, non-persistent |

---

## 🎓 Academic Significance

This model demonstrates:

- True zero-knowledge architecture
- Client-side cryptographic operations using Web Crypto API
- Password-hardening via PBKDF2 against brute-force attacks
- Tamper detection via file hash verification and hash-chained audit logs
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
8. To verify without decryption: upload the .enc file and click **Offline Verify (No Decryption)**

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
- Password strength indicators
- Offline verification mode (verify package metadata/hash without playback)
- Role-based access controls

---

© SecureVision Project
