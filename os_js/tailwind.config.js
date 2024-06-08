  // tailwind.config.js
  module.exports = {

    purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
 // or 'media' or 'class'
     theme: {
      fontFamily: {
        sans: ['Gabarito']
      },
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
     plugins: [
     ],
   }