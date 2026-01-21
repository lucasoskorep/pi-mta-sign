import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Pi MTA Sign!',
  description: 'Using a raspberry pi to display subway information!',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
