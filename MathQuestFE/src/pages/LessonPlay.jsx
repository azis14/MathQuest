
import React from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { api, uuidv4 } from '../lib/api.js'
import Spinner from '../components/Spinner.jsx'
import ErrorBanner from '../components/ErrorBanner.jsx'
import ProgressBar from '../components/ProgressBar.jsx'

function MCQ({ p, value, onChange }) {
  return (
    <div className="space-y-2">
      <div className="font-medium">{p.prompt}</div>
      <div className="grid grid-cols-1 gap-2">
        {p.options.map(opt => (
          <label key={opt.id} className={"border rounded-lg px-3 py-2 flex items-center gap-2 " + (value === opt.id ? "border-indigo-500 bg-indigo-50" : "hover:bg-gray-50")}>
            <input
              type="radio"
              name={`p-${p.id}`}
              checked={value === opt.id}
              onChange={() => onChange(opt.id)}
              className="accent-indigo-600"
            />
            <span>{opt.label}</span>
          </label>
        ))}
      </div>
    </div>
  )
}

function InputQ({ p, value, onChange }) {
  return (
    <div className="space-y-2">
      <div className="font-medium">{p.prompt}</div>
      <input
        type="text"
        inputMode="numeric"
        value={value ?? ''}
        onChange={(e) => onChange(e.target.value)}
        className="w-full rounded-lg border px-3 py-2"
        placeholder="Type your answer"
      />
    </div>
  )
}

export default function LessonPlay() {
  const { lessonId } = useParams()
  const navigate = useNavigate()
  const [lesson, setLesson] = React.useState(null)
  const [error, setError] = React.useState(null)
  const [answers, setAnswers] = React.useState({})
  const [submitting, setSubmitting] = React.useState(false)
  const [result, setResult] = React.useState(null)
  const attemptRef = React.useRef(uuidv4())

  React.useEffect(() => {
    api.getLesson(lessonId)
      .then(setLesson)
      .catch(e => setError(e.payload?.message || e.message))
  }, [lessonId])

  function updateAnswer(pid, val) {
    setAnswers(prev => ({ ...prev, [pid]: val }))
  }

  async function onSubmit() {
    if (!lesson) return
    const payload = {
      attempt_id: attemptRef.current,
      answers: lesson.problems.map(p => {
        const v = answers[p.id]
        if (p.type === 'MCQ') return { problem_id: p.id, option_id: v }
        return { problem_id: p.id, value: v }
      }).filter(a => a.option_id !== undefined || a.value !== undefined)
    }
    if (payload.answers.length === 0) {
      setError("answers must be non-empty")
      return
    }
    setSubmitting(true)
    try {
      const res = await api.submitLesson(lesson.id, payload)
      setResult(res)
      attemptRef.current = uuidv4()
    } catch (e) {
      setError(e.payload?.message || e.message)
    } finally {
      setSubmitting(false)
    }
  }

  if (error) return <ErrorBanner message={error} />
  if (!lesson) return <div className="flex items-center gap-2 text-gray-600"><Spinner/> Loading lesson…</div>

  return (
    <div className="pb-24">
      <h1 className="text-xl font-bold">{lesson.title}</h1>
      <p className="text-sm text-gray-600 mb-4">{lesson.description}</p>

      <div className="space-y-4">
        {lesson.problems.map((p) => (
          <div key={p.id} className="rounded-xl bg-white p-4 border">
            {p.type === 'MCQ' ? (
              <MCQ p={p} value={answers[p.id]} onChange={(v) => updateAnswer(p.id, v)} />
            ) : (
              <InputQ p={p} value={answers[p.id]} onChange={(v) => updateAnswer(p.id, v)} />
            )}
          </div>
        ))}
      </div>

      <div className="fixed bottom-0 left-0 right-0 border-t bg-white p-3">
        <div className="max-w-screen-sm mx-auto flex gap-3">
          <button onClick={() => navigate(-1)} className="flex-1 border rounded-lg px-4 py-3">Back</button>
          <button
            onClick={onSubmit}
            disabled={submitting || Boolean(result)}
            className="flex-1 rounded-lg px-4 py-3 bg-indigo-600 text-white disabled:opacity-60 active:scale-[0.99] transition"
          >
            {submitting ? 'Submitting…' : 'Submit'}
          </button>
        </div>
      </div>

      {result && (
        <div className="fixed inset-0 bg-black/40 flex items-end sm:items-center justify-center p-4">
          <div className="w-full max-w-sm bg-white rounded-2xl p-4 border" onClick={e => e.stopPropagation()}>
            <h2 className="text-lg font-semibold">Nice work!</h2>
            <div className="text-sm text-gray-600 mt-1">You answered <b>{result.correct_count}</b> correctly.</div>
            <div className="mt-3 rounded-lg bg-indigo-50 p-3">
              <div className="text-sm">+{result.earned_xp} XP</div>
              <div className="text-xs text-gray-600">Total: {result.new_total_xp} XP</div>
            </div>
            <div className="mt-3">
              <div className="text-sm font-medium">Progress</div>
              <ProgressBar value={result.lesson_progress} />
              <div className="text-xs text-gray-500 mt-1">{Math.round(result.lesson_progress * 100)}%</div>
            </div>
            <div className="mt-3 text-sm">
              Streak: <span className="font-semibold">{result.streak.current}</span> (best {result.streak.best})
              {result.streak.current > 1 && <span className="ml-2">🔥</span>}
            </div>
            <div className="mt-4 flex gap-2">
              <button className="flex-1 rounded-lg px-4 py-2 bg-indigo-600 text-white" onClick={() => { setResult(null); navigate('/'); }}>Continue</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
