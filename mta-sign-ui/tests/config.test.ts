import { describe, it, expect } from 'vitest'
import { AppConfig, StationConfig, CONFIG_VERSION } from '@/types/config'

describe('Config Types', () => {
    it('CONFIG_VERSION is defined', () => {
        expect(CONFIG_VERSION).toBeDefined()
        expect(typeof CONFIG_VERSION).toBe('number')
    })

    it('StationConfig has correct shape', () => {
        const config: StationConfig = {
            stationId: '127',
            stationName: 'Times Sq-42 St',
            showNorth: true,
            showSouth: false,
            selectedLines: ['A', 'C', 'E'],
        }

        expect(config.stationId).toBe('127')
        expect(config.stationName).toBe('Times Sq-42 St')
        expect(config.showNorth).toBe(true)
        expect(config.showSouth).toBe(false)
        expect(config.selectedLines).toEqual(['A', 'C', 'E'])
    })

    it('AppConfig has correct shape', () => {
        const appConfig: AppConfig = {
            version: CONFIG_VERSION,
            stations: [
                {
                    stationId: '127',
                    stationName: 'Times Sq-42 St',
                    showNorth: true,
                    showSouth: true,
                    selectedLines: ['A', 'C', 'E'],
                },
            ],
        }

        expect(appConfig.version).toBe(CONFIG_VERSION)
        expect(appConfig.stations).toHaveLength(1)
        expect(appConfig.stations[0].stationId).toBe('127')
    })

    it('AppConfig can serialize to JSON and back', () => {
        const appConfig: AppConfig = {
            version: CONFIG_VERSION,
            stations: [
                {
                    stationId: '127',
                    stationName: 'Times Sq-42 St',
                    showNorth: true,
                    showSouth: false,
                    selectedLines: ['1', '2', '3'],
                },
                {
                    stationId: 'A27',
                    stationName: '42 St-Port Authority',
                    showNorth: false,
                    showSouth: true,
                    selectedLines: ['A', 'C', 'E'],
                },
            ],
        }

        const json = JSON.stringify(appConfig)
        const parsed = JSON.parse(json) as AppConfig

        expect(parsed.version).toBe(appConfig.version)
        expect(parsed.stations).toHaveLength(2)
        expect(parsed.stations[0]).toEqual(appConfig.stations[0])
        expect(parsed.stations[1]).toEqual(appConfig.stations[1])
    })
})
