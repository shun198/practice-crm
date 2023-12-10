import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
          "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
      },
    },
  },
  plugins: [],
};
// https://asunaroblog.net/blog/641d6dacb5b671fd6673b3c5
// https://tailwindcss.com/docs/preflight#disabling-preflight
// module.exports = {
//   // 省略
//   corePlugins: {
//     preflight: false,
//   },
// }
export default config;
