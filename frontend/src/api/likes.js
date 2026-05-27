import api from './axios';

export async function likePost(postId) {
  const { data } = await api.post(`/likes/${postId}`);
  return data;
}

export async function unlikePost(postId) {
  await api.delete(`/likes/${postId}`);
}