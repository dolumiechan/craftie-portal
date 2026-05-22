import React from 'react';

export default function PostCard({ post }) {
  const imageUrl = post.image_url || 'https://images.unsplash.com/photo-1513519245088-0e12902e5a38?q=80&w=400';

  return (
    <div style={styles.card}>
      <img src={imageUrl} alt={post.title} style={styles.image} />
      <div style={styles.content}>
        <span style={styles.category}>Категория: {post.category_name || post.category_id}</span>
        <h3 style={styles.title}>{post.title}</h3>
        <p style={styles.description}>
          {post.description?.length > 100 
            ? `${post.description.substring(0, 100)}...` 
            : post.description}
        </p>
        <div style={styles.footer}>
          <span style={styles.author}>👤 {post.author_username || 'Мастер'}</span>
          <span style={styles.likes}>❤️ {post.likes_count || 0}</span>
        </div>
      </div>
    </div>
  );
}

const styles = {
  card: { border: '1px solid #e0e0e0', borderRadius: '12px', overflow: 'hidden', backgroundColor: '#fff', boxShadow: '0 4px 6px rgba(0,0,0,0.05)', display: 'flex', flexDirection: 'column' },
  image: { width: '100%', height: '200px', objectFit: 'cover' },
  content: { padding: '16px', display: 'flex', flexDirection: 'column', flexGrow: 1 },
  category: { fontSize: '12px', color: '#ff7a00', fontWeight: 'bold', textTransform: 'uppercase', marginBottom: '8px' },
  title: { fontSize: '18px', margin: '0 0 8px 0', color: '#333' },
  description: { fontSize: '14px', color: '#666', lineHeight: '1.5', flexGrow: 1, marginBottom: '16px' },
  footer: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '13px', color: '#888', borderTop: '1px solid #f0f0f0', paddingTop: '12px' },
};