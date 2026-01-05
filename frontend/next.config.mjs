/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  async rewrites() {
    // En Docker, el servidor Next.js usa el nombre del servicio 'backend'
    // pero el navegador del cliente usa 'localhost'
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://backend:8001';
    
    return [
      {
        source: '/api/:path*',
        destination: `${apiUrl}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;
