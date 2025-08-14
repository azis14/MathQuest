
const BASE = import.meta.env.VITE_API_URL || ''

async function http(path, options = {}) {
  const res = await fetch(BASE + path, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  })
  if (!res.ok) {
    let payload = {}
    try { payload = await res.json() } catch {}
    const err = new Error(payload?.message || `HTTP ${res.status}`)
    err.status = res.status
    err.payload = payload
    throw err
  }
  return res.json()
}

export const api = {
  listLessons: () => http('/api/lessons'),
  getLesson: (id) => http(`/api/lessons/${id}`),
  submitLesson: (id, body) => http(`/api/lessons/${id}/submit`, { method: 'POST', body: JSON.stringify(body) }),
  getProfile: () => http('/api/profile'),
}

export function uuidv4() {
  if (crypto?.randomUUID) return crypto.randomUUID()
  // Fallback
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
    const r = (Math.random() * 16) | 0
    const v = c === 'x' ? r : (r & 0x3) | 0x8
    return v.toString(16)
  })
}
