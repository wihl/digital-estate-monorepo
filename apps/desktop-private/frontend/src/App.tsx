import { useState, useEffect } from 'react'

interface Person {
    id: string;
    name: string;
    slug: string;
    bio: string;
}

function App() {
    const [status, setStatus] = useState<string>("Connecting to backend...")
    const [people, setPeople] = useState<Person[]>([])
    const [newName, setNewName] = useState("")
    const [newBio, setNewBio] = useState("")

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
                body: JSON.stringify({ name: newName, bio: newBio })
            })
            if (res.ok) {
                setNewName("")
                setNewBio("")
                fetchPeople()
            }
        } catch (err) {
            console.error(err)
        }
    }

    return (
        <div className="min-h-screen bg-gray-900 text-white p-8">
            <div className="max-w-4xl mx-auto">
                <h1 className="text-4xl font-bold mb-8 text-blue-400">Digital Estate MVP</h1>

                <div className="mb-8 p-4 bg-gray-800 rounded border border-gray-700">
                    <p className="text-sm text-gray-400">System Status: <span className="text-green-400">{status}</span></p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {/* List */}
                    <div>
                        <h2 className="text-2xl font-bold mb-4">People</h2>
                        <div className="space-y-4">
                            {people.length === 0 && <p className="text-gray-500">No people found.</p>}
                            {people.map(p => (
                                <div key={p.id} className="p-4 bg-gray-800 rounded hover:bg-gray-700 transition">
                                    <h3 className="text-xl font-bold">{p.name}</h3>
                                    <p className="text-xs text-gray-500 mb-2">ID: {p.id}</p>
                                    <p className="text-gray-300">{p.bio || "No biography"}</p>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Form */}
                    <div>
                        <h2 className="text-2xl font-bold mb-4">Add Person</h2>
                        <form onSubmit={handleAdd} className="bg-gray-800 p-6 rounded border border-gray-700 space-y-4">
                            <div>
                                <label className="block text-sm mb-1">Name</label>
                                <input
                                    className="w-full bg-gray-900 border border-gray-600 rounded p-2 focus:border-blue-500 outline-none"
                                    value={newName}
                                    onChange={e => setNewName(e.target.value)}
                                    placeholder="e.g. Grandma"
                                    required
                                />
                            </div>
                            <div>
                                <label className="block text-sm mb-1">Bio</label>
                                <textarea
                                    className="w-full bg-gray-900 border border-gray-600 rounded p-2 focus:border-blue-500 outline-none"
                                    value={newBio}
                                    onChange={e => setNewBio(e.target.value)}
                                    placeholder="Short biography..."
                                    rows={3}
                                />
                            </div>
                            <button
                                type="submit"
                                className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded transition"
                            >
                                Create Person
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default App
