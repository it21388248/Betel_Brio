import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import Chatbot from "./Chatbot/Chatbot";
import UploadPDF from "./Chatbot/UploadDataSource";
import Navbar from "./Chatbot/Navbar";
import UploadedFiles from "./Chatbot/UploadedFiles";
import Home from "./Chatbot/Home";
import UploadDataSource from "./Chatbot/UploadDataSource";
import HomePage from "./Chatbot/HomePage";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />

        <Route path="/chat" element={<Chatbot />} />
        <Route path="/upload" element={<UploadDataSource />} />
        <Route path="/files" element={<UploadedFiles />} />
      </Routes>
    </Router>
  );
}
