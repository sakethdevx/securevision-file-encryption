from flask import Flask, request, send_file, render_template
from crypto_utils import encrypt_with_password, decrypt_with_password
from cryptography.exceptions import InvalidTag
from io import BytesIO

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("main.html")


@app.route("/encrypt", methods=["POST"])
def encrypt():
    video = request.files["video"].read()
    password = request.form["key"]

    encrypted = encrypt_with_password(video, password, original_filename=request.files["video"].filename)

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
        password = request.form["key"]

        decrypted, _ = decrypt_with_password(enc_file, password)

        return send_file(
            BytesIO(decrypted),
            as_attachment=True,
            download_name="decrypted_video.mp4",
            mimetype="video/mp4"
        )

    except InvalidTag:
        # Wrong password OR tampered file
        return "❌ Wrong decryption key or corrupted encrypted file", 401

    except ValueError as e:
        return f"❌ {str(e)}", 400

    except Exception:
        return "❌ Decryption failed due to server error", 500


if __name__ == "__main__":
    app.run(debug=True)