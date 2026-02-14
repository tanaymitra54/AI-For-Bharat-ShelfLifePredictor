import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface PredictionRequest {
  food_type: string
  storage_type: string
  temperature: number
  humidity: number
  days_stored: number
}

export interface PredictionResponse {
  predicted_shelf_life: number
  freshness_score: number
  risk_level: 'low' | 'medium' | 'high'
  recommendations: string[]
}

export interface ChatRequest {
  message: string
  context?: string
}

export interface ChatResponse {
  response: string
  timestamp: string
}

export const predictShelfLife = async (data: PredictionRequest): Promise<PredictionResponse> => {
  try {
    const response = await api.post('/api/predict', data)
    return response.data
  } catch (error) {
    console.error('Prediction API error:', error)
    throw error
  }
}

export const sendChatMessage = async (data: ChatRequest): Promise<ChatResponse> => {
  try {
    const response = await api.post('/api/chat', data)
    return response.data
  } catch (error) {
    console.error('Chat API error:', error)
    throw error
  }
}

export const getVoiceTranscription = async (audioBlob: Blob): Promise<{ text: string }> => {
  try {
    const formData = new FormData()
    formData.append('audio', audioBlob, 'recording.wav')
    
    const response = await api.post('/api/voice/transcribe', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  } catch (error) {
    console.error('Voice transcription error:', error)
    throw error
  }
}
