import { Navigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import ProtectedRoute from './ProtectedRoute';

export default function StaffRoute({ children }) {
  const { isAdmin, isStaff, loading } = useAuth();

  return (
    <ProtectedRoute>
      {loading ? (
        <p className="py-12 text-center text-sm text-craft-brown/70">Загрузка…</p>
      ) : isAdmin || isStaff ? (
        children
      ) : (
        <Navigate to="/" replace />
      )}
    </ProtectedRoute>
  );
}
