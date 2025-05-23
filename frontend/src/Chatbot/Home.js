import React, { useState } from "react";
import UploadModal from "./UploadModal";
import UploadedFiles from "./UploadedFiles";

const Home = () => {
  const [showModal, setShowModal] = useState(false);
  const [refresh, setRefresh] = useState(false);

  const handleUploadSuccess = () => {
    setRefresh(!refresh); // Trigger re-fetching uploaded files
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">📂 Knowledge</h1>
        <button
          className="px-4 py-2 bg-blue-600 text-white rounded-lg"
          onClick={() => setShowModal(true)}
        >
          + New Data Source
        </button>
      </div>

      {showModal && (
        <UploadModal
          onClose={() => setShowModal(false)}
          onUploadSuccess={handleUploadSuccess}
        />
      )}
      <UploadedFiles key={refresh} />
    </div>
  );
};

export default Home;
