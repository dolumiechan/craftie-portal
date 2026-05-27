import api from './axios';

export async function fetchAdminUsers() {
  const { data } = await api.get('/admin/users');
  return data;
}

export async function toggleUserStatus(userId) {
  const { data } = await api.patch(`/admin/users/${userId}/toggle-status`);
  return data;
}

export async function assignUserRole(userId, role) {
  const { data } = await api.patch(`/admin/users/${userId}/role`, { role });
  return data;
}

export async function exportUsersCsv() {
  const { data } = await api.get('/admin/users/export/csv', { responseType: 'blob' });
  return data;
}

export async function fetchAdminLogs() {
  const { data } = await api.get('/admin/logs');
  return data;
}

export async function fetchAdminPosts(params = {}) {
  const { data } = await api.get('/admin/posts', { params });
  return data;
}

export async function togglePostHidden(postId) {
  const { data } = await api.patch(`/admin/posts/${postId}/toggle-hidden`);
  return data;
}

export async function adminDeletePost(postId) {
  await api.delete(`/admin/posts/${postId}`);
}

export async function createCategory(name) {
  const { data } = await api.post('/categories/', { name });
  return data;
}

export async function updateCategory(id, name) {
  const { data } = await api.put(`/categories/${id}`, { name });
  return data;
}

export async function deleteCategory(id) {
  await api.delete(`/categories/${id}`);
}
