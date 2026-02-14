'use client'

import { useState, useRef, useEffect } from 'react'

interface ChatMessage {
  id: string
  text: string
  sender: 'user' | 'bot'
  timestamp: Date
}

export function ChatSection() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      text: 'Hello! I\'m your AI food storage assistant. Ask me anything about food shelf life, storage tips, or safety guidelines!',
      sender: 'bot',
      timestamp: new Date()
    }
  ])
  const [inputText, setInputText] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async () => {
    if (!inputText.trim()) return

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      text: inputText,
      sender: 'user',
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputText('')
    setIsTyping(true)

    // Simulate bot response
    setTimeout(() => {
      const botResponses = [
        'Based on your question, I recommend storing dairy products at temperatures below 4°C to maintain freshness for up to 5-7 days.',
        'For optimal shelf life, keep fruits in the refrigerator crisper drawer and check them daily for signs of spoilage.',
        'When storing meat, always use airtight containers and consume within 2-3 days for best quality and safety.',
        'Vegetables stay fresh longer when stored with proper humidity levels - around 90-95% for most leafy greens.',
        'Bakery items should be stored in a cool, dry place. Refrigeration can actually speed up staling for most bread products.',
        'Seafood is highly perishable and should be consumed within 1-2 days of purchase. Keep it well-chilled at all times.'
      ]

      const botMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        text: botResponses[Math.floor(Math.random() * botResponses.length)],
        sender: 'bot',
        timestamp: new Date()
      }

      setMessages(prev => [...prev, botMessage])
      setIsTyping(false)
    }, 1500)
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="animate-fadeIn h-[600px] flex flex-col">
      {/* Chat Messages Area */}
      <div className="flex-1 glass-effect rounded-2xl border border-gray-700 p-6 mb-4 overflow-hidden flex flex-col">
        <h3 className="text-xl font-bold mb-4 text-gradient font-poppins">
          💬 AI Food Assistant
        </h3>
        
        <div className="flex-1 overflow-y-auto space-y-4 pr-2">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'} animate-slideIn`}
            >
              <div className={`max-w-xs lg:max-w-md ${message.sender === 'user' ? 'chat-bubble-user' : 'chat-bubble-bot'}`}>
                <p className="text-sm">{message.text}</p>
                <p className="text-xs opacity-70 mt-1">
                  {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </p>
              </div>
            </div>
          ))}
          
          {isTyping && (
            <div className="flex justify-start animate-slideIn">
              <div className="chat-bubble-bot">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Chat Input */}
      <div className="glass-effect rounded-2xl border border-gray-700 p-4">
        <div className="flex space-x-3">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask about food storage or shelf life..."
            className="flex-1 input-field px-4 py-3"
            disabled={isTyping}
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputText.trim() || isTyping}
            className="btn-primary px-6 py-3 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
            <span>Send</span>
          </button>
        </div>
        
        {/* Quick Suggestions */}
        <div className="mt-3 flex flex-wrap gap-2">
          {[
            'How long does milk last?',
            'Best way to store vegetables?',
            'Meat safety guidelines',
            'Fruit storage tips'
          ].map((suggestion) => (
            <button
              key={suggestion}
              onClick={() => setInputText(suggestion)}
              className="text-xs px-3 py-1 bg-gray-800/50 border border-gray-700 rounded-full text-gray-400 hover:border-fresh-leaf-green hover:text-fresh-leaf-green transition-all duration-300"
            >
              {suggestion}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
