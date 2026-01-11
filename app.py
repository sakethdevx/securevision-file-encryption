from flask import Flask, request, send_from_directory, render_template
import os

app = Flask(__name__)
UPLOAD_FOLDER = "storage/client_encrypted"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("main.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return "Encrypted video stored successfully"

@app.route("/video/<filename>")
def serve_video(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)