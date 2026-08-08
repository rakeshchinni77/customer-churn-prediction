import React from 'react';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import './styles/app.css';

export default function App() {
  return (
    <div className="d-flex flex-column min-vh-100" style={{ backgroundColor: '#0b0f19' }}>
      <ToastContainer position="top-right" autoClose={4000} theme="dark" />
      <Navbar />
      <main className="flex-grow-1">
        <Home />
      </main>
      <Footer />
    </div>
  );
}
