import { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { fetchAdminLogs } from '../../api/admin';
import { formatPostDate } from '../../utils/post';

export default function AdminLogs() {
  const { isAdmin } = useAuth();
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAdminLogs()
      .then(setLogs)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (!isAdmin) return <Navigate to="/admin/posts" replace />;

  if (loading) return <p className="text-sm text-craft-brown/70">Загрузка…</p>;

  return (
    <div className="overflow-x-auto rounded-2xl border-2 border-craft-brown bg-craft-beige">
      <table className="w-full min-w-[720px] text-left text-sm">
        <thead>
          <tr className="border-b border-craft-brown/20 text-craft-brown/70">
            <th className="p-3">Время</th>
            <th className="p-3">Пользователь</th>
            <th className="p-3">Действие</th>
            <th className="p-3">Детали</th>
          </tr>
        </thead>
        <tbody>
          {logs.map((log) => (
            <tr key={log.id} className="border-b border-craft-brown/10">
              <td className="p-3 whitespace-nowrap">{formatPostDate(log.timestamp)}</td>
              <td className="p-3">{log.actor_username || `#${log.user_id}`}</td>
              <td className="p-3 font-medium">{log.action}</td>
              <td className="p-3 text-craft-brown/80">{log.details || '—'}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {!logs.length && (
        <p className="p-6 text-center text-sm text-craft-brown/60">Логов пока нет.</p>
      )}
    </div>
  );
}
