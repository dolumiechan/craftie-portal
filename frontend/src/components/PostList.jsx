import React from 'react';
import PostCard from './PostCard';

export default function PostList({ posts, loading, page, setPage, hasMore }) {
  if (loading) return <div style={styles.center}>⏳ Загрузка постов...</div>;
  if (!posts || posts.length === 0) return <div style={styles.center}>🤷‍♂️ Постов не найдено. Смените фильтры.</div>;

  return (
    <div>
      <div style={styles.grid}>
        {posts.map((post) => (
          <PostCard key={post.id} post={post} />
        ))}
      </div>

      {/* Пагинация */}
      <div style={styles.pagination}>
        <button 
          onClick={() => setPage(p => Math.max(p - 1, 1))} 
          disabled={page === 1}
          style={styles.button}
        >
          ⬅️ Назад
        </button>
        <span style={styles.pageNumber}>Страница {page}</span>
        <button 
          onClick={() => setPage(p => p + 1)} 
          disabled={!hasMore}
          style={styles.button}
        >
          Вперед ➡️
        </button>
      </div>
    </div>
  );
}

const styles = {
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '24px', marginBottom: '32px' },
  center: { textAlign: 'center', padding: '40px', fontSize: '16px', color: '#666' },
  pagination: { display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '16px', marginTop: '20px' },
  button: { padding: '8px 16px', borderRadius: '6px', border: '1px solid #ccc', backgroundColor: '#fff', cursor: 'pointer' },
  pageNumber: { fontSize: '15px', fontWeight: 'bold' }
};