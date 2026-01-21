'use client'

import { useState, useEffect, useRef } from 'react'
import { ChevronDownIcon } from '@heroicons/react/24/outline'
import axios from 'axios'

export interface Station {
    id: string
    name: string
}

interface StationSelectorProps {
    selectedStation: Station | null
    onSelect: (station: Station) => void
}

export default function StationSelector({ selectedStation, onSelect }: StationSelectorProps) {
    const [search, setSearch] = useState('')
    const [stations, setStations] = useState<Station[]>([])
    const [isOpen, setIsOpen] = useState(false)
    const [loading, setLoading] = useState(false)
    const dropdownRef = useRef<HTMLDivElement>(null)

    useEffect(() => {
        const fetchStations = async () => {
            setLoading(true)
            try {
                const params = search ? { search } : {}
                const response = await axios.get('/api/stations', { params })
                setStations(response.data.stations || [])
            } catch (err) {
                console.error('Error fetching stations:', err)
            } finally {
                setLoading(false)
            }
        }

        const debounce = setTimeout(fetchStations, 300)
        return () => clearTimeout(debounce)
    }, [search])

    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                setIsOpen(false)
            }
        }

        document.addEventListener('mousedown', handleClickOutside)
        return () => document.removeEventListener('mousedown', handleClickOutside)
    }, [])

    const handleSelect = (station: Station) => {
        onSelect(station)
        setSearch('')
        setIsOpen(false)
    }

    return (
        <div ref={dropdownRef} className="relative w-full">
            <div
                className="flex items-center gap-2 bg-gray-700 px-3 py-2 cursor-pointer"
                onClick={() => setIsOpen(!isOpen)}
            >
                <input
                    type="text"
                    placeholder={selectedStation?.name || 'Search stations...'}
                    value={search}
                    onChange={(e) => {
                        setSearch(e.target.value)
                        setIsOpen(true)
                    }}
                    onClick={(e) => {
                        e.stopPropagation()
                        setIsOpen(true)
                    }}
                    className="flex-1 bg-transparent text-white placeholder-gray-400 outline-none text-sm md:text-base lg:text-lg"
                />
                <ChevronDownIcon
                    className={`w-4 h-4 text-gray-400 transition-transform ${isOpen ? 'rotate-180' : ''}`}
                />
            </div>

            {isOpen && (
                <div className="absolute z-50 w-full mt-1 bg-gray-800 border border-gray-600 rounded-lg shadow-lg max-h-60 overflow-y-auto">
                    {loading ? (
                        <div className="p-3 text-gray-400 text-center">Loading...</div>
                    ) : stations.length === 0 ? (
                        <div className="p-3 text-gray-400 text-center">No stations found</div>
                    ) : (
                        stations.map((station) => (
                            <div
                                key={station.id}
                                onClick={() => handleSelect(station)}
                                className={`px-3 py-2 cursor-pointer hover:bg-gray-700 transition-colors ${
                                    selectedStation?.id === station.id ? 'bg-gray-700' : ''
                                }`}
                            >
                                <span className="text-white text-sm md:text-base">{station.name}</span>
                                <span className="text-gray-500 text-xs ml-2">({station.id})</span>
                            </div>
                        ))
                    )}
                </div>
            )}
        </div>
    )
}
