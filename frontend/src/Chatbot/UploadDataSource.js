import React, { useState } from "react";
import axios from "axios";
import LoadingPopup from "../popups/LoadingPopup";

const UploadDataSource = ({ onClose, onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [dataSourceName, setDataSourceName] = useState("");
  const [message, setMessage] = useState("");
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file || !dataSourceName.trim()) {
      setMessage("Please enter a name and select a file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("dataSourceName", dataSourceName);

    try {
      setIsUploading(true);
      const response = await axios.post(
        "http://betelbrio-production.up.railway.app:5000/api/files/upload",
        formData
      );
      setMessage(response.data.message);
      setFile(null);
      setDataSourceName("");
      onUploadSuccess && onUploadSuccess(); // Optional callback
      onClose && onClose(); // Close modal after upload
    } catch (error) {
      console.error("❌ Upload failed:", error);
      setMessage("❌ Error uploading file.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <>
      {isUploading && <LoadingPopup message="Uploading..." subText="Hang tight!" />}

      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
        <div className="bg-white w-[400px] p-6 rounded-lg shadow-lg relative">
          <h2 className="text-xl font-bold mb-4 text-center">Upload a Data Source</h2>

          <input
            type="text"
            placeholder="Enter data source name"
            value={dataSourceName}
            onChange={(e) => setDataSourceName(e.target.value)}
            className="mb-4 p-2 w-full border rounded"
          />

          <input
            type="file"
            onChange={handleFileChange}
            accept=".pdf,.txt,.doc,.docx,.csv"
            className="mb-4 p-2 w-full border rounded"
          />

          {message && <p className="text-sm text-red-500 text-center mb-2">{message}</p>}

          <div className="flex justify-end space-x-2">
            <button
              className="px-4 py-2 border rounded"
              onClick={onClose}
              disabled={isUploading}
            >
              Cancel
            </button>
            <button
              onClick={handleUpload}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
              disabled={isUploading}
            >
              Upload
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

export default UploadDataSource;
