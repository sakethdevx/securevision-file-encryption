from flask import Flask, request, render_template, send_file
import os
from crypto_utils import encrypt_video, decrypt_video
from io import BytesIO

app = Flask(__name__)
UPLOAD_FOLDER = "storage/encrypted_videos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("main.html")

@app.route("/upload", methods=["POST"])
def upload():
    video = request.files["video"]
    password = request.form["password"]

    encrypted = encrypt_video(video.read(), password)
    filename = video.filename + ".enc"

    with open(os.path.join(UPLOAD_FOLDER, filename), "wb") as f:
        f.write(encrypted)

    return f"Encrypted & Stored as {filename}"

@app.route("/play")
def play_page():
    return render_template("play.html")

@app.route("/decrypt", methods=["POST"])
def decrypt():
    filename = request.form["filename"]
    password = request.form["password"]

    with open(os.path.join(UPLOAD_FOLDER, filename), "rb") as f:
        enc_data = f.read()

    try:
        decrypted = decrypt_video(enc_data, password)
        return send_file(
            BytesIO(decrypted),
            mimetype="video/mp4",
            as_attachment=False
        )
    except:
        return "❌ Incorrect password or tampered video"

if __name__ == "__main__":
    app.run(debug=True)