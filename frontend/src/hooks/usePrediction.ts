import { useState } from 'react'
import { predictShelfLife, PredictionRequest, PredictionResponse } from '@/services/api'

export const usePrediction = () => {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<PredictionResponse | null>(null)

  const predict = async (data: PredictionRequest) => {
    setIsLoading(true)
    setError(null)
    
    try {
      const response = await predictShelfLife(data)
      setResult(response)
      return response
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Prediction failed'
      setError(errorMessage)
      throw err
    } finally {
      setIsLoading(false)
    }
  }

  const reset = () => {
    setResult(null)
    setError(null)
  }

  return {
    predict,
    isLoading,
    error,
    result,
    reset
  }
}
