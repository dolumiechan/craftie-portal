import { useRef, useState } from 'react';
import { Link, NavLink } from 'react-router-dom';
import { MAIN_NAV, SITE_TITLE } from '../../constants/navigation';
import { useAuth } from '../../context/AuthContext';
import { useClickOutside } from '../../hooks/useClickOutside';
import { resolveMediaUrl } from '../../utils/post';
import { IconChevronDown, IconSearch } from '../ui/Icons';

function navLinkClass({ isActive }) {
  const base =
    'block rounded-lg px-3 py-2 text-sm font-medium transition-colors md:inline-block md:rounded-none md:border-b-2 md:px-0 md:py-0.5 md:pb-0.5';
  return isActive
    ? `${base} bg-craft-cream text-craft-brown md:border-craft-brown md:bg-transparent`
    : `${base} text-craft-brown hover:bg-craft-cream/80 md:border-transparent md:hover:border-craft-brown/40 md:hover:bg-transparent`;
}

function NavItems({ isAuthenticated, isAdmin, isStaff, onNavigate }) {
  const extra = onNavigate ? { onClick: onNavigate } : {};

  return (
    <>
      {MAIN_NAV.map((item) => (
        <NavLink key={item.label} to={item.to} end={item.end} className={navLinkClass} {...extra}>
          {item.label}
        </NavLink>
      ))}
      {isAuthenticated && (
        <NavLink to="/posts/new" className={navLinkClass} {...extra}>
          Опубликовать
        </NavLink>
      )}
      {(isAdmin || isStaff) && (
        <NavLink to="/admin" className={navLinkClass} {...extra}>
          Админ
        </NavLink>
      )}
    </>
  );
}

export default function Header({ search = '', onSearchChange }) {
  const { user, isAuthenticated, isAdmin, isStaff, logout, loading } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);
  const [mobileNavOpen, setMobileNavOpen] = useState(false);

  const userMenuRef = useRef(null);
  const mobileNavRef = useRef(null);

  useClickOutside(userMenuRef, () => setMenuOpen(false), menuOpen);
  useClickOutside(mobileNavRef, () => setMobileNavOpen(false), mobileNavOpen);

  const displayName = user?.username ?? 'Гость';
  const avatarUrl = resolveMediaUrl(user?.avatar_url);
  const closeMobile = () => setMobileNavOpen(false);

  return (
    <header className="border-b-2 border-craft-brown bg-craft-pink">
      <div className="mx-auto max-w-7xl px-4 py-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between gap-3">
          <button
            type="button"
            className="rounded-lg border-2 border-craft-brown/30 px-3 py-1.5 text-sm font-medium text-craft-brown md:hidden"
            aria-expanded={mobileNavOpen}
            aria-controls="mobile-nav"
            onClick={() => setMobileNavOpen((o) => !o)}
          >
            Меню
          </button>

          <Link
            to="/"
            className="flex-1 text-center text-lg font-semibold tracking-tight text-craft-brown sm:text-xl md:flex-none"
          >
            {SITE_TITLE}
          </Link>

          <div className="hidden w-56 md:block">
            <label className="sr-only" htmlFor="header-search-desktop">
              Поиск публикаций
            </label>
            <input
              id="header-search-desktop"
              type="search"
              placeholder="Поиск…"
              value={search}
              onChange={(e) => onSearchChange?.(e.target.value)}
              className="w-full rounded-xl border-2 border-craft-brown/30 bg-white px-3 py-2 text-sm outline-none focus:border-craft-brown"
            />
          </div>
        </div>

        <div className="mt-3 md:hidden">
          <label className="sr-only" htmlFor="header-search-mobile">
            Поиск публикаций
          </label>
          <div className="relative">
            <IconSearch className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-craft-brown/50" />
            <input
              id="header-search-mobile"
              type="search"
              placeholder="Поиск по работам…"
              value={search}
              onChange={(e) => onSearchChange?.(e.target.value)}
              className="w-full rounded-xl border-2 border-craft-brown/30 bg-white py-2 pl-10 pr-3 text-sm outline-none focus:border-craft-brown"
            />
          </div>
        </div>

        <div className="mt-4 hidden items-center justify-between gap-4 md:flex">
          <div className="relative" ref={userMenuRef}>
            {loading ? (
              <span className="text-sm text-craft-brown/60">…</span>
            ) : isAuthenticated ? (
              <>
                <button
                  type="button"
                  onClick={() => setMenuOpen((o) => !o)}
                  className="flex items-center gap-2 rounded-full outline-offset-2 hover:opacity-90 focus-visible:outline-2 focus-visible:outline-craft-brown"
                  aria-expanded={menuOpen}
                >
                  <span className="flex h-10 w-10 shrink-0 items-center justify-center overflow-hidden rounded-full bg-craft-thumb text-sm font-semibold text-white">
                    {avatarUrl ? (
                      <img src={avatarUrl} alt="" className="h-full w-full object-cover" />
                    ) : (
                      displayName.charAt(0).toUpperCase()
                    )}
                  </span>
                  <span className="flex items-center gap-1 text-sm font-medium">
                    Привет, {displayName}
                    <IconChevronDown />
                  </span>
                </button>
                {menuOpen && (
                  <div className="absolute left-0 top-full z-20 mt-2 min-w-[10rem] rounded-xl border-2 border-craft-brown bg-white py-1 shadow-lg">
                    <Link
                      to="/profile"
                      className="block px-4 py-2 text-sm hover:bg-craft-cream"
                      onClick={() => setMenuOpen(false)}
                    >
                      Мой профиль
                    </Link>
                    <button
                      type="button"
                      className="block w-full px-4 py-2 text-left text-sm hover:bg-craft-cream"
                      onClick={() => {
                        setMenuOpen(false);
                        logout();
                      }}
                    >
                      Выйти
                    </button>
                  </div>
                )}
              </>
            ) : (
              <Link to="/login" className="text-sm font-medium underline">
                Войти
              </Link>
            )}
          </div>

          <nav className="flex flex-wrap items-center justify-end gap-x-5 gap-y-2" aria-label="Основная навигация">
            <NavItems isAuthenticated={isAuthenticated} isAdmin={isAdmin} isStaff={isStaff} />
          </nav>
        </div>

        {mobileNavOpen && (
          <div
            id="mobile-nav"
            ref={mobileNavRef}
            className="mt-4 space-y-4 rounded-2xl border-2 border-craft-brown/20 bg-white p-4 md:hidden"
          >
            <div ref={userMenuRef}>
              {isAuthenticated ? (
                <div className="flex items-center gap-3 border-b border-craft-brown/10 pb-4">
                  <span className="flex h-10 w-10 items-center justify-center overflow-hidden rounded-full bg-craft-thumb text-white">
                    {avatarUrl ? (
                      <img src={avatarUrl} alt="" className="h-full w-full object-cover" />
                    ) : (
                      displayName.charAt(0).toUpperCase()
                    )}
                  </span>
                  <div className="text-sm">
                    <p className="font-medium">{displayName}</p>
                    <Link to="/profile" className="underline" onClick={closeMobile}>
                      Профиль
                    </Link>
                    {' · '}
                    <button type="button" className="underline" onClick={logout}>
                      Выйти
                    </button>
                  </div>
                </div>
              ) : (
                <Link to="/login" className="block text-sm font-medium underline" onClick={closeMobile}>
                  Войти
                </Link>
              )}
            </div>
            <nav className="flex flex-col gap-1" aria-label="Мобильная навигация">
              <NavItems
                isAuthenticated={isAuthenticated}
                isAdmin={isAdmin}
                isStaff={isStaff}
                onNavigate={closeMobile}
              />
            </nav>
          </div>
        )}
      </div>
    </header>
  );
}
