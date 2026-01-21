/** @type {import('next').NextConfig} */
const nextConfig = {
    output: 'export',
    images: {
        unoptimized: true,
    },
    // Rewrites only work during development (next dev)
    // They are ignored during static export build
    rewrites: async () => {
        return [
            {
                source: '/api/:path*',
                destination: 'http://localhost:8000/api/:path*',
            },
        ]
    },
}

module.exports = nextConfig
