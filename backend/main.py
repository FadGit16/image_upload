from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Configure upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:root@localhost:3306/mydatabase"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Image model
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(255), nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()

@app.route("/upload-image", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    # Save to database
    image = Image(file_path=f"/uploads/{file.filename}")
    db.session.add(image)
    db.session.commit()

    return jsonify({"image_url": image.file_path}), 201

@app.route("/get-image", methods=["GET"])
def get_image():
    image = Image.query.order_by(Image.id.desc()).first()
    if not image:
        return jsonify({"image_url": None}), 404
    return jsonify({"image_url": image.file_path})

@app.route("/update-image", methods=["PUT"])
def update_image():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    image = Image.query.order_by(Image.id.desc()).first()
    if not image:
        return jsonify({"error": "No image to update"}), 404

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    # Update database
    image.file_path = f"/uploads/{file.filename}"
    db.session.commit()

    return jsonify({"image_url": image.file_path}), 200

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
