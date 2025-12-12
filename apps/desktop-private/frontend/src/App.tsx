import { useState, useEffect } from 'react'

function App() {
    const [status, setStatus] = useState<string>("Connecting to backend...")

    useEffect(() => {
        fetch('http://localhost:8000/health')
            .then(res => res.json())
            .then(data => setStatus(`Backend says: ${data.message}`))
            .catch(err => setStatus(`Error connecting to backend: ${err}`))
    }, [])

    return (
        <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center">
            <h1 className="text-4xl font-bold mb-4 text-blue-400">Digital Estate MVP</h1>
            <div className="p-6 bg-gray-800 rounded-lg shadow-lg border border-gray-700">
                <p className="text-xl">System Status:</p>
                <p className="mt-2 text-green-400 font-mono">{status}</p>
            </div>
        </div>
    )
}

export default App
