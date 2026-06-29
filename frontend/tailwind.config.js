/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          orange: "#D2691E",
          brick: "#8B1A1A",
          cream: "#FFF8F0",
          "orange-light": "#E8954A",
          "brick-light": "#A52A2A",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        display: ["Georgia", "serif"],
      },
      boxShadow: {
        card: "0 4px 20px rgba(139, 26, 26, 0.08)",
        elevated: "0 8px 30px rgba(139, 26, 26, 0.12)",
      },
    },
  },
  plugins: [],
};
