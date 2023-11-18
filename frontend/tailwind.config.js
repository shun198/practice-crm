/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './features/**/*.{ts,tsx}',
  ],
  theme: {
    fontSize: {
      h1: '48px',
      h2: '36px',
      h3: '24px',
      normal: '16px',
      tiny: '12px',
    },
    extend: {
      width: {
        styleLabelDefaultWidth: '200px',
        styleLabelDefaultLargeWidth: '250px',
      },
    },
  },
  plugins: [],
};
