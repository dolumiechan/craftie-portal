import { Link } from 'react-router-dom';
import EmptyState from '../ui/EmptyState';

function SidebarBlock({ title, children }) {
  return (
    <section className="rounded-2xl border-2 border-craft-brown/20 bg-craft-beige p-4 sm:p-5">
      <h2 className="mb-3 text-base font-semibold text-craft-brown">{title}</h2>
      {children}
    </section>
  );
}

export default function RightSidebar({ categories = [], categoryId, setCategoryId }) {
  return (
    <aside
      className="w-full shrink-0 space-y-4 lg:sticky lg:top-8 lg:w-72 xl:w-80"
      aria-label="Боковая панель"
    >
      <SidebarBlock title="Категории">
        {categories.length === 0 ? (
          <p className="text-sm text-craft-brown/60">Категории загружаются…</p>
        ) : (
          <ul className="grid grid-cols-2 gap-x-3 gap-y-2 text-sm">
            <li>
              <button
                type="button"
                onClick={() => setCategoryId(null)}
                className={`text-left transition-colors hover:text-craft-brown-dark ${
                  categoryId === null ? 'font-semibold underline' : 'text-craft-brown/90'
                }`}
              >
                Все
              </button>
            </li>
            {categories.map((cat) => (
              <li key={cat.id}>
                <button
                  type="button"
                  onClick={() => setCategoryId(cat.id)}
                  className={`text-left transition-colors hover:text-craft-brown-dark ${
                    categoryId === cat.id ? 'font-semibold underline' : 'text-craft-brown/90'
                  }`}
                >
                  {cat.name}
                </button>
              </li>
            ))}
          </ul>
        )}
      </SidebarBlock>

      <SidebarBlock title="Офлайн-встречи">
        <EmptyState
          title="Скоро"
          description="Анонсы мастер-классов и встреч появятся в разделе «Мероприятия»."
          action={
            <Link
              to="/events"
              className="text-sm font-medium text-craft-brown underline hover:text-craft-brown-dark"
            >
              Подробнее
            </Link>
          }
        />
      </SidebarBlock>
    </aside>
  );
}
