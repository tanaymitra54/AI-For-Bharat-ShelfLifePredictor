'use client'

interface NavigationTabsProps {
  activeTab: 'predict' | 'voice' | 'chat'
  setActiveTab: (tab: 'predict' | 'voice' | 'chat') => void
}

export function NavigationTabs({ activeTab, setActiveTab }: NavigationTabsProps) {
  const tabs = [
    { id: 'predict', label: 'Predict', icon: '🔮' },
    { id: 'voice', label: 'Voice', icon: '🎤' },
    { id: 'chat', label: 'Chat', icon: '💬' }
  ] as const

  return (
    <div className="flex justify-center mb-8">
      <div className="inline-flex bg-cream-100/50 p-2 rounded-2xl border border-royal-green/20 backdrop-blur-sm gap-4">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`
              px-6 py-3 rounded-xl font-semibold transition-all duration-300 transform
              flex items-center space-x-2 min-w-[120px] justify-center
              ${activeTab === tab.id 
                ? 'tab-active shadow-lg scale-105' 
                : 'tab-inactive hover:scale-105'
              }
            `}
          >
            <span className="text-xl">{tab.icon}</span>
            <span>{tab.label}</span>
          </button>
        ))}
      </div>
    </div>
  )
}
