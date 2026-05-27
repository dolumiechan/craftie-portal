import { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import AuthFormLayout, { AuthLink } from '../components/auth/AuthFormLayout';
import { useAuth } from '../context/AuthContext';
import { getApiErrorMessage } from '../utils/apiError';

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from || '/';

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      await login(username.trim(), password);
      navigate(from, { replace: true });
    } catch (err) {
      setError(getApiErrorMessage(err, 'Не удалось войти. Проверьте данные.'));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <AuthFormLayout
      title="Вход"
      subtitle="Email или имя пользователя и пароль"
      footer={
        <>
          Нет аккаунта? <AuthLink to="/register">Зарегистрироваться</AuthLink>
        </>
      }
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        {error && (
          <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-900" role="alert">
            {error}
          </p>
        )}

        <label className="block text-sm font-medium text-craft-brown">
          Email или имя пользователя
          <input
            type="text"
            required
            autoComplete="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="mt-1 w-full rounded-xl border-2 border-craft-brown/30 bg-white px-3 py-2 text-craft-brown outline-none focus:border-craft-brown"
          />
        </label>

        <label className="block text-sm font-medium text-craft-brown">
          Пароль
          <input
            type="password"
            required
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mt-1 w-full rounded-xl border-2 border-craft-brown/30 bg-white px-3 py-2 text-craft-brown outline-none focus:border-craft-brown"
          />
        </label>

        <button
          type="submit"
          disabled={submitting}
          className="w-full rounded-full bg-craft-brown py-2.5 text-sm font-semibold text-white transition-opacity hover:opacity-90 disabled:opacity-50"
        >
          {submitting ? 'Вход…' : 'Войти'}
        </button>
      </form>
    </AuthFormLayout>
  );
}
