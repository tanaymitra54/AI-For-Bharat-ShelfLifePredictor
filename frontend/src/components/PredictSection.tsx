'use client'

import { useState } from 'react'

interface PredictionData {
  foodType: string
  storageType: string
  temperature: string
  humidity: string
  daysStored: string
}

interface PredictionResult {
  predictedShelfLife: number
  freshnessScore: number
  riskLevel: 'low' | 'medium' | 'high'
  recommendations: string[]
}

export function PredictSection() {
  const [formData, setFormData] = useState<PredictionData>({
    foodType: '',
    storageType: '',
    temperature: '',
    humidity: '',
    daysStored: ''
  })
  const [result, setResult] = useState<PredictionResult | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const foodTypes = [
    'Dairy', 'Meat', 'Vegetables', 'Fruits', 'Bakery', 'Seafood'
  ]

  const storageTypes = [
    'Refrigerator', 'Freezer', 'Pantry'
  ]

  const handleInputChange = (field: keyof PredictionData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  const handlePredict = async () => {
    if (!formData.foodType || !formData.storageType || !formData.temperature || !formData.humidity || !formData.daysStored) {
      alert('Please fill in all fields')
      return
    }

    setIsLoading(true)
    
    // Simulate API call
    setTimeout(() => {
      const mockResult: PredictionResult = {
        predictedShelfLife: Math.floor(Math.random() * 10) + 1,
        freshnessScore: Math.floor(Math.random() * 40) + 60,
        riskLevel: (Math.random() > 0.7 ? 'high' : Math.random() > 0.4 ? 'medium' : 'low'),
        recommendations: [
          'Store in airtight container',
          'Keep away from direct sunlight',
          'Check for signs of spoilage regularly'
        ]
      }
      setResult(mockResult)
      setIsLoading(false)
    }, 2000)
  }

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'low': return 'risk-low'
      case 'medium': return 'risk-medium'
      case 'high': return 'risk-high'
      default: return 'risk-low'
    }
  }

  const getRiskBgColor = (risk: string) => {
    switch (risk) {
      case 'low': return 'bg-green-500/20 border-green-500'
      case 'medium': return 'bg-yellow-500/20 border-yellow-500'
      case 'high': return 'bg-red-500/20 border-red-500'
      default: return 'bg-green-500/20 border-green-500'
    }
  }

  return (
    <div className="animate-fadeIn">
      <div className="grid lg:grid-cols-2 gap-8">
        {/* Input Form */}
        <div className="glass-effect rounded-2xl p-8 border border-gray-700">
          <h2 className="text-2xl font-bold mb-6 text-gradient font-poppins">
            🍎 Food Details
          </h2>
          
          <div className="space-y-6">
            {/* Food Type */}
            <div>
              <label className="block text-sm font-semibold text-royal-green mb-2">
                Food Type *
              </label>
              <select
                value={formData.foodType}
                onChange={(e) => handleInputChange('foodType', e.target.value)}
                className="input-field"
              >
                <option value="">Select food type</option>
                {foodTypes.map(type => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
            </div>

            {/* Storage Type */}
            <div>
              <label className="block text-sm font-semibold text-royal-green mb-2">
                Storage Type *
              </label>
              <select
                value={formData.storageType}
                onChange={(e) => handleInputChange('storageType', e.target.value)}
                className="input-field"
              >
                <option value="">Select storage type</option>
                {storageTypes.map(type => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
            </div>

            {/* Temperature */}
            <div>
              <label className="block text-sm font-semibold text-royal-green mb-2">
                Temperature (°C) *
              </label>
              <input
                type="number"
                value={formData.temperature}
                onChange={(e) => handleInputChange('temperature', e.target.value)}
                placeholder="e.g., 4"
                className="input-field"
              />
            </div>

            {/* Humidity */}
            <div>
              <label className="block text-sm font-semibold text-royal-green mb-2">
                Humidity (%) *
              </label>
              <input
                type="number"
                value={formData.humidity}
                onChange={(e) => handleInputChange('humidity', e.target.value)}
                placeholder="e.g., 65"
                min="0"
                max="100"
                className="input-field"
              />
            </div>

            {/* Days Stored */}
            <div>
              <label className="block text-sm font-semibold text-royal-green mb-2">
                Days Stored *
              </label>
              <input
                type="number"
                value={formData.daysStored}
                onChange={(e) => handleInputChange('daysStored', e.target.value)}
                placeholder="e.g., 2"
                min="0"
                className="input-field"
              />
            </div>

            {/* Predict Button */}
            <button
              onClick={handlePredict}
              disabled={isLoading}
              className="w-full btn-primary text-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2 mt-8"
            >
              {isLoading ? (
                <>
                  <div className="loading-spinner"></div>
                  <span>Analyzing...</span>
                </>
              ) : (
                <>
                  <span>🔮</span>
                  <span>Predict Shelf Life</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Results */}
        <div className="space-y-6">
          {result ? (
            <div className="animate-fadeIn">
              {/* Analysis Result Card */}
              <div className="glass-effect rounded-2xl p-8 border border-gray-700 card-hover">
                <h3 className="text-xl font-bold mb-6 text-gradient font-poppins">
                  📊 Analysis Result
                </h3>
                
                <div className="space-y-6">
                  {/* Predicted Shelf Life */}
                  <div className="bg-gray-800/50 rounded-xl p-4 border border-gray-700">
                    <div className="flex justify-between items-center">
                      <span className="text-gray-400">Predicted Shelf Life</span>
                      <span className="text-2xl font-bold text-leaf-green">
                        {result.predictedShelfLife} days
                      </span>
                    </div>
                  </div>

                  {/* Freshness Score */}
                  <div className="bg-gray-800/50 rounded-xl p-4 border border-gray-700">
                    <div className="mb-2">
                      <span className="text-gray-400">Freshness Score</span>
                    </div>
                    <div className="flex items-center space-x-4">
                      <div className="flex-1">
                        <div className="progress-bar">
                          <div 
                            className="progress-fill"
                            style={{ width: `${result.freshnessScore}%` }}
                          ></div>
                        </div>
                      </div>
                      <span className="text-xl font-bold text-leaf-green">
                        {result.freshnessScore}%
                      </span>
                    </div>
                  </div>

                  {/* Risk Level */}
                  <div className={`rounded-xl p-4 border ${getRiskBgColor(result.riskLevel)}`}>
                    <div className="flex justify-between items-center">
                      <span className="text-gray-400">Risk Level</span>
                      <span className={`text-xl font-bold capitalize ${getRiskColor(result.riskLevel)}`}>
                        {result.riskLevel}
                      </span>
                    </div>
                  </div>

                  {/* Recommendations */}
                  <div className="bg-gray-800/50 rounded-xl p-4 border border-gray-700">
                    <div className="mb-3">
                      <span className="text-gray-400">Recommendations</span>
                    </div>
                    <ul className="space-y-2">
                      {result.recommendations.map((rec, index) => (
                        <li key={index} className="flex items-start space-x-2">
                          <span className="text-leaf-green mt-1">•</span>
                          <span className="text-gray-300 text-sm">{rec}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="glass-effect rounded-2xl p-12 border border-gray-700 text-center">
              <div className="w-20 h-20 bg-gray-800 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-3xl">🔮</span>
              </div>
              <h3 className="text-xl font-semibold mb-2 text-gray-400">
                No Analysis Yet
              </h3>
              <p className="text-gray-500">
                Fill in the food details and click "Predict Shelf Life" to get your analysis
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
