import { useState, useEffect } from 'react';
import { Routes, Route, Navigate, useLocation } from 'react-router-dom';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import ProtectedRoute from './components/auth/ProtectedRoute';
import StaffRoute from './components/auth/StaffRoute';
import AdminLayout from './components/admin/AdminLayout';
import Home from './pages/Home';
import PostDetail from './pages/PostDetail';
import CreatePost from './pages/CreatePost';
import EditPost from './pages/EditPost';
import MyPosts from './pages/MyPosts';
import Login from './pages/Login';
import Register from './pages/Register';
import Profile from './pages/Profile';
import AdminIndex from './pages/admin/AdminIndex';
import AdminUsers from './pages/admin/AdminUsers';
import AdminCategories from './pages/admin/AdminCategories';
import AdminPosts from './pages/admin/AdminPosts';
import AdminLogs from './pages/admin/AdminLogs';
import About from './pages/info/About';
import Help from './pages/info/Help';
import Contacts from './pages/info/Contacts';
import Events from './pages/info/Events';

function ScrollToTop() {
  const { pathname } = useLocation();
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [pathname]);
  return null;
}

export default function App() {
  const [search, setSearch] = useState('');

  return (
    <div className="flex min-h-screen flex-col bg-gray-50">
      <ScrollToTop />
      <a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:rounded-lg focus:bg-white focus:px-3 focus:py-2">
        К основному содержимому
      </a>

      <header className="shrink-0">
        <Header search={search} onSearchChange={setSearch} />
      </header>

      <main id="main-content" className="flex-1">
        <div className="mx-auto w-full max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
          <Routes>
          <Route path="/" element={<Home search={search} />} />
          <Route
            path="/posts/new"
            element={
              <ProtectedRoute>
                <CreatePost />
              </ProtectedRoute>
            }
          />
          <Route
            path="/posts/:id/edit"
            element={
              <ProtectedRoute>
                <EditPost />
              </ProtectedRoute>
            }
          />
          <Route path="/posts/:id" element={<PostDetail />} />
          <Route
            path="/my-posts"
            element={
              <ProtectedRoute>
                <MyPosts />
              </ProtectedRoute>
            }
          />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <Profile />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin"
            element={
              <StaffRoute>
                <AdminLayout />
              </StaffRoute>
            }
          >
            <Route index element={<AdminIndex />} />
            <Route path="users" element={<AdminUsers />} />
            <Route path="categories" element={<AdminCategories />} />
            <Route path="posts" element={<AdminPosts />} />
            <Route path="logs" element={<AdminLogs />} />
          </Route>
          <Route path="/activity-log" element={<Navigate to="/admin/logs" replace />} />
          <Route path="/about" element={<About />} />
          <Route path="/help" element={<Help />} />
          <Route path="/contacts" element={<Contacts />} />
          <Route path="/events" element={<Events />} />
          </Routes>
        </div>
      </main>

      <footer className="shrink-0">
        <Footer />
      </footer>
    </div>
  );
}
