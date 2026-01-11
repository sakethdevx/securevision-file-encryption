async function playVideo() {
    const filename = document.getElementById("filename").value;
    const password = document.getElementById("password").value;
    const video = document.getElementById("videoPlayer");

    if (!filename || !password) {
        alert("Please enter filename and password");
        return;
    }

    try {
        const response = await fetch("/decrypt", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `filename=${encodeURIComponent(filename)}&password=${encodeURIComponent(password)}`
        });

        if (!response.ok) {
            throw new Error("Decryption failed");
        }

        const blob = await response.blob();
        const videoURL = URL.createObjectURL(blob);

        video.src = videoURL;
        video.play();

        // Revoke URL after playback ends (extra security)
        video.onended = () => {
            URL.revokeObjectURL(videoURL);
        };

    } catch (err) {
        alert("❌ Incorrect password or video access denied");
        console.error(err);
    }
}