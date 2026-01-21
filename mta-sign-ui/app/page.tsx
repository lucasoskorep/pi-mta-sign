'use client'

import { useState, useEffect, useCallback } from 'react'
import { PlusIcon } from '@heroicons/react/24/outline'
import Header from '@/components/Header'
import StationCard from '@/components/trains/StationCard'
import { AppConfig, StationConfig, CONFIG_VERSION } from '@/types/config'
import axios from 'axios'

const generateId = () => Math.random().toString(36).substring(2, 11)

const DEFAULT_CONFIGS: StationConfig[] = [
    { id: generateId(), stationId: '127', stationName: 'Times Sq-42 St', showNorth: true, showSouth: true, selectedLines: [] },
    { id: generateId(), stationId: 'A27', stationName: 'Times Sq-42 St', showNorth: true, showSouth: true, selectedLines: [] },
]

const STORAGE_KEY = 'mta-sign-config'

export default function Home() {
    const [stationConfigs, setStationConfigs] = useState<StationConfig[]>(DEFAULT_CONFIGS)
    const [availableLines, setAvailableLines] = useState<string[]>([])
    const [startTime, setStartTime] = useState<string | null>(null)
    const [lastUpdated, setLastUpdated] = useState<string | null>(null)
    const [isLoaded, setIsLoaded] = useState(false)

    // Load config from localStorage on mount
    useEffect(() => {
        if (typeof window === 'undefined') return
        try {
            const saved = localStorage.getItem(STORAGE_KEY)
            if (saved) {
                const config = JSON.parse(saved)
                if (config.stations && Array.isArray(config.stations)) {
                    // Ensure all stations have IDs
                    const stationsWithIds = config.stations.map((s: any) => ({
                        ...s,
                        id: s.id || generateId(),
                    }))
                    setStationConfigs(stationsWithIds)
                }
            }
        } catch (err) {
            console.error('Error loading config from localStorage:', err)
        }
        setIsLoaded(true)
    }, [])

    useEffect(() => {
        axios.get('/api/lines')
            .then(response => {
                const lines = response.data.lines || []
                setAvailableLines(lines)
                // Update default configs to include all lines
                setStationConfigs(prev => prev.map(config => ({
                    ...config,
                    selectedLines: config.selectedLines.length === 0 ? lines : config.selectedLines
                })))
            })
            .catch(err => console.error('Error fetching lines:', err))
    }, [])

    useEffect(() => {
        axios.post('/api/start_time')
            .then(response => {
                if (response.data) {
                    setStartTime(new Date(response.data).toLocaleString('en-US'))
                }
            })
            .catch(err => console.error('Error fetching start time:', err))
    }, [])

    useEffect(() => {
        const interval = setInterval(() => {
            setLastUpdated(new Date().toLocaleString('en-US'))
        }, 5000)
        return () => clearInterval(interval)
    }, [])

    // Save config to localStorage whenever it changes
    useEffect(() => {
        if (typeof window === 'undefined') return
        try {
            const configToSave = {
                version: CONFIG_VERSION,
                stations: stationConfigs,
            }
            localStorage.setItem(STORAGE_KEY, JSON.stringify(configToSave))
        } catch (err) {
            console.error('Error saving config to localStorage:', err)
        }
    }, [stationConfigs])

    const handleConfigChange = useCallback((configId: string, newConfig: StationConfig) => {
        setStationConfigs(prevConfigs => {
            const updated = prevConfigs.map(config => config.id === configId ? newConfig : config)
            return updated
        })
    }, [])

    const addStation = () => {
        const newConfig: StationConfig = {
            id: generateId(),
            stationId: '',
            stationName: '',
            showNorth: true,
            showSouth: true,
            selectedLines: availableLines,
        }
        setStationConfigs([...stationConfigs, newConfig])
    }

    const removeStation = (configId: string) => {
        setStationConfigs(stationConfigs.filter(config => config.id !== configId))
    }

    const exportConfig = useCallback((): AppConfig => {
        return {
            version: CONFIG_VERSION,
            stations: stationConfigs,
        }
    }, [stationConfigs])

    const importConfig = useCallback((config: AppConfig) => {
        if (config.version !== CONFIG_VERSION) {
            alert(`Config version mismatch. Expected ${CONFIG_VERSION}, got ${config.version}`)
            return
        }
        // Ensure all stations have IDs
        const stationsWithIds = config.stations.map(station => ({
            ...station,
            id: station.id || generateId(),
        }))
        setStationConfigs(stationsWithIds)
    }, [])

    if (availableLines.length === 0) {
        return (
            <main className="min-h-screen bg-gray-900 flex items-center justify-center">
                <div className="text-white text-xl">Loading...</div>
            </main>
        )
    }

    return (
        <main className="min-h-screen bg-gray-900 flex flex-col">
            <Header
                startTime={startTime}
                lastUpdated={lastUpdated}
                onExportConfig={exportConfig}
                onImportConfig={importConfig}
            />

            <div className="flex-1 p-2 md:p-4 space-y-4 md:space-y-6">
                {stationConfigs.map((config) => (
                    <StationCard
                        key={config.id}
                        configId={config.id}
                        initialConfig={config.stationId ? config : undefined}
                        availableLines={availableLines}
                        onConfigChange={handleConfigChange}
                        onRemove={() => removeStation(config.id)}
                    />
                ))}

                <button
                    onClick={addStation}
                    className="w-full p-4 border-2 border-dashed border-gray-600 rounded-lg text-gray-400 hover:border-gray-500 hover:text-gray-300 transition-colors flex items-center justify-center gap-2"
                >
                    <PlusIcon className="w-5 h-5" />
                    Add Station
                </button>
            </div>
        </main>
    )
}
