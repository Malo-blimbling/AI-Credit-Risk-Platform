import { useEffect, useState } from 'react'
import KpiCard from './KpiCard'
import RecentRequestsTable from './RecentRequestsTable'
import { getHistory, getMetrics, type ApiCredentials, type DashboardMetrics, type PredictionRecord } from './api'

type DashboardProps = {
  credentials: ApiCredentials
}

function Dashboard({ credentials }: DashboardProps) {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null)
  const [metricsError, setMetricsError] = useState('')
  const [requests, setRequests] = useState<PredictionRecord[]>([])
  const [historyError, setHistoryError] = useState('')
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    let isCurrent = true

    Promise.allSettled([getMetrics(credentials), getHistory(credentials)])
      .then(([metricsResult, historyResult]) => {
        if (!isCurrent) return

        if (metricsResult.status === 'fulfilled') {
          setMetrics(metricsResult.value)
        } else if (metricsResult.reason instanceof Error && metricsResult.reason.message.includes('(403)')) {
          setMetricsError('Les métriques sont réservées au rôle Responsable.')
        } else {
          setMetricsError('Les métriques sont temporairement indisponibles.')
        }

        if (historyResult.status === 'fulfilled') setRequests(historyResult.value)
        else setHistoryError('L’historique est temporairement indisponible.')
      })
      .finally(() => {
        if (isCurrent) setIsLoading(false)
      })

    return () => { isCurrent = false }
  }, [credentials])

  return (
    <div className="dashboard">
      <div className="dashboard-heading">
        <div>
          <p className="eyebrow">VUE D’ENSEMBLE</p>
          <h2>Activité du modèle</h2>
        </div>
        {isLoading && <span>Actualisation...</span>}
      </div>
      {metricsError && <p className="notice" role="status">{metricsError}</p>}
      <section className="kpi-grid" aria-label="Indicateurs du backend">
        <KpiCard label="Prédictions" value={metrics?.total ?? '—'} />
        <KpiCard label="Défaut moyen" value={metrics ? `${(metrics.avg_default * 100).toFixed(1)}%` : '—'} />
        <KpiCard label="Risque élevé" value={metrics ? `${(metrics.pct_high * 100).toFixed(1)}%` : '—'} />
        <KpiCard label="Dossiers référés" value={metrics?.referred ?? '—'} />
      </section>
      <RecentRequestsTable requests={requests} isLoading={isLoading} error={historyError} />
    </div>
  )
}

export default Dashboard
