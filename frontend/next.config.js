/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
  compiler: {
    reactRemoveProperties: true,
    removeConsole: {
      exclude: ['error'],
    },
  },
};

module.exports = nextConfig;
