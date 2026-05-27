import { Link } from 'react-router-dom';
import { formatPostDate } from '../../utils/post';

export default function MyPostsList({ posts }) {
  return (
    <div className="space-y-4">
      <Link
        to="/posts/new"
        className="inline-block rounded-full bg-craft-brown px-4 py-2 text-sm font-semibold text-white hover:opacity-90"
      >
        + Новая публикация
      </Link>

      {!posts?.length ? (
        <p className="text-sm text-craft-brown/70">
          У вас пока нет работ.{' '}
        </p>
      ) : (
        <>
          <ul className="space-y-2">
            {posts.map((post) => (
              <li key={post.id}>
                <Link
                  to={`/posts/${post.id}`}
                  className="flex items-center justify-between rounded-xl border-2 border-craft-brown/15 bg-white px-4 py-3 text-sm hover:bg-craft-cream"
                >
                  <span className="font-medium text-craft-brown">{post.title}</span>
                  <time className="text-xs text-craft-brown/55">
                    {formatPostDate(post.created_at)}
                  </time>
                </Link>
              </li>
            ))}
          </ul>
          <Link to="/my-posts" className="text-sm font-medium text-craft-brown underline">
            Все публикации и управление →
          </Link>
        </>
      )}
    </div>
  );
}
