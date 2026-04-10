import { useEffect, useState } from 'react'
import { api } from './lib/api'
import { ChangelogModal } from './components/ChangelogModal'

const statuses = ['New','In Review','Duplicate Found','Duplicate Sent to ABG','Clarification Needed','Clarification Received','New Record Required','In PROSOL','PROSOL Completed','Created in Master','Closed']

const seedChanges = [
  { version: 'v0.1.0', date: '2026-04-10', details: 'Initial ABG Web App MVP with workflow orchestration and mock integrations.', author: 'Codex' },
  { version: 'v0.0.9', date: '2026-04-10', details: 'Added duplicate, clarification, and new-item branch handling.', author: 'Codex' },
  { version: 'v0.0.8', date: '2026-04-10', details: 'Implemented SharePoint typed mapping and ABG code generator.', author: 'Codex' },
  { version: 'v0.0.7', date: '2026-04-10', details: 'Added PROSOL manual return flow and finalization.', author: 'Codex' },
  { version: 'v0.0.6', date: '2026-04-10', details: 'Introduced luxurious responsive UI with dark mode.', author: 'Codex' },
  { version: 'v0.0.5', date: '2026-04-10', details: 'Created dashboard filters and case detail UX.', author: 'Codex' }
]

export default function App() {
  const [dark, setDark] = useState(true)
  const [cases, setCases] = useState([])
  const [selected, setSelected] = useState(null)
  const [form, setForm] = useState({ requestId: '', title: '', senderEmail: '', emailSubject: '', rawInputText: '', status: 'New' })
  const [changelogOpen, setChangelogOpen] = useState(false)
  const [clarificationQuestion, setClarificationQuestion] = useState('Please share brand, dimensions, and any part number.')
  const [prosol, setProsol] = useState({ unspsc: '', shortDescription: '', longDescription: '', internalNote: '' })

  const refresh = () => api('/cases').then(setCases).catch(() => setCases([]))
  useEffect(() => { refresh() }, [])
  useEffect(() => { document.documentElement.classList.toggle('dark', dark) }, [dark])

  async function createCase() {
    await api('/cases', { method: 'POST', body: JSON.stringify({ ...form }) })
    setForm({ requestId: '', title: '', senderEmail: '', emailSubject: '', rawInputText: '', status: 'New' }); refresh()
  }

  async function runMatch() { await api(`/cases/${selected.requestId}/match`, { method: 'POST' }); refresh() }
  async function sendDuplicate() { await api(`/workflow/${selected.requestId}/duplicate/send`, { method: 'POST' }); refresh() }
  async function sendClarification() { await api(`/workflow/${selected.requestId}/clarification/send`, { method: 'POST', body: JSON.stringify({ question: clarificationQuestion }) }); refresh() }
  async function markNew() { await api(`/workflow/${selected.requestId}/mark-new`, { method: 'POST' }); refresh() }
  async function saveProsol() { await api(`/workflow/${selected.requestId}/prosol`, { method: 'POST', body: JSON.stringify(prosol) }); refresh() }
  async function finalize() { await api(`/workflow/${selected.requestId}/finalize`, { method: 'POST' }); refresh() }

  return (
    <div className="max-w-7xl mx-auto p-4 md:p-8 space-y-4">
      <header className="card flex justify-between items-center"><h1 className="text-2xl font-bold">ABG Web App</h1><div className="flex gap-2"><button className="btn" onClick={() => setChangelogOpen(true)}>Changelog</button><button className="btn" onClick={() => setDark(!dark)}>{dark ? 'Light' : 'Dark'} Mode</button></div></header>
      <section className="grid md:grid-cols-2 gap-4">
        <div className="card">
          <h2 className="font-semibold mb-3">Dashboard / Queue</h2>
          <div className="overflow-auto"><table className="w-full text-sm"><thead><tr><th>ID</th><th>Sender</th><th>Status</th><th></th></tr></thead><tbody>{cases.map(c => <tr key={c.requestId} className="border-t border-white/10"><td>{c.requestId}</td><td>{c.senderEmail}</td><td>{c.status}</td><td><button className="btn" onClick={() => setSelected(c)}>Open</button></td></tr>)}</tbody></table></div>
        </div>
        <div className="card space-y-2">
          <h2 className="font-semibold">Request Intake / Case Detail</h2>
          {['requestId','title','senderEmail','emailSubject','rawInputText'].map(k => <input key={k} className="input" placeholder={k} value={form[k]} onChange={e => setForm({ ...form, [k]: e.target.value })} />)}
          <select className="input" value={form.status} onChange={e => setForm({ ...form, status: e.target.value })}>{statuses.map(s => <option key={s}>{s}</option>)}</select>
          <button className="btn" onClick={createCase}>Save Case</button>
        </div>
      </section>

      {selected && <section className="grid md:grid-cols-2 gap-4">
        <div className="card space-y-2">
          <h3 className="font-semibold">MDM-GPT Match Results</h3>
          <div>Request: {selected.requestId}</div>
          <div>Input: {selected.rawInputText}</div>
          <div>Status: {selected.status}</div>
          <button className="btn" onClick={runMatch}>Send to MDM-GPT</button>
          <button className="btn" onClick={sendDuplicate}>Send Duplicate Email</button>
          <button className="btn" onClick={markNew}>Mark New Item Required</button>
          <div className="space-y-1"><input className="input" value={clarificationQuestion} onChange={e => setClarificationQuestion(e.target.value)} /><button className="btn" onClick={sendClarification}>Send Clarification</button></div>
        </div>
        <div className="card space-y-2">
          <h3 className="font-semibold">PROSOL Return + Final New Record</h3>
          {['unspsc','shortDescription','longDescription','internalNote'].map(k => <input key={k} className="input" placeholder={k} value={prosol[k]} onChange={e => setProsol({ ...prosol, [k]: e.target.value })} />)}
          <button className="btn" onClick={saveProsol}>Save PROSOL Result</button>
          <button className="btn" onClick={finalize}>Create Master + Send Final Email</button>
        </div>
      </section>}

      <footer className="text-center text-xs opacity-70">ABG Web App · Internal Cataloguing Workflow</footer>
      <ChangelogModal open={changelogOpen} onClose={() => setChangelogOpen(false)} entries={seedChanges} />
    </div>
  )
}
