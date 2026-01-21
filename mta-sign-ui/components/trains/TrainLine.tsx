'use client'

import Image from 'next/image'

interface TrainLineProps {
    routeId: string
    arrivalTimes: number[]
}

const TrainLine = ({ routeId, arrivalTimes }: TrainLineProps) => {
    const formatTimes = (times: number[]): string => {
        if (!times || times.length === 0) {
            return 'No trains'
        }
        return times
            .sort((a, b) => a - b)
            .join(', ')
    }

    const getLineImage = (route: string): string => {
        const cleanRoute = route.replace('Route.', '')
        return `/images/lines/${cleanRoute}.svg`
    }

    return (
        <div className="flex items-center justify-between p-2 md:p-3 lg:p-4 border-b border-gray-700 last:border-b-0 h-16 md:h-20 lg:h-24">
            <div className="flex items-center gap-2 md:gap-3 lg:gap-4 shrink-0">
                <Image
                    src={getLineImage(routeId)}
                    alt={`${routeId} line`}
                    width={60}
                    height={60}
                    className="w-8 h-8 md:w-12 md:h-12 lg:w-14 lg:h-14 xl:w-16 xl:h-16"
                />
            </div>
            <h2 className="text-xl md:text-2xl lg:text-[2.5rem] font-bold text-white text-right flex-1 ml-4 whitespace-nowrap overflow-hidden text-ellipsis">
                {formatTimes(arrivalTimes)}
            </h2>
        </div>
    )
}

export default TrainLine
