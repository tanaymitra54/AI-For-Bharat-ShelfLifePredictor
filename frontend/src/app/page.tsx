'use client'

import { useState } from 'react'
import { Header } from '@/components/Header'
import { NavigationTabs } from '@/components/NavigationTabs'
import { PredictSection } from '@/components/PredictSection'
import { VoiceSection } from '@/components/VoiceSection'
import { ChatSection } from '@/components/ChatSection'

export default function Home() {
  const [activeTab, setActiveTab] = useState<'predict' | 'voice' | 'chat'>('predict')

  return (
    <div className="min-h-screen bg-cream-50 text-gray-800 relative overflow-hidden">
      {/* Background overlay with subtle pattern */}
      <div className="absolute inset-0 bg-royal-green/5 opacity-30"></div>
      <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMzAiIGN5PSIzMCIgcj0iMSIgZmlsbD0iIzAwNjk1QyIgZmlsbC1vcGFjaXR5PSIwLjEiLz4KPC9zdmc+')] opacity-20"></div>
      
      <div className="relative z-10">
        <Header />
        <NavigationTabs activeTab={activeTab} setActiveTab={setActiveTab} />
        
        <main className="container mx-auto px-4 py-8 max-w-6xl">
          {activeTab === 'predict' && <PredictSection />}
          {activeTab === 'voice' && <VoiceSection />}
          {activeTab === 'chat' && <ChatSection />}
        </main>
      </div>
    </div>
  )
}
