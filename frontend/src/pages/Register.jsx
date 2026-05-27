import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AuthFormLayout, { AuthLink } from '../components/auth/AuthFormLayout';
import { useAuth } from '../context/AuthContext';
import { getApiErrorMessage } from '../utils/apiError';

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (password.length < 6) {
      setError('Пароль должен быть не короче 6 символов.');
      return;
    }
    if (password !== confirm) {
      setError('Пароли не совпадают.');
      return;
    }

    setSubmitting(true);
    try {
      await register({ email: email.trim(), username: username.trim(), password });
      navigate('/', { replace: true });
    } catch (err) {
      setError(getApiErrorMessage(err, 'Не удалось зарегистрироваться.'));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <AuthFormLayout
      title="Регистрация"
      subtitle="Создайте аккаунт автора"
      footer={
        <>
          Уже есть аккаунт? <AuthLink to="/login">Войти</AuthLink>
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
          Email
          <input
            type="email"
            required
            autoComplete="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mt-1 w-full rounded-xl border-2 border-craft-brown/30 bg-white px-3 py-2 text-craft-brown outline-none focus:border-craft-brown"
          />
        </label>

        <label className="block text-sm font-medium text-craft-brown">
          Имя пользователя
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
            minLength={6}
            autoComplete="new-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mt-1 w-full rounded-xl border-2 border-craft-brown/30 bg-white px-3 py-2 text-craft-brown outline-none focus:border-craft-brown"
          />
        </label>

        <label className="block text-sm font-medium text-craft-brown">
          Повторите пароль
          <input
            type="password"
            required
            autoComplete="new-password"
            value={confirm}
            onChange={(e) => setConfirm(e.target.value)}
            className="mt-1 w-full rounded-xl border-2 border-craft-brown/30 bg-white px-3 py-2 text-craft-brown outline-none focus:border-craft-brown"
          />
        </label>

        <button
          type="submit"
          disabled={submitting}
          className="w-full rounded-full bg-craft-brown py-2.5 text-sm font-semibold text-white transition-opacity hover:opacity-90 disabled:opacity-50"
        >
          {submitting ? 'Регистрация…' : 'Создать аккаунт'}
        </button>
      </form>
    </AuthFormLayout>
  );
}
