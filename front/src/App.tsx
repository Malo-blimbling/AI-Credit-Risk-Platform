
// App.tsx
import { useState, type FormEvent } from 'react'
import { checkBackend, type ApiCredentials } from './api'
import { Navbar } from './Navbar'
import Dashboard from './Dashboard'

function App() {
  const [credentials, setCredentials] = useState<ApiCredentials | null>(null)
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [loginError, setLoginError] = useState('')
  const [isConnecting, setIsConnecting] = useState(false)

  async function handleLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setIsConnecting(true)
    setLoginError('')

    try {
      await checkBackend({ username, password })
      setCredentials({ username, password })
      setPassword('')
    } catch {
      setLoginError('Connexion refusée. Vérifiez vos identifiants et la disponibilité du backend.')
    } finally {
      setIsConnecting(false)
    }
  }

  return (
    <div className="app-shell">
      <Navbar title="AI Credit Risk" />
      {credentials ? (
        <>
          <button className="logout-button" onClick={() => setCredentials(null)}>Se déconnecter</button>
          <Dashboard credentials={credentials} />
        </>
      ) : (
        <main className="login-panel">
          <p className="eyebrow">PLATEFORME DE DÉCISION</p>
          <h2>Connexion au backend</h2>
          <form onSubmit={handleLogin}>
            <label htmlFor="username">Identifiant</label>
            <input id="username" autoComplete="username" value={username} onChange={(event) => setUsername(event.target.value)} required />
            <label htmlFor="password">Mot de passe</label>
            <input id="password" type="password" autoComplete="current-password" value={password} onChange={(event) => setPassword(event.target.value)} required />
            {loginError && <p className="error-message" role="alert">{loginError}</p>}
            <button type="submit" disabled={isConnecting}>{isConnecting ? 'Connexion...' : 'Se connecter'}</button>
          </form>
        </main>
      )}
    </div>
  )
}

export default App