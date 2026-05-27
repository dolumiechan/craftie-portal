import { useCallback, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { fetchComments, createComment, deleteComment } from '../../api/comments';
import { formatPostDate } from '../../utils/post';
import { getApiErrorMessage } from '../../utils/apiError';

export default function CommentSection({ postId, onCountChange }) {
  const { isAuthenticated, user, isStaff } = useAuth();
  const [comments, setComments] = useState([]);
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const data = await fetchComments(postId);
      setComments(data);
      onCountChange?.(data.length);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [postId, onCountChange]);

  useEffect(() => {
    load();
  }, [load]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!text.trim()) return;
    setSubmitting(true);
    try {
      await createComment(postId, text.trim());
      setText('');
      await load();
    } catch (err) {
      console.error(err);
      alert(getApiErrorMessage(err, 'Не удалось отправить комментарий.'));
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (commentId) => {
    if (!window.confirm('Удалить комментарий?')) return;
    try {
      await deleteComment(commentId);
      await load();
    } catch (err) {
      console.error(err);
      alert(getApiErrorMessage(err, 'Не удалось удалить.'));
    }
  };

  const canDelete = (comment) =>
    isAuthenticated &&
    (comment.user_id === user?.id || isStaff);

  return (
    <section className="mt-8 border-t border-craft-brown/15 pt-6">
      <h2 className="text-lg font-semibold text-craft-brown">
        Комментарии {comments.length > 0 && `(${comments.length})`}
      </h2>

      {isAuthenticated ? (
        <form onSubmit={handleSubmit} className="mt-4 space-y-2">
          <textarea
            rows={3}
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Напишите отзыв…"
            className="w-full rounded-xl border-2 border-craft-brown/30 bg-white px-3 py-2 text-sm outline-none focus:border-craft-brown"
          />
          <button
            type="submit"
            disabled={submitting || !text.trim()}
            className="rounded-full bg-craft-brown px-4 py-2 text-sm font-medium text-white disabled:opacity-50"
          >
            {submitting ? 'Отправка…' : 'Отправить'}
          </button>
        </form>
      ) : (
        <p className="mt-3 text-sm text-craft-brown/70">
          <Link to="/login" className="font-medium underline">
            Войдите
          </Link>
          , чтобы оставить комментарий.
        </p>
      )}

      {loading ? (
        <p className="mt-4 text-sm text-craft-brown/60">Загрузка…</p>
      ) : (
        <ul className="mt-4 space-y-3">
          {comments.map((c) => (
            <li
              key={c.id}
              className="rounded-xl border border-craft-brown/15 bg-white px-4 py-3 text-sm"
            >
              <div className="flex items-start justify-between gap-2">
                <span className="font-medium text-craft-brown">
                  {c.author_username || 'Пользователь'}
                </span>
                <time className="shrink-0 text-xs text-craft-brown/50" dateTime={c.created_at}>
                  {formatPostDate(c.created_at)}
                </time>
              </div>
              <p className="mt-2 text-craft-brown/90">{c.text}</p>
              {canDelete(c) && (
                <button
                  type="button"
                  onClick={() => handleDelete(c.id)}
                  className="mt-2 text-xs text-red-800 hover:underline"
                >
                  Удалить
                </button>
              )}
            </li>
          ))}
          {!comments.length && (
            <li className="text-sm text-craft-brown/60">Пока нет комментариев.</li>
          )}
        </ul>
      )}
    </section>
  );
}
