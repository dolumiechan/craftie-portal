import api from './axios';

export async function fetchComments(postId) {
  const { data } = await api.get(`/posts/${postId}/comments/`);
  return data;
}

export async function createComment(postId, text) {
  const { data } = await api.post(`/posts/${postId}/comments/`, { text });
  return data;
}

export async function deleteComment(commentId) {
  await api.delete(`/posts/comments/${commentId}`);
}
