import { useEffect, useRef, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { likePost, unlikePost } from '../api/likes';
import { confirmDeletePost, fetchPostById } from '../api/posts';
import { getPostDisplay, resolveMediaUrl } from '../utils/post';
import { useAuth } from '../context/AuthContext';
import { useClickOutside } from '../hooks/useClickOutside';
import { IconComment, IconHeart, IconMoreVertical } from '../components/ui/Icons';
import CommentSection from '../components/comments/CommentSection';
import Spinner from '../components/ui/Spinner';
import Alert from '../components/ui/Alert';
import { getApiErrorMessage } from '../utils/apiError';

export default function PostDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user, isAuthenticated, isStaff } = useAuth();
  const [post, setPost] = useState(null);
  const [commentsCount, setCommentsCount] = useState(0);
  const [likesCount, setLikesCount] = useState(0);
  const [isLiked, setIsLiked] = useState(false);
  const [liking, setLiking] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const menuRef = useRef(null);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await fetchPostById(id);
        setPost(data);
        setCommentsCount(data.comments_count ?? 0);
        setLikesCount(data.likes_count ?? 0);
        setIsLiked(Boolean(data.is_liked));
      } catch (err) {
        console.error('Failed to load post:', err);
        setError(getApiErrorMessage(err, 'Публикация не найдена или сервер недоступен.'));
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [id]);

  const handleLike = async () => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    if (liking || !post) return;

    setLiking(true);
    try {
      if (isLiked) {
        await unlikePost(post.id);
        setIsLiked(false);
        setLikesCount((count) => Math.max(0, count - 1));
      } else {
        const result = await likePost(post.id);
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

  const canManage = Boolean(post && user && (user.id === post.author_id || isStaff));

  useClickOutside(menuRef, () => setMenuOpen(false), menuOpen && canManage);

  const handleDelete = async () => {
    if (!post) return;
    setMenuOpen(false);
    const deleted = await confirmDeletePost(post.id, post.title);
    if (deleted) navigate('/');
  };

  if (loading) {
    return <Spinner label="Загрузка публикации…" />;
  }

  if (error || !post) {
    return (
      <div className="mx-auto max-w-lg space-y-4">
        <Alert>{error || 'Публикация не найдена.'}</Alert>
        <Link to="/" className="block text-center text-sm font-medium text-craft-brown underline">
          Вернуться в ленту
        </Link>
      </div>
    );
  }

  const {
    title,
    fullDescription,
    authorName,
    categoryName,
    imageUrl,
    createdAt,
  } = getPostDisplay(post);

  return (
    <article className="mx-auto max-w-3xl">
      <div className="mb-6">
        <Link to="/" className="text-sm text-craft-brown/80 hover:text-craft-brown">
          ← Лента
        </Link>
      </div>

      <div className="relative overflow-hidden rounded-2xl border-2 border-craft-brown bg-craft-beige">
        {canManage && (
          <div className="absolute right-3 top-3 z-20" ref={menuRef}>
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
                  to={`/posts/${post.id}/edit`}
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
        {imageUrl && (
          <img src={imageUrl} alt={title} className="max-h-96 w-full object-cover" />
        )}

        <div className="space-y-4 p-6 sm:p-8">
          <header className={`space-y-2 ${canManage ? 'pr-10' : ''}`}>
            <h1 className="text-2xl font-bold text-craft-brown sm:text-3xl">{title}</h1>
            <p className="text-craft-brown/80">
              [{authorName}]
              {createdAt && (
                <>
                  {' '}
                  · <time dateTime={post.created_at}>{createdAt}</time>
                </>
              )}
            </p>
            <div className="flex flex-wrap items-center gap-2">
              <span className="inline-flex rounded-full bg-craft-brown px-3 py-1 text-sm font-medium text-white">
                {categoryName}
              </span>
              {post.tags?.map((tag) => (
                <span
                  key={tag.id}
                  className="rounded-full border border-craft-brown/30 px-2 py-0.5 text-xs text-craft-brown/80"
                >
                  #{tag.name}
                </span>
              ))}
            </div>
          </header>

          {fullDescription && (
            <p className="whitespace-pre-wrap text-base leading-relaxed text-craft-brown/90">
              {fullDescription}
            </p>
          )}

          {post.images?.length > 1 && (
            <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
              {post.images.slice(1).map((img) => (
                <img
                  key={img.id}
                  src={resolveMediaUrl(img.image_url)}
                  alt=""
                  className="h-32 w-full rounded-xl object-cover"
                />
              ))}
            </div>
          )}

          <footer className="relative z-10 flex items-center gap-4 border-t border-craft-brown/15 pt-4 text-sm text-gray-500">
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
              {commentsCount} комментариев
            </span>
          </footer>
          <CommentSection postId={post.id} onCountChange={setCommentsCount} />
        </div>
      </div>
    </article>
  );
}
