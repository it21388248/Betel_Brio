import React from "react";
import { FaFacebook, FaTwitter, FaEnvelope, FaGithub } from "react-icons/fa";
import { Link } from "react-router-dom";

const Footer = () => {
  return (
    <footer className="bg-green-700 text-white py-8 mt-12">
      <div className="max-w-6xl mx-auto px-6 grid grid-cols-1 md:grid-cols-3 gap-8 text-sm">
        {/* About */}
        <div>
          <h4 className="text-lg font-semibold mb-2">About BetelBrio</h4>
          <p>
            A research-driven initiative to modernize betel cultivation through
            AI, market prediction, and disease detection.
          </p>
        </div>

        {/* Quick Links */}
        <div>
          <h4 className="text-lg font-semibold mb-2">Quick Links</h4>
          <ul className="space-y-2">
            <li>
              <a href="#features" className="hover:underline">
                Features
              </a>
            </li>
            <li>
              <a href="#about" className="hover:underline">
                About
              </a>
            </li>
            <li>
              <a href="#contact" className="hover:underline">
                Contact
              </a>
            </li>
            <li>
              <Link to="/files" className="hover:underline">
                Knowledgebases
              </Link>
            </li>
          </ul>
        </div>

        {/* Contact & Social */}
        <div>
          <h4 className="text-lg font-semibold mb-2">Connect with Us</h4>
          <p className="mb-2">📧 betelbrio@support.lk</p>
          <div className="flex space-x-4 text-white text-lg">
            <a
              href="https://facebook.com"
              target="_blank"
              rel="noopener noreferrer"
            >
              <FaFacebook />
            </a>
            <a
              href="https://twitter.com"
              target="_blank"
              rel="noopener noreferrer"
            >
              <FaTwitter />
            </a>
            <a href="mailto:betelbrio@support.lk">
              <FaEnvelope />
            </a>
            <a
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
            >
              <FaGithub />
            </a>
          </div>
        </div>
      </div>

      {/* Bottom */}
      <div className="text-center text-xs mt-8 border-t border-green-600 pt-4">
        © 2025 BetelBrio — All rights reserved.
      </div>
    </footer>
  );
};

export default Footer;
