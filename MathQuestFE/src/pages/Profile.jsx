
import React from 'react'
import { api } from '../lib/api.js'
import Spinner from '../components/Spinner.jsx'
import ErrorBanner from '../components/ErrorBanner.jsx'
import ProgressBar from '../components/ProgressBar.jsx'

export default function Profile() {
  const [data, setData] = React.useState(null)
  const [error, setError] = React.useState(null)

  React.useEffect(() => {
    api.getProfile().then(setData).catch(e => setError(e.payload?.message || e.message))
  }, [])

  if (error) return <ErrorBanner message={error} />
  if (!data) return <div className="flex items-center gap-2 text-gray-600"><Spinner/> Loading profile…</div>

  return (
    <div className="space-y-3">
      <div className="rounded-xl bg-white p-4 border">
        <div className="text-sm text-gray-600">Total XP</div>
        <div className="text-2xl font-bold">{data.total_xp}</div>
      </div>
      <div className="rounded-xl bg-white p-4 border">
        <div className="text-sm text-gray-600">Streak</div>
        <div className="text-xl font-semibold">{data.streak.current} <span className="text-sm text-gray-500">(best {data.streak.best})</span></div>
      </div>
      <div className="rounded-xl bg-white p-4 border">
        <div className="text-sm text-gray-600 mb-2">Overall Progress</div>
        <ProgressBar value={data.progress_percentage / 100} />
        <div className="text-xs text-gray-500 mt-1">{data.progress_percentage}%</div>
      </div>
      <div className="text-xs text-gray-500">
        Lessons completed: {data.lessons_completed} / {data.lessons_total}
      </div>
    </div>
  )
}
