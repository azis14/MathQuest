
import React from 'react'
import { NavLink, Routes, Route } from 'react-router-dom'
import LessonsList from './pages/LessonsList.jsx'
import LessonPlay from './pages/LessonPlay.jsx'
import Profile from './pages/Profile.jsx'
import NotFound from './pages/NotFound.jsx'

export default function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="sticky top-0 z-10 bg-white/90 backdrop-blur border-b">
        <nav className="max-w-screen-sm mx-auto px-4 py-3 flex items-center justify-between">
          <span className="font-bold text-indigo-600">MathQuest</span>
          <div className="flex gap-4 text-sm">
            <NavLink to="/" className={({isActive}) => isActive ? 'text-indigo-600 font-semibold' : 'text-gray-600'}>Lessons</NavLink>
            <NavLink to="/profile" className={({isActive}) => isActive ? 'text-indigo-600 font-semibold' : 'text-gray-600'}>Profile</NavLink>
          </div>
        </nav>
      </header>

      <main className="flex-1 max-w-screen-sm mx-auto w-full px-4 py-4">
        <Routes>
          <Route path="/" element={<LessonsList />} />
          <Route path="/lesson/:lessonId" element={<LessonPlay />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </main>
      <footer className="border-t py-4 text-center text-xs text-gray-500">
        © {new Date().getFullYear()} MathQuest
      </footer>
    </div>
  )
}
