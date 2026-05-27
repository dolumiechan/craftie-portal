import api from './axios';
import { clearStoredToken, getStoredToken, setStoredToken } from './tokenStorage';

export { getStoredToken, setStoredToken, clearStoredToken };

export async function loginRequest(username, password) {
  const body = new URLSearchParams();
  body.append('username', username);
  body.append('password', password);

  const { data } = await api.post('/auth/login', body, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });
  return data;
}

export async function registerRequest({ email, username, password }) {
  const { data } = await api.post('/auth/register', { email, username, password });
  return data;
}

export async function fetchMe() {
  const { data } = await api.get('/auth/me');
  return data;
}
