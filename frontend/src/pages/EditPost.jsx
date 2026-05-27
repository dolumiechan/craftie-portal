import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import api from '../api/axios';
import { fetchPostById, updatePost } from '../api/posts';
import { useAuth } from '../context/AuthContext';
import PostForm from '../components/post/PostForm';

export default function EditPost() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [post, setPost] = useState(null);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        const [postData, cats] = await Promise.all([
          fetchPostById(id),
          api.get('/categories/').then((r) => r.data),
        ]);
        if (user && postData.author_id !== user.id) {
          setError('Нет прав на редактирование.');
          return;
        }
        setPost(postData);
        setCategories(cats);
      } catch {
        setError('Публикация не найдена.');
      } finally {
        setLoading(false);
      }
    };
    if (user) load();
  }, [id, user]);

  const handleSubmit = async (formData) => {
    setSubmitting(true);
    try {
      await updatePost(id, formData);
      navigate(`/posts/${id}`);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return <p className="text-center text-sm text-craft-brown/70">Загрузка…</p>;
  }

  if (error) {
    return (
      <p className="text-center text-sm text-red-800">
        {error}{' '}
        <Link to="/my-posts" className="underline">
          Назад
        </Link>
      </p>
    );
  }

  return (
    <div className="mx-auto max-w-xl">
      <Link to={`/posts/${id}`} className="mb-4 inline-block text-sm text-craft-brown/80 hover:underline">
        ← К публикации
      </Link>
      <h1 className="mb-6 text-2xl font-bold text-craft-brown">Редактирование</h1>
      <div className="rounded-2xl border-2 border-craft-brown bg-craft-beige p-6 sm:p-8">
        <PostForm
          initial={post}
          categories={categories}
          onSubmit={handleSubmit}
          submitting={submitting}
          submitLabel="Сохранить изменения"
        />
      </div>
    </div>
  );
}
