import { Route, Routes } from 'react-router-dom'
import Layout from './components/Layout.jsx'
import ProtectedRoute from './components/ProtectedRoute.jsx'
import HomePage from './pages/HomePage.jsx'
import CardListPage from './pages/CardListPage.jsx'
import CardDetailPage from './pages/CardDetailPage.jsx'
import CardNewPage from './pages/CardNewPage.jsx'
import CardEditPage from './pages/CardEditPage.jsx'
import LoginPage from './pages/LoginPage.jsx'
import NotFoundPage from './pages/NotFoundPage.jsx'

// 주소 → 페이지 연결표. 모든 페이지를 Layout 아래에 두어 헤더를 공통으로 쓴다.
// '/cards/new' 와 '/cards/:id' 는 순서와 상관없이 React Router 가 고정 경로(new)를 먼저 고른다.
// 등록·수정은 ProtectedRoute 아래에 두어 로그인한 사람만 들어간다.
export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<HomePage />} />
        <Route path="cards" element={<CardListPage />} />
        <Route path="cards/:id" element={<CardDetailPage />} />
        <Route element={<ProtectedRoute />}>
          <Route path="cards/new" element={<CardNewPage />} />
          <Route path="cards/:id/edit" element={<CardEditPage />} />
        </Route>
        <Route path="login" element={<LoginPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  )
}
