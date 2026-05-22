import React from 'react';
import { Link } from 'react-router-dom';

export default function Header() {
  return (
    <header style={styles.header}>
      <div style={styles.container}>
        <Link to="/" style={styles.logo}>🧶 CraftiePortal</Link>
        <nav style={styles.nav}>
          <Link to="/" style={styles.link}>Главная</Link>
          <Link to="/profile" style={styles.link}>Профиль</Link>
          <Link to="/login" style={styles.loginBtn}>Войти</Link>
        </nav>
      </div>
    </header>
  );
}

const styles = {
  header: { backgroundColor: '#fff', borderBottom: '1px solid #e0e0e0', position: 'sticky', top: 0, zIndex: 100 },
  container: { maxWith: '1200px', margin: '0 auto', padding: '16px 24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' },
  logo: { fontSize: '22px', fontWeight: 'bold', color: '#ff7a00', textDecoration: 'none' },
  nav: { display: 'flex', alignItems: 'center', gap: '20px' },
  link: { textDecoration: 'none', color: '#555', fontWeight: '500' },
  loginBtn: { textDecoration: 'none', backgroundColor: '#ff7a00', color: '#fff', padding: '8px 16px', borderRadius: '20px', fontWeight: '500' }
};