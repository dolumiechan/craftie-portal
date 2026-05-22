import React from 'react';

export default function Filters({ search, setSearch, categoryId, setCategoryId, categories }) {
  return (
    <div style={styles.container}>
      {/* Поле поиска */}
      <input
        type="text"
        placeholder="Поиск по названию или описанию..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        style={styles.input}
      />
      
      {/* Выпадающий список категорий */}
      <select
        value={categoryId || ''}
        onChange={(e) => setCategoryId(e.target.value ? Number(e.target.value) : null)}
        style={styles.select}
      >
        <option value="">Все категории 🧶</option>
        {categories.map((cat) => (
          <option key={cat.id} value={cat.id}>
            {cat.name}
          </option>
        ))}
      </select>
    </div>
  );
}

const styles = {
  container: { display: 'flex', gap: '16px', marginBottom: '24px', flexWrap: 'wrap' },
  input: { flex: '1', minWidth: '200px', padding: '10px 16px', borderRadius: '8px', border: '1px solid #ccc', fontSize: '15px' },
  select: { padding: '10px 16px', borderRadius: '8px', border: '1px solid #ccc', backgroundColor: '#fff', fontSize: '15px', cursor: 'pointer', minWidth: '180px' }
};