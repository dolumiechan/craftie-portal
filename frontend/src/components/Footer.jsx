import React from 'react';

export default function Footer() {
  return (
    <footer style={styles.footer}>
      <p>© {new Date().getFullYear()} CraftiePortal — Платформа для мастеров рукоделия.</p>
    </footer>
  );
}

const styles = {
  footer: { backgroundColor: '#333', color: '#fff', textAlign: 'center', padding: '20px', marginTop: 'auto', fontSize: '14px' }
};