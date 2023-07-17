'use client'

import React, {useEffect, useState} from 'react';
import {fetchStartDate} from "@/services/mta-api/mta-server";
import {MtaStartTime} from "@/services/mta-api/types";
import Image from 'next/image';

const Header = () => {
    const [startDate, setStartDate] = useState<MtaStartTime | null>(null);
    const [lastUpdatedDate, setLastUpdatedDate] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                console.log("CALLING API")
                const mtaData = await fetchStartDate([""])
                setStartDate(mtaData)
                setLastUpdatedDate(new Date().toLocaleString("en-US"))
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData();
    }, []);

    return (
        <div className="align-middle lg:flex  w-full">
            <div className="flex align-middle justify-center lg:justify-normal">
                <div className="align-middle p-0.5">

                    <div style={{width: '100%', aspectRatio: '16/9'}} className="h-5 lg:h-6">
                        <Image src="/images/RPI-LOGO.png" alt="rpi-logo" width="160" height="90" className="w-11"/>
                    </div>
                </div>
                <h1 className="lg:text-left text-center mb-4 text-5xl font-extrabold leading-none tracking-tight text-gray-900 lg:text-6xl dark:text-white ">
                    Pi MTA Display!
                </h1>
            </div>
            <div className="lg:flex-grow"></div>
            <div className="lg:text-right text-center lg:p-2">

                {startDate ? (
                    <h2 className="text-lg lg:text-xl font-bold dark:text-white">Started
                        At: <span>{startDate.startTime.toLocaleString("en-US")}</span></h2>

                ) : (
                    <p>Loading data...</p>
                )}

                <h2 className="text-lg lg:text-xl font-bold dark:text-white">Updated
                    At: <span>{lastUpdatedDate}</span></h2>
            </div>
        </div>
    );
};

export default Header;