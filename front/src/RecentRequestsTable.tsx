import { useState } from 'react'
import type { PredictionRecord } from './api'
import useSortedRequests from './hooks/useSortedRequests'

type RecentRequestsTableProps = {
  requests: PredictionRecord[]
  isLoading: boolean
  error: string
}

function RecentRequestsTable({ requests, isLoading, error }: RecentRequestsTableProps) {
  const [sortBy, setSortBy] = useState<'date' | 'probabilityOfDefault'>('date')
  const [search, setSearch] = useState('')
  const sortedRequests = useSortedRequests(requests, sortBy)
  const filteredRequests = sortedRequests.filter((request) =>
    `${request.clientId} ${request.riskCategory} ${request.decisionStatus}`
      .toLowerCase()
      .includes(search.toLowerCase()),
  )

  return (
    <div className="recent-requests">
      <div className="section-heading">
        <div>
          <p className="eyebrow">DERNIÈRES ACTIVITÉS</p>
          <h2>Historique des prédictions</h2>
        </div>
      </div>
      <div className="search-and-sort">
        <div className="search-box">
          <label className="visually-hidden" htmlFor="history-search">Rechercher dans l’historique</label>
          <input
            id="history-search"
            type="text"
            placeholder="Rechercher une référence ou un risque..."
            value={search}
            onChange={(event) => setSearch(event.target.value)}
          />
        </div>

        <div className="sort-buttons">
          <button aria-pressed={sortBy === 'date'} onClick={() => setSortBy('date')}>
            Plus récents
          </button>
          <button aria-pressed={sortBy === 'probabilityOfDefault'} onClick={() => setSortBy('probabilityOfDefault')}>
            Risque le plus élevé
          </button>
        </div>
      </div>

      {error && <p className="error-message" role="alert">{error}</p>}
      <table className="recent-requests-table">
        <thead>
          <tr>
            <th>Référence</th>
            <th>Probabilité de défaut</th>
            <th>Niveau de risque</th>
            <th>Décision</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {filteredRequests.map((request) => (
            <tr key={`${request.clientId}-${request.date}`}>
              <td>{request.clientId}</td>
              <td>{(request.probabilityOfDefault * 100).toFixed(1)}%</td>
              <td><span className={`risk-label risk-${request.riskCategory.toLowerCase()}`}>{request.riskCategory}</span></td>
              <td>{request.decisionStatus}</td>
              <td>{new Date(request.date).toLocaleString()}</td>
            </tr>
          ))}
          {!isLoading && filteredRequests.length === 0 && (
            <tr><td colSpan={5} className="empty-state">{requests.length ? 'Aucun résultat.' : 'Aucune prédiction enregistrée.'}</td></tr>
          )}
        </tbody>
      </table>
    </div>
  )
}

export default RecentRequestsTable
