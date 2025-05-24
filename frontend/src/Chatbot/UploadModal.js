import React, { useState } from "react";
import axios from "axios";
import LoadingPopup from "../popups/LoadingPopup";

const UploadModal = ({ onClose, onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [dataSourceName, setDataSourceName] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [message, setMessage] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file || !dataSourceName.trim()) {
      setMessage("Please enter a name and select a file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("dataSourceName", dataSourceName);

    setIsUploading(true);
    setMessage("");

    try {
      const response = await axios.post(
        "http://betelbrio-production.up.railway.app/api/files/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      onUploadSuccess();
      onClose();
    } catch (error) {
      console.error("Error uploading file:", error);
      setMessage("❌ Error uploading file.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <>
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
        <div className="bg-white w-[400px] p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-bold mb-4">New Data Source</h2>

          <div className="mb-4">
            <label className="block text-sm font-medium mb-1">Name</label>
            <input
              type="text"
              value={dataSourceName}
              onChange={(e) => setDataSourceName(e.target.value)}
              placeholder="Name of the data source"
              className="w-full border border-gray-300 px-3 py-2 rounded"
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium mb-1">File</label>
            <input
              type="file"
              accept=".pdf,.doc,.docx,.txt,.csv"
              onChange={handleFileChange}
              className="w-full border border-dashed px-3 py-2 rounded cursor-pointer"
            />
            <p className="text-sm text-gray-500 mt-1">
              Supported: .pdf, .doc, .docx, .txt, .csv
            </p>
          </div>

          {message && (
            <p className="text-center text-red-500 text-sm mb-2">{message}</p>
          )}

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
              Save Data Source
            </button>
          </div>
        </div>
      </div>

      {isUploading && <LoadingPopup message="Uploading file..." />}
    </>
  );
};

export default UploadModal;
