
import React from 'react'
import { Link } from 'react-router-dom'
import { api } from '../lib/api.js'
import Spinner from '../components/Spinner.jsx'
import ProgressBar from '../components/ProgressBar.jsx'
import ErrorBanner from '../components/ErrorBanner.jsx'

export default function LessonsList() {
  const [data, setData] = React.useState(null)
  const [error, setError] = React.useState(null)

  React.useEffect(() => {
    let mounted = true
    api.listLessons().then(setData).catch(e => setError(e.payload?.message || e.message))
    return () => { mounted = false }
  }, [])

  if (error) return <ErrorBanner message={error} />
  if (!data) return <div className="flex items-center gap-2 text-gray-600"><Spinner/> Loading lessons…</div>

  return (
    <div className="space-y-3">
      {data.map(lesson => (
        <Link key={lesson.id} to={`/lesson/${lesson.id}`} className="block rounded-xl bg-white p-4 border hover:shadow-sm active:scale-[0.99] transition">
          <div className="flex items-center justify-between">
            <h3 className="font-semibold">{lesson.title}</h3>
            {lesson.completed && <span className="text-xs px-2 py-0.5 bg-green-100 text-green-700 rounded-full">Completed</span>}
          </div>
          <p className="text-sm text-gray-600 mt-1">{lesson.description}</p>
          <div className="mt-3">
            <ProgressBar value={lesson.progress} />
            <div className="text-xs text-gray-500 mt-1">{Math.round(lesson.progress * 100)}%</div>
          </div>
        </Link>
      ))}
    </div>
  )
}
