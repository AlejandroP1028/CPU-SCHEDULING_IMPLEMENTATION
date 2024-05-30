  // tailwind.config.js
  module.exports = {
    purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
     darkMode: false, // or 'media' or 'class'
     theme: {
       extend: {},
     },
     safelist: [
      {
        pattern: /grow-\[\d+(\.\d+)?\]/
      }
    ],
     variants: {
       extend: {},
     },
     plugins: [],
   }