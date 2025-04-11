/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/*.html"],
  safelist: [
    'hidden' 
  ],
  theme: {
    extend: {
      animation: {
        'logo': 'logo_animation 10s ease-in-out infinite alternate'
      },
      keyframes: {
        logo_animation: {
          '0%': {
            fill: 'transparent',
            stroke: '#ffe7a3',
            strokeWidth: '3',
            strokeDashoffset: '25%',
            strokeDasharray: '0 32%'
          },
          '30%': {
            fill: 'transparent',
            stroke: '#ffe7a3',
            strokeWidth: '3'
          },
          '40%, 100%': {
            fill: '#ffe7a3',
            stroke: 'transparent',
            strokeWidth: '0',
            strokeDashoffset: '-25%',
            strokeDasharray: '32% 0'
          }
        }
      }
    },
  },
  plugins: [
      require('daisyui'),
  ],
  daisyui: {
      themes: ["luxury"],
  },
}