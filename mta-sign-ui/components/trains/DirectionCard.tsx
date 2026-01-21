'use client'

import TrainLine from './TrainLine'

interface Route {
    routeId: string
    arrival_times: number[]
}

interface DirectionCardProps {
    direction: 'North' | 'South'
    routes: Route[]
}

const DirectionCard = ({ direction, routes }: DirectionCardProps) => {
    return (
        <div className="bg-gray-800 overflow-hidden flex-1">
            <div className="bg-gray-700 px-3 py-2 md:px-4 md:py-3 lg:px-6 lg:py-4">
                <h2 className="text-xl md:text-2xl lg:text-3xl xl:text-4xl font-bold text-white">
                    {direction}
                </h2>
            </div>
            <div className="divide-y divide-gray-700">
                {routes && routes.length > 0 ? (
                    routes.map((route, index) => (
                        <TrainLine
                            key={`${route.routeId}-${index}`}
                            routeId={route.routeId}
                            arrivalTimes={route.arrival_times}
                        />
                    ))
                ) : (
                    <div className="p-4 text-gray-400 text-center">
                        No trains available
                    </div>
                )}
            </div>
        </div>
    )
}

export default DirectionCard
