import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../../api/axios';
import { formatPostDate } from '../../utils/post';

export default function CommentHistory() {
  const [myComments, setMyComments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    const load = async () => {
      setLoading(true);
      try {
        const { data } = await api.get('/profile/comments');
        if (!cancelled) setMyComments(data);
      } catch (err) {
        console.error(err);
        if (!cancelled) setMyComments([]);
      } finally {
        if (!cancelled) setLoading(false);
      }
    };

    load();
    return () => {
      cancelled = true;
    };
  }, []);

  if (loading) {
    return <p className="text-sm text-craft-brown/70">Загрузка комментариев…</p>;
  }

  if (!myComments.length) {
    return (
      <p className="text-sm text-craft-brown/70">
        Вы ещё не оставляли комментариев под работами.
      </p>
    );
  }

  return (
    <ul className="space-y-3">
      {myComments.map((c) => (
        <li
          key={c.id}
          className="rounded-xl border-2 border-craft-brown/15 bg-white p-4 text-sm"
        >
          <Link
            to={`/posts/${c.post_id}`}
            className="font-semibold text-craft-brown hover:underline"
          >
            {c.post_title}
          </Link>
          <p className="mt-2 text-craft-brown/90">{c.text}</p>
          <time className="mt-2 block text-xs text-craft-brown/55" dateTime={c.created_at}>
            {formatPostDate(c.created_at)}
          </time>
        </li>
      ))}
    </ul>
  );
}
