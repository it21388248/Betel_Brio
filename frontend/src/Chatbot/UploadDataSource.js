import React, { useState } from "react";
import axios from "axios";
import { FaCloudUploadAlt } from "react-icons/fa";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const UploadDataSource = ({ onClose, onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [dataSourceName, setDataSourceName] = useState("");
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file || !dataSourceName.trim()) {
      toast.warning("⚠️ Please enter a name and select a file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("dataSourceName", dataSourceName);

    try {
      setIsUploading(true);
      const response = await axios.post(
        "http://localhost:5000/api/files/upload",
        formData
      );
      toast.success(" File uploaded and indexed!");
      setFile(null);
      setDataSourceName("");
      onUploadSuccess && onUploadSuccess();
      onClose && onClose();
    } catch (error) {
      console.error("❌ Upload failed:", error);
      toast.error("❌ Error uploading file.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <>
      {/* Modal Background */}
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-gradient-to-b from-green-100 via-green-50 to-white">
        <div className="bg-white w-[500px] p-6 rounded-lg shadow-xl text-center">
          {/* Heading */}
          <h2 className="text-2xl font-bold text-green-700 mb-2">
            Upload Knowledge Base Files
          </h2>
          <p className="mb-4 text-gray-600 text-sm">
            Add documents, PDFs, and other files to enhance your BetelBrio AI
            with agricultural expertise.
          </p>

          {/* Upload Box */}
          <div className="border-2 border-dashed border-green-400 bg-green-50 p-6 rounded-lg mb-4">
            <div className="flex flex-col items-center">
              <FaCloudUploadAlt className="text-green-600 text-4xl mb-2" />
              <p className="text-gray-800 font-semibold mb-1">
                Drop your files here
              </p>
              <p className="text-sm text-gray-500">
                or click to browse from your computer
              </p>
              <input
                type="file"
                accept=".pdf,.txt,.doc,.docx,.csv,.xls,.xlsx"
                onChange={handleFileChange}
                className="mt-4 mb-2"
              />
              <p className="text-xs text-gray-500">
                PDF, DOC | TXT, CSV | XLSX, XLS
              </p>
            </div>
          </div>

          {/* Data Source Name Input */}
          <input
            type="text"
            placeholder="Enter data source name"
            value={dataSourceName}
            onChange={(e) => setDataSourceName(e.target.value)}
            className="mb-4 p-2 w-full border rounded"
          />

          {/* Action Buttons */}
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
              className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
              disabled={isUploading}
            >
              {isUploading ? "Uploading..." : "Upload"}
            </button>
          </div>
        </div>
      </div>

      {/* Toast Popup */}
      <ToastContainer
        position="top-right"
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        pauseOnHover
        theme="light"
      />
    </>
  );
};

export default UploadDataSource;
