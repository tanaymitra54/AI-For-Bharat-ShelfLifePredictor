'use client'

import { useState } from 'react'

export function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  return (
    <header className="relative z-50 py-6 px-4 lg:px-8">
      <div className="container mx-auto max-w-7xl">
        <div className="flex items-center justify-between">
          {/* Logo and Title */}
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 bg-royal-green rounded-xl flex items-center justify-center shadow-lg glow-green">
              <svg className="w-8 h-8 text-black" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
              </svg>
            </div>
            <div>
              <h1 className="text-3xl lg:text-4xl font-bold text-gradient font-poppins">
                ShelfLife AI
              </h1>
              <p className="text-sm lg:text-base text-gray-600 font-inter">
                AI-powered Food Shelf Life Prediction System
              </p>
            </div>
          </div>

          {/* Mobile menu button */}
          <button
            className="lg:hidden p-2 rounded-lg bg-cream-100/50 border border-royal-green/20"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            <svg className="w-6 h-6 text-gray-800" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>

          {/* Desktop navigation */}
          <nav className="hidden lg:flex items-center space-x-8">
            <button className="btn-primary px-6 py-2">
              Get Started
            </button>
          </nav>
        </div>

        {/* Mobile navigation */}
        {isMenuOpen && (
          <nav className="lg:hidden mt-4 py-4 bg-cream-100/50 rounded-xl border border-royal-green/20">
            <div className="flex flex-col space-y-4 px-4">
              <button className="btn-primary px-6 py-2">
                Get Started
              </button>
            </div>
          </nav>
        )}
      </div>
    </header>
  )
}
