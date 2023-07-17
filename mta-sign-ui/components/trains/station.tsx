'use client'
import React, {useEffect, useState} from 'react';
import {AllStationModel} from "@/gen-sources/mta-sign-api";
import {mtaDataClient} from "@/services/mta-api/types";
const Station = () => {
    const [data, setData] = useState<AllStationModel | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                console.log("CALLING API")
                const mtaData = await mtaDataClient.getAllApiMtaPost()
                const data = mtaData.data
                setData(data)

            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData();
    }, []);

    return (
        <div className="align-middle lg:flex  w-full">
            <div className="lg:flex-grow"></div>
            <div className="lg:text-right text-center lg:p-2">

                {data ? (
                    <h2 className="text-lg lg:text-xl font-bold dark:text-white">Train Line <span>{data.stations.toString()}</span></h2>

                ) : (
                    <p>Loading data...</p>
                )}

            </div>
        </div>
    );
};

export default Station;