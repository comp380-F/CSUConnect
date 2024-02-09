/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/templates/*.html",
    "./app/static/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        'csun-red': '#D22030',
      }
    },
  },
  plugins: [],
}

