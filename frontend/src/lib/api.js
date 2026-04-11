const BASE = 'https://abg-webapp-backend.onrender.com/api'
const KEY = import.meta.env.VITE_INTERNAL_KEY || ''

export async function api(path, opts = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...(KEY ? { 'x-internal-key': KEY } : {}),
    ...(opts.headers || {}),
  }

  const res = await fetch(`${BASE}${path}`, {
    ...opts,
    headers,
  })

  if (!res.ok) {
    throw new Error(await res.text())
  }

  return res.json()
}
