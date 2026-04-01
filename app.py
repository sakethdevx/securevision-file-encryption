from flask import Flask, request, send_file, render_template, send_from_directory, abort
from crypto_utils import encrypt_with_password, decrypt_with_password
from cryptography.exceptions import InvalidTag
from io import BytesIO

app = Flask(__name__)

DIAGRAM_FILES = {
    "crypto": "cryptographic architecture.svg",
    "full": "full architecture.svg",
}

@app.route("/")
def home():
    return render_template("main.html")


@app.route("/diagram/<diagram_id>")
def get_diagram(diagram_id):
    filename = DIAGRAM_FILES.get(diagram_id)
    if not filename:
        abort(404)
    return send_from_directory(app.root_path, filename, mimetype="image/svg+xml")


@app.route("/encrypt", methods=["POST"])
def encrypt():
    uploaded_file = request.files.get("file") or request.files.get("video")
    if not uploaded_file:
        return "❌ Missing file", 400
    file_bytes = uploaded_file.read()
    password = request.form["key"]

    encrypted = encrypt_with_password(
        file_bytes,
        password,
        original_filename=uploaded_file.filename,
        mime_type=uploaded_file.mimetype,
    )

    return send_file(
        BytesIO(encrypted),
        as_attachment=True,
        download_name=f"{uploaded_file.filename}.enc" if uploaded_file.filename else "encrypted_file.enc",
        mimetype="application/octet-stream"
    )


@app.route("/decrypt", methods=["POST"])
def decrypt():
    try:
        uploaded_file = request.files.get("file") or request.files.get("video")
        if not uploaded_file:
            return "❌ Missing encrypted file", 400

        enc_file = uploaded_file.read()
        password = request.form["key"]

        decrypted, metadata = decrypt_with_password(enc_file, password)

        return send_file(
            BytesIO(decrypted),
            as_attachment=True,
            download_name=metadata.get("filename", "decrypted_file"),
            mimetype=metadata.get("mime_type", "application/octet-stream")
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