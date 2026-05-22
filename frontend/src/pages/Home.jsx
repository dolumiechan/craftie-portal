import React, { useState, useEffect } from 'react';
import Filters from '../components/Filters';
import PostList from '../components/PostList';
import api from '../api/axios';

export default function Home() {
  const [posts, setPosts] = useState([]);
  const [categories, setCategories] = useState([]); // Сюда прилетят категории из БД
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Состояния для фильтрации и пагинации
  const [search, setSearch] = useState('');
  const [categoryId, setCategoryId] = useState(null);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);

  const POSTS_PER_PAGE = 6;

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await api.get('/categories/'); // Наш эндпоинт категорий
        setCategories(response.data);
      } catch (err) {
        console.error("Не удалось загрузить категории с бэкенда:", err);
      }
    };
    fetchCategories();
  }, []);

  useEffect(() => {
    setPage(1);
  }, [search, categoryId]);

  useEffect(() => {
    const fetchPosts = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await api.get('/posts/', {
          params: {
            page: page,
            size: POSTS_PER_PAGE,
            // Передаем category_id на бэкенд, только если он выбран (не null)
            category_id: categoryId || undefined, 
            search: search || undefined
          }
        });

        setPosts(response.data);
        setHasMore(response.data.length === POSTS_PER_PAGE);
      } catch (err) {
        console.error("Ошибка при получении постов:", err);
        setError("Не удалось загрузить публикации.");
      } finally {
        setLoading(false);
      }
    };

    fetchPosts();
  }, [page, categoryId, search]); // Срабатывает каждый раз, когда меняется категория, поиск или страница!

  return (
    <div>
      <h2 style={styles.title}>Лента творческих проектов</h2>
      
      <Filters 
        search={search} 
        setSearch={setSearch} 
        categoryId={categoryId} 
        setCategoryId={setCategoryId} 
        categories={categories}
      />

      {error && <div style={styles.error}>{error}</div>}

      {!error && (
        <PostList 
          posts={posts} 
          loading={loading} 
          page={page} 
          setPage={setPage} 
          hasMore={hasMore} 
        />
      )}
    </div>
  );
}

const styles = {
  title: { marginBottom: '24px', color: '#222', fontSize: '28px', fontWeight: '600' },
  error: { padding: '16px', backgroundColor: '#fff0f0', border: '1px solid #ffcccc', borderRadius: '8px', color: '#cc0000', textAlign: 'center', marginBottom: '20px' }
};