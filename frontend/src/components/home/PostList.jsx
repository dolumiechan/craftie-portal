import PostCard from './PostCard';
import Spinner from '../ui/Spinner';
import EmptyState from '../ui/EmptyState';
import { Link } from 'react-router-dom';

const PAGE_SIZE = 6;

export default function PostList({ posts, loading, page, total, setPage, hasMore, onPostDeleted }) {
  if (loading) {
    return (
      <div className="flex min-h-0 flex-1 items-center justify-center">
        <Spinner label="Загрузка публикаций…" />
      </div>
    );
  }

  if (!posts?.length) {
    return (
      <div className="flex min-h-0 flex-1 items-center justify-center">
        <EmptyState
        title="Публикации не найдены"
        description="Попробуйте другую категорию или измените поисковый запрос."
        action={
          <Link
            to="/posts/new"
            className="inline-block rounded-full bg-craft-brown px-4 py-2 text-sm font-medium text-white"
          >
            Опубликовать работу
          </Link>
        }
      />
      </div>
    );
  }

  return (
    <div className="flex min-h-0 flex-1 flex-col overflow-hidden">
      <p className="shrink-0 text-sm text-craft-brown/70">
        Найдено: {total}{' '}
        {total === 1 ? 'публикация' : total < 5 ? 'публикации' : 'публикаций'}
      </p>

      <div className="min-h-0 flex-1 overflow-y-auto">
        <div className="grid grid-cols-1 gap-4 py-4 sm:grid-cols-2 xl:grid-cols-3">
          {posts.map((post) => (
            <PostCard key={post.id} post={post} onDeleted={onPostDeleted} />
          ))}
        </div>
      </div>

      <nav
        className="flex shrink-0 flex-wrap items-center justify-center gap-4 pt-2"
        aria-label="Пагинация ленты"
      >
        <button
          type="button"
          className="rounded-full border-2 border-craft-brown bg-white px-4 py-2 text-sm font-medium text-craft-brown transition-colors hover:bg-craft-cream disabled:cursor-not-allowed disabled:opacity-40"
          onClick={() => setPage((p) => Math.max(p - 1, 1))}
          disabled={page === 1}
        >
          Назад
        </button>
        <span className="text-sm text-craft-brown/80">
          Страница {page}
          {total > 0 && ` из ${Math.ceil(total / PAGE_SIZE) || 1}`}
        </span>
        <button
          type="button"
          className="rounded-full border-2 border-craft-brown bg-white px-4 py-2 text-sm font-medium text-craft-brown transition-colors hover:bg-craft-cream disabled:cursor-not-allowed disabled:opacity-40"
          onClick={() => setPage((p) => p + 1)}
          disabled={!hasMore}
        >
          Далее
        </button>
      </nav>
    </div>
  );
}
