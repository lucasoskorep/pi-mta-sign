'use client'

import { useState, useEffect, useCallback, useMemo } from 'react'
import { XMarkIcon } from '@heroicons/react/24/outline'
import axios from 'axios'
import StationSelector, { Station } from '../StationSelector'
import DirectionCard from './DirectionCard'
import { StationConfig } from '@/types/config'

interface Route {
    routeId: string
    arrival_times: number[]
}

interface StationData {
    stationId: string
    routes: Route[]
}

interface StationCardProps {
    configId: string
    initialConfig?: StationConfig
    availableLines: string[]
    onConfigChange?: (configId: string, config: StationConfig) => void
    onRemove?: () => void
}

export default function StationCard({ configId, initialConfig, availableLines, onConfigChange, onRemove }: StationCardProps) {
    const [selectedStation, setSelectedStation] = useState<Station | null>(
        initialConfig ? { id: initialConfig.stationId, name: initialConfig.stationName } : null
    )
    const [showNorth, setShowNorth] = useState(initialConfig?.showNorth ?? true)
    const [showSouth, setShowSouth] = useState(initialConfig?.showSouth ?? true)
    const [selectedLines, setSelectedLines] = useState<Set<string>>(
        new Set(initialConfig?.selectedLines ?? availableLines)
    )
    const [northData, setNorthData] = useState<StationData | null>(null)
    const [southData, setSouthData] = useState<StationData | null>(null)

    const notifyConfigChange = useCallback(() => {
        if (onConfigChange && selectedStation) {
            onConfigChange(configId, {
                id: configId,
                stationId: selectedStation.id,
                stationName: selectedStation.name,
                showNorth,
                showSouth,
                selectedLines: Array.from(selectedLines),
            })
        }
    }, [configId, onConfigChange, selectedStation, showNorth, showSouth, selectedLines])

    useEffect(() => {
        notifyConfigChange()
    }, [notifyConfigChange])

    const fetchStationData = useCallback(async () => {
        if (!selectedStation) return

        try {
            if (showNorth) {
                const response = await axios.post(`/api/mta/${selectedStation.id}N`)
                setNorthData(response.data)
            }
            if (showSouth) {
                const response = await axios.post(`/api/mta/${selectedStation.id}S`)
                setSouthData(response.data)
            }
        } catch (err) {
            console.error('Error fetching station data:', err)
        }
    }, [selectedStation, showNorth, showSouth])

    useEffect(() => {
        if (selectedStation) {
            fetchStationData()
            const interval = setInterval(fetchStationData, 5000)
            return () => clearInterval(interval)
        }
    }, [selectedStation, fetchStationData])

    const availableDirections = useMemo(() => {
        const directions = new Set<string>()
        if (northData && northData.routes.length > 0) directions.add('North')
        if (southData && southData.routes.length > 0) directions.add('South')
        return directions
    }, [northData, southData])

    const stationAvailableLines = useMemo(() => {
        const lines = new Set<string>()
        if (northData) {
            northData.routes.forEach(route => {
                const lineId = route.routeId.replace('Route.', '')
                lines.add(lineId)
            })
        }
        if (southData) {
            southData.routes.forEach(route => {
                const lineId = route.routeId.replace('Route.', '')
                lines.add(lineId)
            })
        }
        return Array.from(lines).sort()
    }, [northData, southData])

    const toggleLine = (line: string) => {
        const newSelected = new Set(selectedLines)
        if (newSelected.has(line)) {
            newSelected.delete(line)
        } else {
            newSelected.add(line)
        }
        setSelectedLines(newSelected)
    }

    const toggleDirection = (direction: 'North' | 'South') => {
        if (direction === 'North') {
            setShowNorth(!showNorth)
        } else {
            setShowSouth(!showSouth)
        }
    }

    const filterRoutes = (routes: Route[]): Route[] => {
        return routes.filter(route => {
            const lineId = route.routeId.replace('Route.', '')
            return selectedLines.has(lineId)
        })
    }

    return (
        <div className="bg-gray-800 overflow-hidden">
            <Header
                selectedStation={selectedStation}
                onSelectStation={setSelectedStation}
                showNorth={showNorth}
                showSouth={showSouth}
                selectedLines={selectedLines}
                availableDirections={availableDirections}
                availableLines={stationAvailableLines}
                onToggleDirection={toggleDirection}
                onToggleLine={toggleLine}
                onRemove={onRemove}
            />

            <Content
                selectedStation={selectedStation}
                showNorth={showNorth}
                showSouth={showSouth}
                northRoutes={northData ? filterRoutes(northData.routes || []) : []}
                southRoutes={southData ? filterRoutes(southData.routes || []) : []}
            />
        </div>
    )
}

interface HeaderProps {
    selectedStation: Station | null
    onSelectStation: (station: Station) => void
    showNorth: boolean
    showSouth: boolean
    selectedLines: Set<string>
    availableDirections: Set<string>
    availableLines: string[]
    onToggleDirection: (direction: 'North' | 'South') => void
    onToggleLine: (line: string) => void
    onRemove?: () => void
}

function Header({
    selectedStation,
    onSelectStation,
    showNorth,
    showSouth,
    selectedLines,
    availableDirections,
    availableLines,
    onToggleDirection,
    onToggleLine,
    onRemove,
}: HeaderProps) {
    return (
        <div className="bg-gray-700 px-3 py-2 md:px-4 md:py-3 flex items-center gap-2 md:gap-4">
            <div className="flex-1">
                <StationSelector selectedStation={selectedStation} onSelect={onSelectStation} />
            </div>

            <div className="flex items-center gap-2 md:gap-3 shrink-0">
                {availableDirections.has('North') && (
                    <label className="flex items-center gap-1 cursor-pointer">
                        <input
                            type="checkbox"
                            checked={showNorth}
                            onChange={() => onToggleDirection('North')}
                            className="w-4 h-4 rounded"
                        />
                        <span className="text-white text-xs md:text-sm">N</span>
                    </label>
                )}

                {availableDirections.has('South') && (
                    <label className="flex items-center gap-1 cursor-pointer">
                        <input
                            type="checkbox"
                            checked={showSouth}
                            onChange={() => onToggleDirection('South')}
                            className="w-4 h-4 rounded"
                        />
                        <span className="text-white text-xs md:text-sm">S</span>
                    </label>
                )}

                <div className="flex gap-1 md:gap-2">
                    {availableLines.map(line => (
                        <button
                            key={line}
                            onClick={() => onToggleLine(line)}
                            className={`w-6 h-6 md:w-7 md:h-7 rounded-full text-xs font-bold transition-all ${
                                selectedLines.has(line) ? 'bg-blue-600 text-white' : 'bg-gray-600 text-gray-400'
                            }`}
                        >
                            {line}
                        </button>
                    ))}
                </div>

                {onRemove && (
                    <button
                        onClick={onRemove}
                        className="p-2 rounded-lg bg-red-600 hover:bg-red-500 transition-colors shrink-0"
                        title="Remove station"
                    >
                        <XMarkIcon className="w-4 h-4 md:w-5 md:h-5 text-white" />
                    </button>
                )}
            </div>
        </div>
    )
}

interface ContentProps {
    selectedStation: Station | null
    showNorth: boolean
    showSouth: boolean
    northRoutes: Route[]
    southRoutes: Route[]
}

function Content({ selectedStation, showNorth, showSouth, northRoutes, southRoutes }: ContentProps) {
    if (!selectedStation) {
        return (
            <div className="p-8 text-center text-gray-400">
                Select a station to view train arrivals
            </div>
        )
    }

    return (
        <div className="flex flex-col md:flex-row">
            {showNorth && (
                <div className={`flex-1 ${showSouth ? 'border-b md:border-b-0 md:border-r border-gray-700' : ''}`}>
                    <DirectionCard direction="North" routes={northRoutes} />
                </div>
            )}
            {showSouth && (
                <div className="flex-1">
                    <DirectionCard direction="South" routes={southRoutes} />
                </div>
            )}
        </div>
    )
}
