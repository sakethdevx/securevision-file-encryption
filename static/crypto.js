async function deriveKey(password, salt) {
    const enc = new TextEncoder();
    const baseKey = await crypto.subtle.importKey(
        "raw",
        enc.encode(password),
        "PBKDF2",
        false,
        ["deriveKey"]
    );

    return crypto.subtle.deriveKey(
        {
            name: "PBKDF2",
            salt: salt,
            iterations: 100000,
            hash: "SHA-256"
        },
        baseKey,
        { name: "AES-GCM", length: 256 },
        false,
        ["encrypt", "decrypt"]
    );
}

async function encryptVideo(file, password) {
    const data = await file.arrayBuffer();
    const salt = crypto.getRandomValues(new Uint8Array(16));
    const iv = crypto.getRandomValues(new Uint8Array(12));
    const key = await deriveKey(password, salt);

    const encrypted = await crypto.subtle.encrypt(
        { name: "AES-GCM", iv },
        key,
        data
    );

    return new Blob([salt, iv, new Uint8Array(encrypted)]);
}

async function decryptVideo(blob, password) {
    const buffer = await blob.arrayBuffer();
    const salt = buffer.slice(0, 16);
    const iv = buffer.slice(16, 28);
    const data = buffer.slice(28);

    const key = await deriveKey(password, new Uint8Array(salt));

    const decrypted = await crypto.subtle.decrypt(
        { name: "AES-GCM", iv: new Uint8Array(iv) },
        key,
        data
    );

    return new Blob([decrypted], { type: "video/mp4" });
}