import { useCallback, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { fetchProfile, updateProfile } from '../api/profile';
import api from '../api/axios';
import ProfileForm from '../components/profile/ProfileForm';
import CommentHistory from '../components/profile/CommentHistory';
import MyPostsList from '../components/profile/MyPostsList';
import Alert from '../components/ui/Alert';

const ROLE_LABELS = {
  user: 'Пользователь',
  moderator: 'Модератор',
  admin: 'Администратор',
};

const TABS = [
  { id: 'edit', label: 'Редактирование' },
  { id: 'posts', label: 'Мои публикации' },
  { id: 'comments', label: 'Мои комментарии' },
];

export default function Profile() {
  const { user: authUser, isAdmin, logout, refreshUser } = useAuth();
  const [tab, setTab] = useState('edit');
  const [profile, setProfile] = useState(null);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [saved, setSaved] = useState(false);

  const loadProfile = useCallback(async () => {
    const data = await fetchProfile();
    setProfile(data);
    return data;
  }, []);

  useEffect(() => {
    const init = async () => {
      setLoading(true);
      try {
        const [profileData, cats] = await Promise.all([
          fetchProfile(),
          api.get('/categories/').then((r) => r.data),
        ]);
        setProfile(profileData);
        setCategories(cats);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    init();
  }, []);

  const handleSave = async (formData) => {
    setSubmitting(true);
    setSaved(false);
    try {
      const updated = await updateProfile(formData);
      setProfile(updated);
      await refreshUser();
      setSaved(true);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <p className="py-12 text-center text-sm text-craft-brown/70" role="status">
        Загрузка профиля…
      </p>
    );
  }

  return (
    <div className="mx-auto w-full max-w-xl">
      <header className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h1 className="text-xl font-bold text-craft-brown">Личный кабинет</h1>
          <p className="mt-1 text-sm text-craft-brown/70">
            {ROLE_LABELS[profile?.role_name || authUser?.role_name] || 'Пользователь'}
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          {isAdmin && (
            <Link
              to="/admin"
              className="rounded-full border-2 border-craft-brown px-4 py-2 text-sm font-medium text-craft-brown hover:bg-craft-cream"
            >
              Админ-панель
            </Link>
          )}
          <button
            type="button"
            onClick={logout}
            className="rounded-full bg-craft-brown px-4 py-2 text-sm font-medium text-white hover:opacity-90"
          >
            Выйти
          </button>
        </div>
      </header>

      <nav className="mt-4 flex flex-wrap gap-2 border-b-2 border-craft-brown/15 pb-2">
        {TABS.map((t) => (
          <button
            key={t.id}
            type="button"
            onClick={() => setTab(t.id)}
            className={`rounded-full px-4 py-1.5 text-sm font-medium transition-colors ${
              tab === t.id
                ? 'bg-craft-brown text-white'
                : 'text-craft-brown hover:bg-craft-cream'
            }`}
          >
            {t.label}
          </button>
        ))}
      </nav>

      <div className="mt-4 rounded-2xl border-2 border-craft-brown bg-craft-beige p-3">
        {tab === 'edit' && (
          <>
            {saved && (
              <div className="mb-4">
                <Alert variant="success">Профиль сохранён.</Alert>
              </div>
            )}
            <ProfileForm
              profile={profile}
              categories={categories}
              onSubmit={handleSave}
              submitting={submitting}
            />
          </>
        )}
        {tab === 'posts' && <MyPostsList posts={profile?.posts} />}
        {tab === 'comments' && <CommentHistory />}
      </div>
    </div>
  );
}
