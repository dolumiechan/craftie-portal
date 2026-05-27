import { useEffect, useState } from 'react';
import { resolveMediaUrl } from '../../utils/post';
import InterestPicker from './InterestPicker';
import { getApiErrorMessage } from '../../utils/apiError';

export default function ProfileForm({ profile, categories, onSubmit, submitting }) {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [bio, setBio] = useState('');
  const [interestIds, setInterestIds] = useState([]);
  const [avatarFile, setAvatarFile] = useState(null);
  const [avatarPreview, setAvatarPreview] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!profile) return;
    setUsername(profile.username || '');
    setEmail(profile.email || '');
    setBio(profile.bio || '');
    setInterestIds(profile.interests?.map((i) => i.id) || []);
    setAvatarPreview(resolveMediaUrl(profile.avatar_url));
    setAvatarFile(null);
  }, [profile]);

  const handleAvatarChange = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setAvatarFile(file);
    setAvatarPreview(URL.createObjectURL(file));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    const formData = new FormData();
    formData.append('username', username.trim());
    formData.append('email', email.trim());
    formData.append('bio', bio);
    formData.append('interest_ids', JSON.stringify(interestIds));
    if (avatarFile) {
      formData.append('avatar', avatarFile);
    }

    try {
      await onSubmit(formData);
    } catch (err) {
      setError(getApiErrorMessage(err, 'Не удалось сохранить профиль.'));
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mx-auto max-w-xl space-y-3">
      {error && (
        <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-900" role="alert">
          {error}
        </p>
      )}

      <div>
        <p className="text-sm font-medium text-craft-brown">Аватар</p>

        {avatarPreview ? (
          <div className="mt-2 space-y-2">
            <img
              src={avatarPreview}
              alt=""
              className="mx-auto h-28 w-28 rounded-full border border-craft-brown/20 object-cover"
            />
            <div className="flex flex-wrap justify-center gap-2">
              <label className="cursor-pointer rounded-full border border-craft-brown px-3 py-1.5 text-sm font-medium text-craft-brown hover:bg-craft-cream">
                Заменить
                <input
                  type="file"
                  accept="image/jpeg,image/png,image/jpg"
                  onChange={handleAvatarChange}
                  className="sr-only"
                />
              </label>
              <button
                type="button"
                onClick={() => {
                  setAvatarFile(null);
                  setAvatarPreview(null);
                }}
                className="rounded-full border border-red-300 px-3 py-1.5 text-sm font-medium text-red-800 hover:bg-red-50"
              >
                Удалить
              </button>
            </div>
          </div>
        ) : (
          <label className="mt-2 flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed border-gray-300 bg-gray-50 p-6 text-center transition-colors hover:border-gray-400">
            <span className="text-sm font-medium text-craft-brown">+ Загрузить изображение</span>
            <span className="mt-1 text-xs text-gray-500">PNG, JPG до 5MB</span>
            <input
              type="file"
              accept="image/jpeg,image/png,image/jpg"
              onChange={handleAvatarChange}
              className="sr-only"
            />
          </label>
        )}
      </div>

      <label className="block text-sm font-medium text-craft-brown">
        Имя пользователя
        <input
          type="text"
          required
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="mt-1 w-full rounded-xl border-2 border-craft-brown/30 bg-white px-3 py-1.5 text-sm outline-none focus:border-craft-brown"
        />
      </label>

      <label className="block text-sm font-medium text-craft-brown">
        Email
        <input
          type="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="mt-1 w-full rounded-xl border-2 border-craft-brown/30 bg-white px-3 py-1.5 text-sm outline-none focus:border-craft-brown"
        />
      </label>

      <label className="block text-sm font-medium text-craft-brown">
        О себе
        <textarea
          rows={4}
          value={bio}
          onChange={(e) => setBio(e.target.value)}
          placeholder="Расскажите о своём творчестве…"
          className="mt-1 w-full resize-y rounded-xl border-2 border-craft-brown/30 bg-white px-3 py-1.5 text-sm outline-none focus:border-craft-brown"
        />
      </label>

      <fieldset>
        <legend className="mb-2 text-sm font-medium text-craft-brown">Интересы</legend>
        <InterestPicker
          categories={categories}
          selectedIds={interestIds}
          onChange={setInterestIds}
        />
      </fieldset>

      <button
        type="submit"
        disabled={submitting}
        className="rounded-full bg-craft-brown px-6 py-2.5 text-sm font-semibold text-white hover:opacity-90 disabled:opacity-50"
      >
        {submitting ? 'Сохранение…' : 'Сохранить профиль'}
      </button>
    </form>
  );
}
