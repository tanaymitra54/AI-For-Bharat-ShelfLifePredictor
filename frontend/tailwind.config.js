/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'cream': '#FFF8E7',
        'cream-50': '#FFFEF7',
        'cream-100': '#FFF8E7',
        'cream-200': '#FEF3C7',
        'royal-green': '#00695C',
        'leaf-green': '#4CAF50',
        'fresh-leaf-green': '#66BB6A',
        'light-green': '#86EFAC',
        'dark-green': '#166534',
        'pink': '#E91E63',
        'light-pink': '#F8BBD0',
        'pink-50': '#FCE4EC',
        'pink-100': '#F8BBD0',
        'green': '#10B981',
        'green-50': '#ECFDF5',
        'green-100': '#D1FAE5',
        'green-200': '#A7F3D0',
        'green-600': '#059669',
        'green-700': '#047857',
        'green-800': '#065F46',
      },
      fontFamily: {
        'poppins': ['Poppins', 'sans-serif'],
        'montserrat': ['Montserrat', 'sans-serif'],
        'inter': ['Inter', 'sans-serif'],
        'playfair': ['Playfair Display', 'serif'],
      },
      animation: {
        'fadeIn': 'fadeIn 0.6s ease-out',
        'slideIn': 'slideIn 0.5s ease-out',
        'pulse': 'pulse 2s infinite',
        'glow': 'glow 2s infinite',
        'soundWave': 'soundWave 0.5s ease-in-out infinite',
        'typing': 'typing 2s steps(40, end)',
      },
      keyframes: {
        fadeIn: {
          'from': { opacity: '0', transform: 'translateY(20px)' },
          'to': { opacity: '1', transform: 'translateY(0)' }
        },
        slideIn: {
          'from': { opacity: '0', transform: 'translateX(-20px)' },
          'to': { opacity: '1', transform: 'translateX(0)' }
        },
        pulse: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.7' }
        },
        glow: {
          '0%, 100%': { boxShadow: '0 0 20px rgba(74, 222, 128, 0.3)' },
          '50%': { boxShadow: '0 0 30px rgba(74, 222, 128, 0.6)' }
        },
        soundWave: {
          '0%, 100%': { transform: 'scaleY(1)' },
          '50%': { transform: 'scaleY(1.5)' }
        },
        typing: {
          'from': { width: '0' },
          'to': { width: '100%' }
        }
      }
    },
  },
  plugins: [],
}
