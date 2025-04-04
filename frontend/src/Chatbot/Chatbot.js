import React, { useState } from "react";
import axios from "axios";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { FaPaperPlane, FaRobot, FaUser } from "react-icons/fa";

const Chatbot = () => {
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: `Hello! I'm the Betel Bot, your assistant for betel farming. You can ask me anything about betel cultivation, or use the buttons below for guided recommendations.`,
    },
  ]);
  const [input, setInput] = useState("");
  const [options, setOptions] = useState([]);
  const [showDatePicker, setShowDatePicker] = useState(false);
  const [selectedDate, setSelectedDate] = useState(null);

  const fieldOptions = {
    Leaf_Type: ["Peedichcha", "Korikan", "Keti", "Raan Keti"],
    Leaf_Size: ["Small", "Medium", "Large"],
    Quality_Grade: ["Ash", "Dark"],
    Location: ["Kuliyapitiya", "Naiwala", "Apaladeniya"],
    Season: ["Dry", "Rainy"],
  };

  const fieldMessageMap = {
    "what is the leaf type": "Leaf_Type",
    "what is the leaf size": "Leaf_Size",
    "what is the quality grade": "Quality_Grade",
    "what is your location": "Location",
    "what season is it": "Season",
  };

  const sendMessage = async (customMessage) => {
    const userMessage = customMessage || input;
    if (!userMessage.trim()) return;

    setMessages((prev) => [...prev, { sender: "user", text: userMessage }]);
    setInput("");
    setOptions([]);
    setShowDatePicker(false);

    try {
      const response = await axios.post("http://localhost:5000/api/chat/", {
        message: userMessage,
        session_id: "user1",
      });

      const botText = response.data?.reply || "⚠️ No reply from bot.";
      setMessages((prev) => [...prev, { sender: "bot", text: botText }]);

      const lowerText = botText.toLowerCase();

      const matchedMessageKey = Object.keys(fieldMessageMap).find((pattern) =>
        lowerText.includes(pattern)
      );

      if (matchedMessageKey) {
        const matchedField = fieldMessageMap[matchedMessageKey];
        setOptions(fieldOptions[matchedField] || []);
      }

      if (
        lowerText.includes("which date") ||
        lowerText.includes("yyyy-mm-dd") ||
        lowerText.includes("date")
      ) {
        setShowDatePicker(true);
      }

      if (response.data?.options) {
        const backendOptions = response.data.options.map((opt) => opt.value);
        setOptions(backendOptions);
      }
    } catch (error) {
      console.error("❌ Error from backend:", error);
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "⚠️ Error: Could not get a response.",
        },
      ]);
    }
  };

  const handleOptionClick = (value) => {
    sendMessage(value);
    setOptions([]);
  };

  const handleDateChange = (date) => {
    const formattedDate = date.toISOString().split("T")[0];
    setSelectedDate(date);
    setShowDatePicker(false);
    sendMessage(formattedDate);
  };

  return (
    <div className="max-w-xl mx-auto mt-10 border rounded-lg shadow-md overflow-hidden">
      {/* Header */}
      <div className="bg-green-700 text-white text-lg font-semibold px-6 py-3 flex items-center gap-2">
        <span className="text-xl">🍃</span> Betel Bot Chat
      </div>

      {/* Messages */}
      <div className="h-96 overflow-y-auto bg-white px-4 py-3">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`mb-4 flex items-end ${
              msg.sender === "user" ? "justify-end" : "justify-start"
            }`}
          >
            {/* Bot Avatar */}
            {msg.sender === "bot" && (
              <div className="flex-shrink-0 w-9 h-9 rounded-full bg-green-700 text-white flex items-center justify-center mr-2">
                <FaRobot className="text-lg" />
              </div>
            )}

            {/* Message Bubble */}
            <div
              className={`px-4 py-2 max-w-[75%] rounded-xl ${
                msg.sender === "user"
                  ? "bg-green-700 text-white text-right rounded-br-none"
                  : "bg-gray-100 text-black rounded-bl-none"
              }`}
            >
              {msg.text}
            </div>

            {/* User Avatar */}
            {msg.sender === "user" && (
              <div className="flex-shrink-0 w-9 h-9 rounded-full bg-amber-700 text-white flex items-center justify-center ml-2">
                <FaUser className="text-lg" />
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Options (Carousel Buttons) */}
      {options.length > 0 && (
        <div className="flex flex-wrap justify-center gap-2 px-4 py-2 bg-gray-50">
          {options.map((value, index) => (
            <button
              key={index}
              onClick={() => handleOptionClick(value)}
              className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
            >
              {value}
            </button>
          ))}
        </div>
      )}

      {/* Date Picker */}
      {showDatePicker && (
        <div className="px-4 py-2 text-center bg-gray-50">
          <DatePicker
            selected={selectedDate}
            onChange={handleDateChange}
            placeholderText="Select a date"
            className="border p-2 rounded w-full"
            dateFormat="yyyy-MM-dd"
          />
        </div>
      )}

      {/* Input */}
      <div className="flex items-center px-4 py-3 bg-gray-100 border-t">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about betel cultivation..."
          className="flex-grow px-4 py-2 border rounded-l-md focus:outline-none"
        />
        <button
          onClick={() => sendMessage()}
          className="bg-green-600 text-white px-4 py-2 rounded-r-md hover:bg-green-700"
        >
          <FaPaperPlane />
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
