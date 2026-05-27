import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { adminDeletePost, fetchAdminPosts, togglePostHidden } from '../../api/admin';
import { getPostDisplay } from '../../utils/post';

export default function AdminPosts() {
  const [data, setData] = useState({ items: [], total: 0 });
  const [loading, setLoading] = useState(true);

  const load = async () => {
    setLoading(true);
    try {
      setData(await fetchAdminPosts({ limit: 100 }));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const handleHide = async (id) => {
    try {
      await togglePostHidden(id);
      await load();
    } catch (err) {
      alert(err.response?.data?.detail || 'Ошибка');
    }
  };

  const handleDelete = async (id, title) => {
    if (!window.confirm(`Удалить «${title}»?`)) return;
    try {
      await adminDeletePost(id);
      await load();
    } catch (err) {
      alert(err.response?.data?.detail || 'Ошибка');
    }
  };

  if (loading) return <p className="text-sm text-craft-brown/70">Загрузка…</p>;

  return (
    <div className="space-y-4">
      <p className="text-sm text-craft-brown/70">Всего: {data.total}</p>
      <ul className="space-y-3">
        {data.items.map((post) => {
          const { title, authorName, createdAt } = getPostDisplay(post);
          return (
            <li
              key={post.id}
              className={`rounded-xl border-2 p-4 ${
                post.is_hidden
                  ? 'border-red-300/50 bg-red-50/50'
                  : 'border-craft-brown/20 bg-white'
              }`}
            >
              <div className="flex flex-wrap items-start justify-between gap-2">
                <div>
                  <Link to={`/posts/${post.id}`} className="font-semibold text-craft-brown hover:underline">
                    {title}
                  </Link>
                  <p className="text-xs text-craft-brown/60">
                    [{authorName}] · {createdAt}
                    {post.is_hidden && ' · скрыта'}
                  </p>
                </div>
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => handleHide(post.id)}
                    className="rounded-full border border-craft-brown px-3 py-1 text-xs font-medium"
                  >
                    {post.is_hidden ? 'Показать' : 'Скрыть'}
                  </button>
                  <button
                    type="button"
                    onClick={() => handleDelete(post.id, title)}
                    className="rounded-full border border-red-800/40 px-3 py-1 text-xs text-red-900"
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
