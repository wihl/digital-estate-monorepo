import { useState, useEffect } from 'react'

interface Person {
    id: string;
    display_name?: string;
    slug: string;
    bio: string;
}

function App() {
    const [status, setStatus] = useState<string>("Connecting to backend...")
    const [people, setPeople] = useState<Person[]>([])

    // V2 Fields
    const [family, setFamily] = useState("")
    const [given, setGiven] = useState("")
    const [dob, setDob] = useState("")
    const [bio, setBio] = useState("")

    const fetchPeople = () => {
        fetch('http://localhost:8000/api/people/')
            .then(res => res.json())
            .then(data => setPeople(data))
            .catch(err => console.error(err))
    }

    useEffect(() => {
        fetch('http://localhost:8000/health')
            .then(res => res.json())
            .then(data => setStatus(`Online: ${data.message}`))
            .catch(err => setStatus(`Offline: ${err}`))

        fetchPeople()
    }, [])

    const handleAdd = async (e: React.FormEvent) => {
        e.preventDefault()
        try {
            const res = await fetch('http://localhost:8000/api/people/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    family_name: family,
                    given_name: given,
                    dob: dob,
                    bio: bio
                })
            })
            if (res.ok) {
                setFamily("")
                setGiven("")
                setDob("")
                setBio("")
                fetchPeople()
            }
        } catch (err) {
            console.error(err)
        }
    }

    return (
        <div className="min-h-screen bg-gray-900 text-white p-8">
            <div className="max-w-4xl mx-auto">
                <h1 className="text-4xl font-bold mb-8 text-blue-400">Digital Estate MVP (Schema V2)</h1>

                <div className="mb-8 p-4 bg-gray-800 rounded border border-gray-700">
                    <p className="text-sm text-gray-400">System Status: <span className="text-green-400">{status}</span></p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {/* List */}
                    <div>
                        <h2 className="text-2xl font-bold mb-4">People Directory</h2>
                        <div className="space-y-4">
                            {people.length === 0 && <p className="text-gray-500">No people found.</p>}
                            {people.map(p => (
                                <div key={p.id} className="p-4 bg-gray-800 rounded hover:bg-gray-700 transition">
                                    <h3 className="text-xl font-bold">{p.display_name}</h3>
                                    <p className="text-xs text-gray-400 font-mono mb-2">{p.id}</p>
                                    <p className="text-xs text-gray-500 mb-2 truncate">PATH: {p.slug}</p>
                                    <p className="text-gray-300">{p.bio || "No biography"}</p>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Form */}
                    <div>
                        <h2 className="text-2xl font-bold mb-4">Add Person Entity</h2>
                        <form onSubmit={handleAdd} className="bg-gray-800 p-6 rounded border border-gray-700 space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm mb-1 text-gray-400">Given Name</label>
                                    <input
                                        className="w-full bg-gray-900 border border-gray-600 rounded p-2 outline-none"
                                        value={given}
                                        onChange={e => setGiven(e.target.value)}
                                        required
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm mb-1 text-gray-400">Family Name</label>
                                    <input
                                        className="w-full bg-gray-900 border border-gray-600 rounded p-2 outline-none"
                                        value={family}
                                        onChange={e => setFamily(e.target.value)}
                                        required
                                    />
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm mb-1 text-gray-400">Date of Birth (YYYY-MM-DD)</label>
                                <input
                                    type="date"
                                    className="w-full bg-gray-900 border border-gray-600 rounded p-2 outline-none"
                                    value={dob}
                                    onChange={e => setDob(e.target.value)}
                                    required
                                />
                            </div>

                            <div>
                                <label className="block text-sm mb-1 text-gray-400">Bio (Markdown)</label>
                                <textarea
                                    className="w-full bg-gray-900 border border-gray-600 rounded p-2 outline-none"
                                    value={bio}
                                    onChange={e => setBio(e.target.value)}
                                    rows={3}
                                />
                            </div>
                            <button
                                type="submit"
                                className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded transition"
                            >
                                Create V2 Entity
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default App
