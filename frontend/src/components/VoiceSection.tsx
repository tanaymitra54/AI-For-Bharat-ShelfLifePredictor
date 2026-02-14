'use client'

import { useState } from 'react'

export function VoiceSection() {
  const [isRecording, setIsRecording] = useState(false)
  const [response, setResponse] = useState<string>('')
  const [isLoading, setIsLoading] = useState(false)

  const handleMicrophoneClick = async () => {
    setIsRecording(true)
    setIsLoading(true)
    
    // Simulate voice recording and processing
    setTimeout(() => {
      const mockResponse = "Based on your voice input, I've analyzed the food details. The predicted shelf life is approximately 5 more days with a freshness level of 85%. For optimal storage, keep refrigerated and check regularly for any signs of spoilage."
      
      setResponse(mockResponse)
      setIsLoading(false)
      setIsRecording(false)
    }, 3000)
  }

  return (
    <div className="animate-fadeIn">
      <div className="max-w-4xl mx-auto">
        {/* Main Voice Interface */}
        <div className="glass-effect rounded-3xl p-12 border border-gray-700 text-center">
          <h2 className="text-3xl font-bold mb-8 text-gradient font-poppins">
            🎤 Voice Assistant
          </h2>
          
          {/* Microphone Button */}
          <div className="flex justify-center mb-8">
            <button
              onClick={handleMicrophoneClick}
              disabled={isLoading}
              className={`relative w-40 h-40 rounded-full flex items-center justify-center transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed border-4 ${
                isRecording 
                  ? 'bg-pink animate-pulse border-black shadow-[6px_6px_0px_0px_rgba(0,0,0,1)]' 
                  : 'bg-royal-green hover:bg-leaf-green border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] active:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] active:translate-x-1 active:translate-y-1'
              }`}
            >
              {isLoading ? (
                <div className="loading-spinner w-16 h-16 border-4 border-white border-t-transparent rounded-full"></div>
              ) : (
                <svg className="w-20 h-20 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 15c1.66 0 3-1.34 3-3V6c0-1.66-1.34-3-3-3S9 4.34 9 6v6c0 1.66 1.34 3 3 3z"/>
                  <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
                </svg>
              )}
            </button>
          </div>

          <p className="text-gray-400 text-lg mb-8">
            {isRecording ? 'Recording...' : 'Click to start voice analysis'}
          </p>

          {/* Sound Wave Animation */}
          {isRecording && (
            <div className="flex justify-center items-center h-16 mb-8">
              <div className="flex space-x-1">
                {[...Array(15)].map((_, i) => (
                  <div
                    key={i}
                    className="w-1 bg-gradient-to-t from-royal-green to-pink rounded-full animate-soundWave"
                    style={{
                      height: `${Math.random() * 30 + 10}px`,
                      animationDelay: `${i * 0.1}s`
                    }}
                  ></div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Response Card */}
        {response && (
          <div className="mt-8 animate-fadeIn">
            <div className="glass-effect rounded-2xl p-8 border border-gray-700 card-hover">
              <div className="flex items-start space-x-4">
                <div className="w-12 h-12 bg-royal-green rounded-full flex items-center justify-center flex-shrink-0">
                  <span className="text-white font-bold text-lg">AI</span>
                </div>
                <div className="flex-1">
                  <h3 className="text-xl font-bold mb-3 font-poppins">Analysis Result</h3>
                  <p className="text-gray-300 leading-relaxed text-lg">
                    {response}
                  </p>
                  <div className="mt-4 flex items-center space-x-3 text-sm text-gray-500">
                    <span className="w-2 h-2 bg-leaf-green rounded-full"></span>
                    <span>Voice analysis complete</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Instructions */}
        {!response && (
          <div className="mt-8 glass-effect rounded-2xl p-8 border border-gray-700">
            <h4 className="font-bold text-xl mb-4 text-gradient">
              How to use Voice Assistant:
            </h4>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="w-16 h-16 bg-royal-green rounded-full flex items-center justify-center mx-auto mb-3">
                  <span className="text-white font-bold text-xl">1</span>
                </div>
                <p className="text-gray-300">Click the microphone button</p>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 bg-leaf-green rounded-full flex items-center justify-center mx-auto mb-3">
                  <span className="text-white font-bold text-xl">2</span>
                </div>
                <p className="text-gray-300">Speak your food details</p>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 bg-pink rounded-full flex items-center justify-center mx-auto mb-3">
                  <span className="text-white font-bold text-xl">3</span>
                </div>
                <p className="text-gray-300">Get instant AI analysis</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
