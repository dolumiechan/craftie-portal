import { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import {
  assignUserRole,
  exportUsersCsv,
  fetchAdminUsers,
  toggleUserStatus,
} from '../../api/admin';
import { formatPostDate } from '../../utils/post';
import { getApiErrorMessage } from '../../utils/apiError';

const ROLES = ['user', 'moderator', 'admin'];

export default function AdminUsers() {
  const { isAdmin } = useAuth();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  const load = async () => {
    setLoading(true);
    try {
      setUsers(await fetchAdminUsers());
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const handleToggle = async (id) => {
    try {
      await toggleUserStatus(id);
      await load();
    } catch (err) {
      alert(getApiErrorMessage(err));
    }
  };

  const handleRole = async (id, role) => {
    try {
      await assignUserRole(id, role);
      await load();
    } catch (err) {
      alert(getApiErrorMessage(err));
    }
  };

  const handleExport = async () => {
    try {
      const blob = await exportUsersCsv();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'users_export.csv';
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      alert('Не удалось выгрузить CSV');
    }
  };

  if (!isAdmin) return <Navigate to="/admin/posts" replace />;

  if (loading) return <p className="text-sm text-craft-brown/70">Загрузка…</p>;

  return (
    <div className="flex h-full w-full flex-col overflow-hidden">
      <button
        type="button"
        onClick={handleExport}
        className="shrink-0 rounded-full border-2 border-craft-brown px-4 py-2 text-sm font-medium text-craft-brown hover:bg-craft-cream"
      >
        Экспорт CSV
      </button>

      <div className="min-h-0 flex-1 overflow-y-auto pt-4">
        <div className="overflow-x-auto rounded-2xl border-2 border-craft-brown bg-craft-beige">
          <table className="w-full min-w-[640px] text-left text-sm">
          <thead>
            <tr className="border-b border-craft-brown/20 text-craft-brown/70">
              <th className="p-3">ID</th>
              <th className="p-3">Пользователь</th>
              <th className="p-3">Роль</th>
              <th className="p-3">Статус</th>
              <th className="p-3">Действия</th>
            </tr>
          </thead>
          <tbody>
            {users.map((u) => (
              <tr key={u.id} className="border-b border-craft-brown/10">
                <td className="p-3">{u.id}</td>
                <td className="p-3">
                  <div className="font-medium">{u.username}</div>
                  <div className="text-xs text-craft-brown/60">{u.email}</div>
                  <div className="text-xs text-craft-brown/50">
                    {formatPostDate(u.created_at)}
                  </div>
                </td>
                <td className="p-3">
                  <select
                    value={u.role_name || 'user'}
                    onChange={(e) => handleRole(u.id, e.target.value)}
                    className="rounded-lg border border-craft-brown/30 bg-white px-2 py-1"
                  >
                    {ROLES.map((r) => (
                      <option key={r} value={r}>
                        {r}
                      </option>
                    ))}
                  </select>
                </td>
                <td className="p-3">
                  {u.is_active ? (
                    <span className="text-green-800">Активен</span>
                  ) : (
                    <span className="text-red-800">Заблокирован</span>
                  )}
                </td>
                <td className="p-3">
                  <button
                    type="button"
                    onClick={() => handleToggle(u.id)}
                    className="text-sm font-medium text-craft-brown underline"
                  >
                    {u.is_active ? 'Заблокировать' : 'Разблокировать'}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        </div>
      </div>
    </div>
  );
}
