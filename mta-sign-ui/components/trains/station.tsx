'use client'
import React, {useEffect, useState} from 'react';
import {fetchStationData} from "@/services/mta-api/mta-server";
import {MtaData,} from "@/services/mta-api/types";

const Station = () => {
    const [data, setData] = useState<MtaData | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                console.log("CALLING API")
                const mtaData = await fetchStationData([""])
                setData(mtaData)

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
                    <h2 className="text-lg lg:text-xl font-bold dark:text-white">Train Line <span>{data.mtaData.toLocaleString()}</span></h2>

                ) : (
                    <p>Loading data...</p>
                )}

                <h2 className="text-lg lg:text-xl font-bold dark:text-white">Updated
                    At: <span>{new Date().toLocaleString("en-US")}</span></h2>
            </div>
        </div>
    );
};

export default Station;