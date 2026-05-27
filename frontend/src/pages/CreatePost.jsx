import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api/axios';
import { createPost } from '../api/posts';
import PostForm from '../components/post/PostForm';

export default function CreatePost() {
  const navigate = useNavigate();
  const [categories, setCategories] = useState([]);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    api.get('/categories/').then((r) => setCategories(r.data)).catch(console.error);
  }, []);

  const handleSubmit = async (formData) => {
    setSubmitting(true);
    try {
      const post = await createPost(formData);
      navigate(`/posts/${post.id}`);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="mx-auto max-w-xl">
      <Link to="/my-posts" className="mb-3 inline-block text-sm text-craft-brown/80 hover:underline">
        ← Мои публикации
      </Link>
      <h1 className="mb-4 text-xl font-bold text-craft-brown">Новая публикация</h1>
      <div className="rounded-2xl border-2 border-craft-brown bg-craft-beige p-3">
        <PostForm
          categories={categories}
          onSubmit={handleSubmit}
          submitting={submitting}
          submitLabel="Опубликовать"
        />
      </div>
    </div>
  );
}
