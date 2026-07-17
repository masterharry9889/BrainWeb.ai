import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',
  distDir: 'out',
  assetPrefix: './',
  trailingSlash: true,
};

export default nextConfig;
