import { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import api from '../../api/axios';
import { createCategory, deleteCategory, updateCategory } from '../../api/admin';

export default function AdminCategories() {
  const { isAdmin } = useAuth();
  const [categories, setCategories] = useState([]);
  const [newName, setNewName] = useState('');
  const [editingId, setEditingId] = useState(null);
  const [editName, setEditName] = useState('');
  const [loading, setLoading] = useState(true);

  const load = async () => {
    setLoading(true);
    try {
      const { data } = await api.get('/categories/');
      setCategories(data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!newName.trim()) return;
    try {
      await createCategory(newName.trim());
      setNewName('');
      await load();
    } catch (err) {
      alert(err.response?.data?.detail || 'Ошибка');
    }
  };

  const handleUpdate = async (id) => {
    try {
      await updateCategory(id, editName.trim());
      setEditingId(null);
      await load();
    } catch (err) {
      alert(err.response?.data?.detail || 'Ошибка');
    }
  };

  const handleDelete = async (id, name) => {
    if (!window.confirm(`Удалить категорию «${name}»?`)) return;
    try {
      await deleteCategory(id);
      await load();
    } catch (err) {
      alert(err.response?.data?.detail || 'Ошибка');
    }
  };

  if (!isAdmin) return <Navigate to="/admin/posts" replace />;

  if (loading) return <p className="text-sm text-craft-brown/70">Загрузка…</p>;

  return (
    <div className="space-y-6">
      <form onSubmit={handleCreate} className="flex flex-wrap gap-2">
        <input
          type="text"
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
          placeholder="Новая категория"
          className="min-w-[200px] flex-1 rounded-xl border-2 border-craft-brown/30 bg-white px-3 py-2"
        />
        <button
          type="submit"
          className="rounded-full bg-craft-brown px-4 py-2 text-sm font-medium text-white"
        >
          Добавить
        </button>
      </form>

      <ul className="space-y-2">
        {categories.map((cat) => (
          <li
            key={cat.id}
            className="flex flex-wrap items-center justify-between gap-2 rounded-xl border border-craft-brown/20 bg-white px-4 py-3"
          >
            {editingId === cat.id ? (
              <>
                <input
                  value={editName}
                  onChange={(e) => setEditName(e.target.value)}
                  className="flex-1 rounded-lg border px-2 py-1"
                />
                <button
                  type="button"
                  onClick={() => handleUpdate(cat.id)}
                  className="text-sm font-medium text-craft-brown underline"
                >
                  Сохранить
                </button>
                <button type="button" onClick={() => setEditingId(null)} className="text-sm">
                  Отмена
                </button>
              </>
            ) : (
              <>
                <span className="font-medium text-craft-brown">{cat.name}</span>
                <div className="flex gap-3">
                  <button
                    type="button"
                    onClick={() => {
                      setEditingId(cat.id);
                      setEditName(cat.name);
                    }}
                    className="text-sm underline"
                  >
                    Изменить
                  </button>
                  <button
                    type="button"
                    onClick={() => handleDelete(cat.id, cat.name)}
                    className="text-sm text-red-800 underline"
                  >
                    Удалить
                  </button>
                </div>
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
