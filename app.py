from flask import Flask, request, send_file, render_template
from crypto_utils import encrypt_bytes, decrypt_bytes
from cryptography.exceptions import InvalidTag
from io import BytesIO
import hashlib

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("main.html")


@app.route("/encrypt", methods=["POST"])
def encrypt():
    video = request.files["video"].read()
    key = hashlib.sha256(request.form["key"].encode()).digest()

    encrypted = encrypt_bytes(video, key)

    return send_file(
        BytesIO(encrypted),
        as_attachment=True,
        download_name="video.enc",
        mimetype="application/octet-stream"
    )


@app.route("/decrypt", methods=["POST"])
def decrypt():
    try:
        enc_file = request.files["video"].read()
        key = hashlib.sha256(request.form["key"].encode()).digest()

        decrypted = decrypt_bytes(enc_file, key)

        return send_file(
            BytesIO(decrypted),
            as_attachment=True,
            download_name="decrypted_video.mp4",
            mimetype="video/mp4"
        )

    except InvalidTag:
        # Wrong password OR tampered file
        return "❌ Wrong decryption key or corrupted encrypted file", 401

    except Exception:
        return "❌ Decryption failed due to server error", 500


if __name__ == "__main__":
    app.run(debug=True)