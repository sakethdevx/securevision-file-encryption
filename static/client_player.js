async function uploadEncrypted() {
    console.log("Upload clicked");

    const fileInput = document.getElementById("videoFile");
    const passwordInput = document.getElementById("encPassword");

    if (!fileInput || !passwordInput) {
        alert("Input elements not found");
        return;
    }

    const file = fileInput.files[0];
    const password = passwordInput.value;

    if (!file || !password) {
        alert("Please select a video and enter a password");
        return;
    }

    try {
        const encryptedBlob = await encryptVideo(file, password);

        const formData = new FormData();
        formData.append("file", encryptedBlob, file.name + ".enc");

        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        if (!response.ok) throw new Error("Upload failed");

        alert("✅ Encrypted video uploaded successfully");
    } catch (err) {
        console.error(err);
        alert("❌ Encryption or upload failed");
    }
}

async function playEncrypted(filename) {
    const password = document.getElementById("decPassword").value;

    if (!filename || !password) {
        alert("Please enter filename and password");
        return;
    }

    try {
        const response = await fetch(`/video/${filename}`);
        if (!response.ok) throw new Error("File not found");

        const encryptedBlob = await response.blob();
        const decryptedBlob = await decryptVideo(encryptedBlob, password);

        const videoURL = URL.createObjectURL(decryptedBlob);
        const video = document.getElementById("videoPlayer");

        video.src = videoURL;
        video.play();
    } catch (err) {
        console.error(err);
        alert("❌ Decryption failed (wrong password or corrupted file)");
    }
}