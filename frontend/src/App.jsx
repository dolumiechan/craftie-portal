import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';

// Здесь позже появятся импорты других страниц, например Login, Register, Profile, Admin...

export default function App() {
  return (
    <div style={styles.appWrapper}>
      <Header />
      
      <main style={styles.mainContent}>
        <Routes>
          {/* Главная страница с нашей лентой постов */}
          <Route path="/" element={<Home />} />
          
          {/* Сюда мы будем добавлять новые маршруты по ТЗ:
              <Route path="/login" element={<Login />} />
              <Route path="/profile" element={<Profile />} /> 
          */}
        </Routes>
      </main>

      <Footer />
    </div>
  );
}

const styles = {
  appWrapper: { display: 'flex', flexDirection: 'column', minHeight: '100vh', backgroundColor: '#f9f9f9' },
  mainContent: { flex: 1, maxWidth: '1200px', width: '100%', margin: '0 auto', padding: '32px 24px' }
};