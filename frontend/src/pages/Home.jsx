import { useState, useEffect } from 'react';
import PostList from '../components/home/PostList';
import RightSidebar from '../components/home/RightSidebar';
import Alert from '../components/ui/Alert';
import { fetchPosts } from '../api/posts';
import { getApiErrorMessage } from '../utils/apiError';
import api from '../api/axios';

const POSTS_PER_PAGE = 6;

export default function Home({ search = '' }) {
  const [posts, setPosts] = useState([]);
  const [total, setTotal] = useState(0);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [categoryId, setCategoryId] = useState(null);
  const [page, setPage] = useState(1);

  useEffect(() => {
    api
      .get('/categories/')
      .then((response) => setCategories(response.data))
      .catch(() => setCategories([]));
  }, []);

  useEffect(() => {
    setPage(1);
  }, [search, categoryId]);

  useEffect(() => {
    const loadPosts = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await fetchPosts({
          skip: (page - 1) * POSTS_PER_PAGE,
          limit: POSTS_PER_PAGE,
          categoryId,
          search,
        });
        setPosts(data.items);
        setTotal(data.total);
      } catch (err) {
        setError(
          getApiErrorMessage(err, 'Не удалось загрузить публикации. Проверьте, что бэкенд запущен.'),
        );
      } finally {
        setLoading(false);
      }
    };

    loadPosts();
  }, [page, categoryId, search]);

  const hasMore = page * POSTS_PER_PAGE < total;

  const handlePostDeleted = (postId) => {
    setPosts((prev) => prev.filter((post) => post.id !== postId));
    setTotal((prev) => Math.max(0, prev - 1));
  };

  return (
    <div className="flex h-full w-full flex-col overflow-hidden lg:flex-row lg:gap-8">
      <section className="flex min-h-0 min-w-0 flex-1 flex-col overflow-hidden" aria-label="Лента публикаций">
        {error && (
          <div className="mb-6 shrink-0">
            <Alert onDismiss={() => setError(null)}>{error}</Alert>
          </div>
        )}

        {!error && (
          <PostList
            posts={posts}
            loading={loading}
            page={page}
            total={total}
            setPage={setPage}
            hasMore={hasMore}
            onPostDeleted={handlePostDeleted}
          />
        )}
      </section>

      <div className="shrink-0">
        <RightSidebar
        categories={categories}
        categoryId={categoryId}
        setCategoryId={setCategoryId}
      />
      </div>
    </div>
  );
}
