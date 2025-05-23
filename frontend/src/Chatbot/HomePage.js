import React, { useState } from "react";
import {
  FaLeaf,
  FaCloudSunRain,
  FaChartLine,
  FaHeartbeat,
  FaComments,
  FaTimes,
} from "react-icons/fa";
import Chatbot from "./Chatbot";
import "react-datepicker/dist/react-datepicker.css";

const HomePage = () => {
  const [showChat, setShowChat] = useState(false);

  return (
    <div className="min-h-screen bg-white text-gray-800">
      {/* Navbar */}
      <header className="bg-green-700 text-white py-4 px-8 flex justify-between items-center">
        <h1 className="text-2xl font-bold">BetelBrio</h1>
        <nav className="space-x-6">
          <a href="#features" className="hover:underline">
            Features
          </a>
          <a href="#about" className="hover:underline">
            About
          </a>
          <a href="#contact" className="hover:underline">
            Contact
          </a>
        </nav>
      </header>

      {/* Hero Section */}
      <section className="text-center py-20 px-4 bg-gray-50">
        <h2 className="text-4xl font-bold text-green-700 mb-4">
          Empowering Betel Farmers with Smart AI Solutions
        </h2>
        <p className="max-w-2xl mx-auto text-lg">
          BetelBrio is your intelligent guide for modern betel farming. Explore
          our mobile app features to improve yield, predict the market, manage
          disease, and make data-driven decisions.
        </p>
      </section>

      {/* Features Section */}
      <section id="features" className="py-16 px-8 bg-white">
        <h3 className="text-3xl font-semibold text-center text-green-700 mb-12">
          App Features
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 max-w-6xl mx-auto">
          <div className="border p-6 rounded-lg shadow hover:shadow-lg transition-all">
            <FaChartLine className="text-green-700 text-4xl mb-4" />
            <h4 className="text-xl font-bold mb-2">Harvest Prediction</h4>
            <p>
              Estimate your harvest time and volume with AI-powered analysis to
              improve planning and reduce waste.
            </p>
          </div>
          <div className="border p-6 rounded-lg shadow hover:shadow-lg transition-all">
            <FaLeaf className="text-green-700 text-4xl mb-4" />
            <h4 className="text-xl font-bold mb-2">Market Prediction</h4>
            <p>
              Get smart predictions on the best location and time to sell your
              betel harvest for maximum profit.
            </p>
          </div>
          <div className="border p-6 rounded-lg shadow hover:shadow-lg transition-all">
            <FaCloudSunRain className="text-green-700 text-4xl mb-4" />
            <h4 className="text-xl font-bold mb-2">Weather & Recommendation</h4>
            <p>
              Receive tailored suggestions for watering, fertilizing, and crop
              protection based on current weather conditions.
            </p>
          </div>
          <div className="border p-6 rounded-lg shadow hover:shadow-lg transition-all">
            <FaHeartbeat className="text-green-700 text-4xl mb-4" />
            <h4 className="text-xl font-bold mb-2">Disease Management</h4>
            <p>
              Detect and identify diseases early using AI and receive actionable
              treatment recommendations.
            </p>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-16 px-8 bg-gray-50">
        <div className="max-w-3xl mx-auto text-center">
          <h3 className="text-3xl font-semibold text-green-700 mb-4">
            About the Project
          </h3>
          <p className="text-lg">
            This solution is part of a research-backed project aiming to
            modernize betel cultivation in Sri Lanka. With a Flutter-based
            mobile app and an intelligent chatbot assistant, we provide
            real-time insights to farmers across multiple domains.
          </p>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="py-16 px-8 bg-white">
        <div className="max-w-xl mx-auto text-center">
          <h3 className="text-3xl font-semibold text-green-700 mb-4">
            Get in Touch
          </h3>
          <p className="text-lg mb-4">
            Want to learn more or partner with us? Contact the BetelBrio team
            for demos, support, or collaborations.
          </p>
          <a
            href="mailto:betelbrio@support.lk"
            className="text-green-600 font-semibold hover:underline"
          >
            betelbrio@support.lk
          </a>
        </div>
      </section>

      <footer className="text-center py-4 text-sm text-gray-500 bg-gray-100">
        © 2025 BetelBrio — All rights reserved.
      </footer>

      {/* Chatbot Floating Widget */}
      <div className="fixed bottom-4 right-4 z-50">
        {showChat ? (
          <div className="relative w-96 rounded-xl overflow-hidden shadow-lg border border-green-600 bg-white">
            <div className="bg-green-700 text-white flex items-center justify-between px-4 py-3">
              <div className="font-bold text-lg flex items-center gap-2">
                <FaComments /> Betel Bot Chat
              </div>
              <button
                onClick={() => setShowChat(false)}
                title="Close chat"
                className="hover:bg-green-600 rounded-full p-1.5 transition border border-white"
              >
                <FaTimes className="text-white text-base" />
              </button>
            </div>
            <div className="max-h-[550px] overflow-y-auto">
              <Chatbot />
            </div>
          </div>
        ) : (
          <button
            className="bg-green-600 text-white p-4 rounded-full shadow-lg hover:bg-green-700"
            onClick={() => setShowChat(true)}
            title="Open chat"
          >
            <FaComments className="text-2xl" />
          </button>
        )}
      </div>
    </div>
  );
};

export default HomePage;
