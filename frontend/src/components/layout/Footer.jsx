import { Link } from 'react-router-dom';
import { FOOTER_NAV } from '../../constants/navigation';

export default function Footer() {
  return (
    <footer className="mt-auto">
      <div className="h-5 bg-craft-pink-bar" aria-hidden="true" />
      <div className="bg-craft-brown-dark">
        <nav
          className="mx-auto flex max-w-7xl flex-wrap items-center justify-end gap-x-6 gap-y-2 px-4 py-5 sm:px-6 lg:px-8"
          aria-label="Нижняя навигация"
        >
          {FOOTER_NAV.map((item) => (
            <Link
              key={item.label}
              to={item.to}
              className="text-sm font-medium text-craft-cream/95 transition-colors hover:text-white"
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </div>
    </footer>
  );
}
