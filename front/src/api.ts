export type ApiCredentials = {
  username: string
  password: string
}

export type PredictionRecord = {
  date: string
  clientId: string
  probabilityOfDefault: number
  riskCategory: 'LOW' | 'MEDIUM' | 'HIGH'
  decisionStatus: string
}

export type DashboardMetrics = {
  total: number
  avg_default: number
  pct_high: number
  referred: number
}

function authHeaders(credentials: ApiCredentials) {
  return {
    Authorization: `Basic ${window.btoa(`${credentials.username}:${credentials.password}`)}`,
    Accept: 'application/json',
  }
}

async function apiGet<T>(path: string, credentials: ApiCredentials): Promise<T> {
  const response = await fetch(path, { headers: authHeaders(credentials) })
  if (!response.ok) throw new Error(`Erreur API (${response.status})`)
  return response.json() as Promise<T>
}

export async function checkBackend(credentials: ApiCredentials) {
  const response = await fetch('/api/health', { headers: authHeaders(credentials) })
  if (!response.ok) throw new Error(`Erreur API (${response.status})`)
  return response.text()
}

export function getMetrics(credentials: ApiCredentials) {
  return apiGet<DashboardMetrics>('/api/metrics', credentials)
}

export function getHistory(credentials: ApiCredentials) {
  return apiGet<PredictionRecord[]>('/api/history?limit=20', credentials)
}