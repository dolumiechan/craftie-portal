import { NavLink, Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

function tabClass({ isActive }) {
  return `rounded-full px-4 py-1.5 text-sm font-medium transition-colors ${
    isActive ? 'bg-craft-brown text-white' : 'text-craft-brown hover:bg-craft-cream'
  }`;
}

export default function AdminLayout() {
  const { isAdmin, isStaff, loading } = useAuth();

  if (loading) {
    return <p className="py-12 text-center text-sm text-craft-brown/70">Загрузка…</p>;
  }

  if (!isAdmin && !isStaff) {
    return <Navigate to="/" replace />;
  }

  return (
    <div className="flex h-full w-full flex-col overflow-hidden">
      <header className="shrink-0">
        <h1 className="text-2xl font-bold text-craft-brown">Администрирование</h1>
        <p className="mt-1 text-sm text-craft-brown/70">
          {isAdmin ? 'Полный доступ' : 'Модерация публикаций'}
        </p>
      </header>

      <nav className="mt-6 shrink-0 flex flex-wrap gap-2 border-b border-craft-brown/15 pb-3">
        {isAdmin && (
          <>
            <NavLink to="/admin/users" className={tabClass}>
              Пользователи
            </NavLink>
            <NavLink to="/admin/categories" className={tabClass}>
              Категории
            </NavLink>
          </>
        )}
        <NavLink to="/admin/posts" className={tabClass}>
          Публикации
        </NavLink>
        {isAdmin && (
          <NavLink to="/admin/logs" className={tabClass}>
            Лог действий
          </NavLink>
        )}
      </nav>

      <div className="min-h-0 flex-1 overflow-hidden pt-6">
        <Outlet />
      </div>
    </div>
  );
}
