import { useEffect, useState } from 'react';
import { resolveMediaUrl } from '../../utils/post';
import { getApiErrorMessage } from '../../utils/apiError';

export default function PostForm({ initial, categories, onSubmit, submitting, submitLabel }) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [categoryId, setCategoryId] = useState('');
  const [tagsInput, setTagsInput] = useState('');
  const [imageFile, setImageFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!initial) return;
    setTitle(initial.title || '');
    setDescription(initial.description || '');
    setCategoryId(initial.category_id ? String(initial.category_id) : '');
    setTagsInput(initial.tags?.map((t) => t.name).join(', ') || '');
    setPreview(resolveMediaUrl(initial.image_url || initial.images?.[0]?.image_url));
    setImageFile(null);
  }, [initial]);

  const handleFile = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setImageFile(file);
    setPreview(URL.createObjectURL(file));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (!initial && !imageFile) {
      setError('Добавьте изображение работы.');
      return;
    }

    const tagNames = tagsInput
      .split(',')
      .map((t) => t.trim())
      .filter(Boolean);

    const formData = new FormData();
    formData.append('title', title.trim());
    formData.append('description', description);
    if (categoryId) formData.append('category_id', categoryId);
    formData.append('tags_json', JSON.stringify(tagNames));
    if (imageFile) formData.append('file', imageFile);

    try {
      await onSubmit(formData);
    } catch (err) {
      setError(getApiErrorMessage(err, 'Не удалось сохранить публикацию.'));
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mx-auto max-w-xl space-y-3">
      {error && (
        <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-900" role="alert">
          {error}
        </p>
      )}

      <label className="block text-sm font-medium text-craft-brown">
        Название *
        <input
          type="text"
          required
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="mt-1 w-full rounded-xl border-2 border-craft-brown/30 bg-white px-3 py-1.5 text-sm outline-none focus:border-craft-brown"
        />
      </label>

      <label className="block text-sm font-medium text-craft-brown">
        Описание
        <textarea
          rows={5}
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="mt-1 w-full resize-y rounded-xl border-2 border-craft-brown/30 bg-white px-3 py-1.5 text-sm outline-none focus:border-craft-brown"
        />
      </label>

      <label className="block text-sm font-medium text-craft-brown">
        Категория
        <select
          value={categoryId}
          onChange={(e) => setCategoryId(e.target.value)}
          className="mt-1 w-full rounded-xl border-2 border-craft-brown/30 bg-white px-3 py-1.5 text-sm outline-none focus:border-craft-brown"
        >
          <option value="">— не выбрана —</option>
          {categories?.map((cat) => (
            <option key={cat.id} value={cat.id}>
              {cat.name}
            </option>
          ))}
        </select>
      </label>

      <label className="block text-sm font-medium text-craft-brown">
        Теги (через запятую)
        <input
          type="text"
          value={tagsInput}
          onChange={(e) => setTagsInput(e.target.value)}
          placeholder="керамика, ручная работа"
          className="mt-1 w-full rounded-xl border-2 border-craft-brown/30 bg-white px-3 py-1.5 text-sm outline-none focus:border-craft-brown"
        />
      </label>

      <div>
        <p className="text-sm font-medium text-craft-brown">
          Изображение {!initial && '*'}
        </p>

        {preview ? (
          <div className="mt-2 space-y-2">
            <img
              src={preview}
              alt=""
              className="mx-auto max-h-48 w-full rounded-xl border border-craft-brown/20 object-cover"
            />
            <div className="flex flex-wrap justify-center gap-2">
              <label className="cursor-pointer rounded-full border border-craft-brown px-3 py-1.5 text-sm font-medium text-craft-brown hover:bg-craft-cream">
                Заменить
                <input
                  type="file"
                  accept="image/jpeg,image/png,image/webp,image/jpg"
                  onChange={handleFile}
                  className="sr-only"
                />
              </label>
              <button
                type="button"
                onClick={() => {
                  setImageFile(null);
                  setPreview(
                    initial
                      ? resolveMediaUrl(initial.image_url || initial.images?.[0]?.image_url)
                      : null,
                  );
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
              accept="image/jpeg,image/png,image/webp,image/jpg"
              onChange={handleFile}
              className="sr-only"
            />
          </label>
        )}
      </div>

      <button
        type="submit"
        disabled={submitting}
        className="rounded-full bg-craft-brown px-6 py-2.5 text-sm font-semibold text-white hover:opacity-90 disabled:opacity-50"
      >
        {submitting ? 'Сохранение…' : submitLabel}
      </button>
    </form>
  );
}
