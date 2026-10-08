import { useMemo } from 'react'
import type { PredictionRecord } from '../api'

function useSortedRequests(requests: PredictionRecord[], sortBy: 'probabilityOfDefault' | 'date') {
  return useMemo(() => {
    const copy = [...requests]
    if (sortBy === 'probabilityOfDefault') {
      return copy.sort((a, b) => b.probabilityOfDefault - a.probabilityOfDefault)
    }
    return copy.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
  }, [requests, sortBy])
}

export default useSortedRequests
