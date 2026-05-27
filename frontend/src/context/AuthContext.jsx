import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import {
  clearStoredToken,
  fetchMe,
  getStoredToken,
  loginRequest,
  registerRequest,
  setStoredToken,
} from '../api/auth';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadUser = useCallback(async () => {
    const token = getStoredToken();
    if (!token) {
      setUser(null);
      return null;
    }
    const me = await fetchMe();
    setUser(me);
    return me;
  }, []);

  useEffect(() => {
    let cancelled = false;

    const init = async () => {
      try {
        if (getStoredToken()) {
          await loadUser();
        }
      } catch {
        clearStoredToken();
        if (!cancelled) setUser(null);
      } finally {
        if (!cancelled) setLoading(false);
      }
    };

    init();

    const onLogout = () => {
      setUser(null);
    };
    window.addEventListener('auth:logout', onLogout);

    return () => {
      cancelled = true;
      window.removeEventListener('auth:logout', onLogout);
    };
  }, [loadUser]);

  const login = useCallback(async (username, password) => {
    const { access_token } = await loginRequest(username, password);
    setStoredToken(access_token);
    return loadUser();
  }, [loadUser]);

  const register = useCallback(async (payload) => {
    await registerRequest(payload);
    return login(payload.email, payload.password);
  }, [login]);

  const logout = useCallback(() => {
    clearStoredToken();
    setUser(null);
  }, []);

  const value = useMemo(() => {
    const roleName = user?.role_name ?? null;
    return {
      user,
      loading,
      isAuthenticated: Boolean(user),
      roleName,
      isAdmin: roleName === 'admin',
      isModerator: roleName === 'moderator',
      isStaff: roleName === 'admin' || roleName === 'moderator',
      login,
      register,
      logout,
      refreshUser: loadUser,
    };
  }, [user, loading, login, register, logout, loadUser]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return ctx;
}
