'use client'

import { useRef } from 'react'
import Image from 'next/image'
import { ArrowDownTrayIcon, ArrowUpTrayIcon } from '@heroicons/react/24/outline'
import { AppConfig } from '@/types/config'

interface HeaderProps {
    startTime: string | null
    lastUpdated: string | null
    onExportConfig: () => AppConfig
    onImportConfig: (config: AppConfig) => void
}

export default function Header({ startTime, lastUpdated, onExportConfig, onImportConfig }: HeaderProps) {
    const fileInputRef = useRef<HTMLInputElement>(null)

    const handleExport = () => {
        const config = onExportConfig()
        const blob = new Blob([JSON.stringify(config, null, 2)], { type: 'application/json' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = 'mta-sign-config.json'
        a.click()
        URL.revokeObjectURL(url)
    }

    const handleImport = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0]
        if (!file) return

        const reader = new FileReader()
        reader.onload = (e) => {
            try {
                const config = JSON.parse(e.target?.result as string) as AppConfig
                onImportConfig(config)
            } catch (err) {
                console.error('Failed to parse config file:', err)
                alert('Invalid config file')
            }
        }
        reader.readAsText(file)

        // Reset input so same file can be imported again
        if (fileInputRef.current) {
            fileInputRef.current.value = ''
        }
    }

    return (
        <nav className="bg-gray-900 w-full px-4 py-3 md:px-6 md:py-4">
            <div className="flex flex-col lg:flex-row items-center justify-between gap-2 lg:gap-4">
                <div className="flex items-center gap-2 md:gap-4">
                    <Image
                        src="/images/RPI-LOGO.png"
                        alt="Raspberry Pi Logo"
                        width={50}
                        height={50}
                        className="w-8 h-8 md:w-10 md:h-10 lg:w-12 lg:h-12"
                    />
                    <h1 className="text-2xl md:text-4xl lg:text-5xl xl:text-6xl font-bold text-white">
                        Pi MTA Display!
                    </h1>
                </div>

                <div className="flex items-center gap-4">
                    <div className="flex gap-2">
                        <button
                            onClick={handleExport}
                            className="p-2 rounded-lg bg-gray-700 hover:bg-gray-600 transition-colors"
                            title="Export config"
                        >
                            <ArrowDownTrayIcon className="w-5 h-5 text-white" />
                        </button>
                        <button
                            onClick={() => fileInputRef.current?.click()}
                            className="p-2 rounded-lg bg-gray-700 hover:bg-gray-600 transition-colors"
                            title="Import config"
                        >
                            <ArrowUpTrayIcon className="w-5 h-5 text-white" />
                        </button>
                        <input
                            ref={fileInputRef}
                            type="file"
                            accept=".json"
                            onChange={handleImport}
                            className="hidden"
                        />
                    </div>

                    <div className="flex flex-col items-center lg:items-end text-sm md:text-base lg:text-lg xl:text-xl">
                        <div className="text-white">
                            <span className="font-semibold">Last Updated:</span>{' '}
                            <span>{lastUpdated || 'Loading...'}</span>
                        </div>
                        <div className="text-white">
                            <span className="font-semibold">Started:</span>{' '}
                            <span>{startTime || 'Loading...'}</span>
                        </div>
                    </div>
                </div>
            </div>
        </nav>
    )
}
