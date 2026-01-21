export interface StationConfig {
    id: string
    stationId: string
    stationName: string
    showNorth: boolean
    showSouth: boolean
    selectedLines: string[]
}

export interface AppConfig {
    version: number
    stations: StationConfig[]
}

export const CONFIG_VERSION = 1
