module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx}',
    './public/**/*.html'
  ],
  theme: {
    extend: {
      colors: {
        'hedera-purple': '#6F2C8D',
        'primary-blue': '#2563eb',
        'secondary-gray': '#4b5563',
        'success-green': '#22c55e',
        'warning-yellow': '#eab308',
        'danger-red': '#ef4444'
      },
      fontFamily: {
        sans: ['Inter var', 'sans-serif'],
        mono: ['Fira Code', 'monospace']
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography')
  ]
}