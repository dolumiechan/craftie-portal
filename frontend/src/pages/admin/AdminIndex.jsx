import { Navigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export default function AdminIndex() {
  const { isAdmin } = useAuth();
  return <Navigate to={isAdmin ? '/admin/users' : '/admin/posts'} replace />;
}
