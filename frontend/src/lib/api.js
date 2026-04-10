const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
const KEY = import.meta.env.VITE_INTERNAL_KEY || 'dev-internal-key'

export async function api(path, opts = {}) {
  const res = await fetch(`${BASE}${path}`, {
    ...opts,
    headers: { 'Content-Type': 'application/json', 'x-internal-key': KEY, ...(opts.headers || {}) }
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}
