import { Link } from 'react-router-dom';

export default function AuthFormLayout({ title, subtitle, children, footer }) {
  return (
    <div className="mx-auto max-w-md">
      <div className="rounded-2xl border-2 border-craft-brown bg-craft-beige p-6 sm:p-8">
        <header className="mb-6 text-center">
          <h1 className="text-xl font-bold text-craft-brown">{title}</h1>
          {subtitle && <p className="mt-2 text-sm text-craft-brown/75">{subtitle}</p>}
        </header>
        {children}
      </div>
      {footer && <p className="mt-4 text-center text-sm text-craft-brown/80">{footer}</p>}
    </div>
  );
}

export function AuthLink({ to, children }) {
  return (
    <Link to={to} className="font-medium text-craft-brown underline hover:text-craft-brown-dark">
      {children}
    </Link>
  );
}
