import api from './axios';

export async function fetchPosts({ skip, limit, categoryId, search }) {
  const { data } = await api.get('/posts/', {
    params: {
      skip,
      limit,
      category_id: categoryId ?? undefined,
      search: search?.trim() || undefined,
    },
  });
  return data;
}

export async function fetchMyPosts({ skip = 0, limit = 50 } = {}) {
  const { data } = await api.get('/posts/my', { params: { skip, limit } });
  return data;
}

export async function fetchPostById(id) {
  const { data } = await api.get(`/posts/${id}`);
  return data;
}

export async function createPost(formData) {
  const { data } = await api.post('/posts/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return data;
}

export async function updatePost(id, formData) {
  const { data } = await api.put(`/posts/${id}`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return data;
}

export async function deletePost(id) {
  await api.delete(`/posts/${id}`);
}

export async function confirmDeletePost(id, title) {
  if (!window.confirm(`Удалить «${title}»?`)) return false;
  try {
    await deletePost(id);
    return true;
  } catch (err) {
    console.error(err);
    alert('Не удалось удалить публикацию.');
    return false;
  }
}
