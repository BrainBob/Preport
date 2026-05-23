/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{vue,js,ts}"],
  theme: {
    extend: {
      colors: {
        critical: "#FF0000",
        high: "#FF6B00",
        medium: "#FFD700",
        low: "#00C853",
        info: "#2196F3",
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
