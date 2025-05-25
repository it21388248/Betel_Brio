import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <header className="bg-green-700 text-white py-4 px-8 flex justify-between items-center shadow-md">
      <h1 className="text-2xl font-bold">BetelBrio</h1>
      <nav className="space-x-6">
        <Link to="/" className="hover:underline">
          Home
        </Link>
        <a href="#about" className="hover:underline">
          About
        </a>
        <a href="#contact" className="hover:underline">
          Contact
        </a>
        <Link to="/files" className="hover:underline">
          Knowledgebases
        </Link>
      </nav>
    </header>
  );
};

export default Navbar;
