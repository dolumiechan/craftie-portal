import { useCallback, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { fetchMyPosts, confirmDeletePost } from '../api/posts';
import { getPostDisplay } from '../utils/post';

export default function MyPosts() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      setPosts(await fetchMyPosts());
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const handleDelete = async (id, title) => {
    const deleted = await confirmDeletePost(id, title);
    if (deleted) {
      setPosts((prev) => prev.filter((p) => p.id !== id));
    }
  };

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <h1 className="text-2xl font-bold text-craft-brown">Мои публикации</h1>
        <Link
          to="/posts/new"
          className="rounded-full bg-craft-brown px-5 py-2 text-sm font-semibold text-white hover:opacity-90"
        >
          + Новая работа
        </Link>
      </div>

      {loading && <p className="text-sm text-craft-brown/70">Загрузка…</p>}

      {!loading && !posts.length && (
        <p className="text-sm text-craft-brown/70">
          Пока нет публикаций.{' '}
          <Link to="/posts/new" className="font-medium underline">
            Создать первую
          </Link>
        </p>
      )}

      <ul className="space-y-4">
        {posts.map((post) => {
          const { title, imageUrl, createdAt, categoryName } = getPostDisplay(post);
          return (
            <li
              key={post.id}
              className="flex gap-4 rounded-2xl border-2 border-craft-brown bg-craft-beige p-4"
            >
              <div className="h-20 w-20 shrink-0 overflow-hidden rounded-xl bg-craft-thumb">
                {imageUrl ? (
                  <img src={imageUrl} alt="" className="h-full w-full object-cover" />
                ) : null}
              </div>
              <div className="min-w-0 flex-1">
                <Link
                  to={`/posts/${post.id}`}
                  className="font-semibold text-craft-brown hover:underline"
                >
                  {title}
                </Link>
                <p className="mt-1 text-xs text-craft-brown/60">
                  {categoryName}
                  {createdAt && ` · ${createdAt}`}
                </p>
                <div className="mt-3 flex flex-wrap gap-2">
                  <Link
                    to={`/posts/${post.id}/edit`}
                    className="rounded-full border border-craft-brown px-3 py-1 text-xs font-medium text-craft-brown hover:bg-craft-cream"
                  >
                    Изменить
                  </Link>
                  <button
                    type="button"
                    onClick={() => handleDelete(post.id, title)}
                    className="rounded-full border border-red-800/40 px-3 py-1 text-xs font-medium text-red-900 hover:bg-red-50"
                  >
                    Удалить
                  </button>
                </div>
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
