import React, { useState, useEffect } from "react";
import axios from "axios";

const ImageUploader = () => {
  const [image, setImage] = useState(null);
  const [uploadedImage, setUploadedImage] = useState(null);

  // Fetch the current image from the server
  useEffect(() => {
    axios.get("http://localhost:8000/get-image")
      .then(response => {
        setUploadedImage(response.data.image_url);
      })
      .catch(error => console.error(error));
  }, []);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", image);

    try {
      const response = await axios.post("http://localhost:8000/upload-image", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      setUploadedImage(response.data.image_url);
    } catch (error) {
      console.error("Error uploading image:", error);
    }
  };

  const handleUpdate = async () => {
    const formData = new FormData();
    formData.append("file", image);

    try {
      const response = await axios.put("http://localhost:8000/update-image", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      setUploadedImage(response.data.image_url);
    } catch (error) {
      console.error("Error updating image:", error);
    }
  };

  return (
    <div>
      <h1>Image Uploader</h1>
      <input type="file" onChange={(e) => setImage(e.target.files[0])} />
      <button onClick={handleUpload}>Upload</button>
      <button onClick={handleUpdate}>Update</button>
      {uploadedImage && <img src={`http://localhost:8000${uploadedImage}`} alt="Uploaded" />}
    </div>
  );
};

export default ImageUploader;
