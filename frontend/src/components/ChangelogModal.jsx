import { useState } from 'react'

export function ChangelogModal({ open, onClose, entries }) {
  const [showAll, setShowAll] = useState(false)
  if (!open) return null
  const visible = showAll ? entries : entries.slice(0, 5)
  return (
    <div className="fixed inset-0 bg-black/60 grid place-items-center p-4">
      <div className="card w-full max-w-2xl">
        <div className="flex justify-between items-center mb-3"><h2 className="text-xl font-semibold">Changelog</h2><button onClick={onClose}>✕</button></div>
        <div className="space-y-3 max-h-96 overflow-auto">
          {visible.map((e) => <div key={e.version} className="border border-white/10 rounded-lg p-3"><div className="font-semibold">{e.version} · {e.date}</div><div className="text-sm opacity-90">{e.details}</div><div className="text-xs opacity-70">By {e.author}</div></div>)}
        </div>
        <button className="btn mt-3" onClick={() => setShowAll(!showAll)}>{showAll ? 'Show Less' : 'Show More'}</button>
      </div>
    </div>
  )
}
