import api from './axios';

export async function fetchProfile() {
  const { data } = await api.get('/profile/');
  return data;
}

export async function updateProfile(formData) {
  const { data } = await api.put('/profile/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return data;
}