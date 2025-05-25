import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const UploadedFiles = () => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const fetchFiles = async () => {
    try {
      const response = await axios.get("http://localhost:5000/api/files/list");
      setFiles(response.data.files);
    } catch (error) {
      console.error("Error fetching files:", error);
    } finally {
      setLoading(false);
    }
  };

  const deleteFile = async (id, filename) => {
    const confirmDelete = window.confirm(
      `Are you sure you want to delete "${filename}"?`
    );
    if (!confirmDelete) return;

    try {
      await axios.delete(`http://localhost:5000/api/files/delete/${id}`);
      alert("✅ File deleted successfully.");
      fetchFiles(); // Refresh list
    } catch (error) {
      console.error("❌ Error deleting file:", error);
      alert("⚠️ Failed to delete file.");
    }
  };

  useEffect(() => {
    fetchFiles();
  }, []);

  return (
    <div className="bg-gradient-to-b from-green-100 via-green-50 to-white p-6 rounded-lg shadow-lg mt-6">
      {/* Heading + Add KB Button */}
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold text-green-700 flex items-center gap-2">
          📁 Uploaded Files
        </h2>
        <button
          onClick={() => navigate("/upload")}
          className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded shadow"
        >
          ➕ Add New KB
        </button>
      </div>

      {/* Table or Fallback */}
      {loading ? (
        <p className="text-center">Loading...</p>
      ) : files.length === 0 ? (
        <p className="text-center text-gray-500">No files uploaded yet.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left text-gray-600">
            <thead className="text-xs text-gray-700 uppercase bg-gray-100">
              <tr>
                <th className="px-6 py-3">Filename</th>
                <th className="px-6 py-3">Uploaded At</th>
                <th className="px-6 py-3 text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              {files.map((file, index) => (
                <tr key={index} className="bg-white border-b hover:bg-gray-50">
                  <td className="px-6 py-4 font-medium text-gray-800">
                    <span className="inline-block bg-green-100 text-green-700 px-2 py-1 rounded text-xs font-mono">
                      {file.dataSourceName || file.filename}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    {new Date(file.timestamp).toLocaleString("en-IN", {
                      timeZone: "Asia/Kolkata",
                      year: "numeric",
                      month: "short",
                      day: "numeric",
                      hour: "2-digit",
                      minute: "2-digit",
                      second: "2-digit",
                      hour12: true,
                    })}
                  </td>
                  <td className="px-6 py-4 text-center space-x-2">
                    <a
                      href={`http://localhost:5000/uploads/${file.filename}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="bg-yellow-500 text-white px-3 py-1 rounded hover:bg-yellow-600"
                    >
                      View
                    </a>
                    <a
                      href={`http://localhost:5000/uploads/${file.filename}`}
                      download={file.filename}
                      className="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-700"
                    >
                      Download
                    </a>
                    {file.id && (
                      <button
                        onClick={() => deleteFile(file.id, file.filename)}
                        className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-700"
                      >
                        Delete
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default UploadedFiles;
