export function resolveMediaUrl(url) {
  if (!url) return null;
  if (url.startsWith('http://') || url.startsWith('https://')) return url;
  return url.startsWith('/') ? url : `/${url}`;
}

export function formatPostDate(isoString) {
  if (!isoString) return '';
  return new Date(isoString).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  });
}

export function getPostDisplay(post) {
  const description = post.description?.trim();
  const shortDescription =
    description && description.length > 120
      ? `${description.slice(0, 120)}…`
      : description || '';

  return {
    id: post.id,
    title: post.title || 'Публикация',
    description: shortDescription,
    fullDescription: description || '',
    authorName: post.author_username || post.author?.username || 'Автор',
    categoryName: post.category_name || post.category?.name || 'Ремесло',
    imageUrl: resolveMediaUrl(post.image_url || post.images?.[0]?.image_url || post.images?.[0]?.url),
    createdAt: formatPostDate(post.created_at),
    likesCount: post.likes_count ?? 0,
    commentsCount: post.comments_count ?? 0,
  };
}
