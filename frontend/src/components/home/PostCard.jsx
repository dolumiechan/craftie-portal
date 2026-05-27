import { useEffect, useRef, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { likePost, unlikePost } from '../../api/likes';
import { confirmDeletePost } from '../../api/posts';
import { useClickOutside } from '../../hooks/useClickOutside';
import { getPostDisplay } from '../../utils/post';
import { IconComment, IconHeart, IconMoreVertical } from '../ui/Icons';
export { useAuth } from '../context/AuthContext';

export default function PostCard({ post, onDeleted }) {
  const navigate = useNavigate();
  const { user, isStaff, isAuthenticated } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);
  const [likesCount, setLikesCount] = useState(post.likes_count ?? 0);
  const [isLiked, setIsLiked] = useState(Boolean(post.is_liked));
  const [liking, setLiking] = useState(false);
  const menuRef = useRef(null);

  const {
    id,
    title,
    description,
    authorName,
    categoryName,
    imageUrl,
    createdAt,
    commentsCount,
  } = getPostDisplay(post);

  useEffect(() => {
    setLikesCount(post.likes_count ?? 0);
    setIsLiked(Boolean(post.is_liked));
  }, [post.id, post.likes_count, post.is_liked]);

  const canManage = Boolean(user && (user.id === post.author_id || isStaff));

  useClickOutside(menuRef, () => setMenuOpen(false), menuOpen && canManage);

  const handleDelete = async () => {
    setMenuOpen(false);
    const deleted = await confirmDeletePost(id, title);
    if (deleted) onDeleted?.(id);
  };

  const handleLike = async (event) => {
    event.preventDefault();
    event.stopPropagation();

    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    if (liking) return;

    setLiking(true);
    try {
      if (isLiked) {
        await unlikePost(id);
        setIsLiked(false);
        setLikesCount((count) => Math.max(0, count - 1));
      } else {
        const result = await likePost(id);
        setIsLiked(true);
        if (result?.message !== 'Лайк уже поставлен') {
          setLikesCount((count) => count + 1);
        }
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLiking(false);
    }
  };

  return (
    <article className="relative flex flex-col rounded-2xl border-2 border-craft-brown bg-craft-beige transition-shadow hover:shadow-md">
      {canManage && (
        <div className="absolute right-2 top-2 z-10" ref={menuRef}>
          <button
            type="button"
            onClick={() => setMenuOpen((open) => !open)}
            className="flex h-8 w-8 items-center justify-center rounded-full border border-craft-brown/20 bg-white/95 text-craft-brown shadow-sm hover:bg-craft-cream"
            aria-label="Действия с публикацией"
            aria-expanded={menuOpen}
            aria-haspopup="menu"
          >
            <IconMoreVertical />
          </button>
          {menuOpen && (
            <div
              role="menu"
              className="absolute right-0 top-full mt-1 min-w-[9.5rem] overflow-hidden rounded-xl border-2 border-craft-brown bg-white py-1 shadow-lg"
            >
              <Link
                to={`/posts/${id}/edit`}
                role="menuitem"
                className="block px-4 py-2 text-sm text-craft-brown hover:bg-craft-cream"
                onClick={() => setMenuOpen(false)}
              >
                Редактировать
              </Link>
              <button
                type="button"
                role="menuitem"
                className="block w-full px-4 py-2 text-left text-sm text-red-900 hover:bg-red-50"
                onClick={handleDelete}
              >
                Удалить
              </button>
            </div>
          )}
        </div>
      )}

      <Link to={`/posts/${id}`} className="block p-3">
        {imageUrl ? (
          <img
            src={imageUrl}
            alt=""
            className="max-h-48 w-full rounded-lg object-cover"
          />
        ) : (
          <div className="max-h-48 w-full rounded-lg bg-craft-thumb" aria-hidden="true" />
        )}

        <div className="mt-2 flex min-w-0 flex-col gap-1 pr-6">
          <h3 className="line-clamp-2 text-base font-semibold leading-snug text-craft-brown">
            {title}
          </h3>
          <p className="text-xs text-craft-brown/80">[{authorName}]</p>
          {description && (
            <p className="line-clamp-2 text-xs text-gray-600">{description}</p>
          )}
          <div className="mt-auto flex flex-wrap items-center gap-2">
            <span className="inline-flex w-fit rounded-full bg-craft-brown px-2.5 py-0.5 text-xs font-medium text-white">
              {categoryName}
            </span>
            {createdAt && (
              <time className="text-xs text-craft-brown/60" dateTime={post.created_at}>
                {createdAt}
              </time>
            )}
          </div>
        </div>
      </Link>

      <div className="flex items-center gap-4 border-t border-craft-brown/15 px-3 py-2 text-sm text-gray-500">
        <button
          type="button"
          onClick={handleLike}
          disabled={liking}
          aria-pressed={isLiked}
          aria-label={isLiked ? 'Убрать лайк' : 'Поставить лайк'}
          className={`inline-flex h-8 items-center gap-1.5 rounded-full bg-gray-100 px-3 transition-colors hover:bg-gray-200 disabled:opacity-50 ${
            isLiked ? 'text-red-600' : ''
          }`}
        >
          <IconHeart className={`h-4 w-4 ${isLiked ? 'fill-current' : ''}`} />
          {likesCount}
        </button>
        <span className="inline-flex h-8 items-center gap-1.5 rounded-full bg-gray-100 px-3">
          <IconComment className="h-4 w-4" />
          {commentsCount}
        </span>
      </div>
    </article>
  );
}
