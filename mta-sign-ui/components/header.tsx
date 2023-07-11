'use client'
import React, {useEffect, useState} from 'react';
import {fetchStartDate} from "@/services/mta-api/mta-server";
import {MtaStartTime} from "@/services/mta-api/types";


const TitleBar = () => {
    const [data, setData] = useState<MtaStartTime|null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                console.log("CALLING API")
                const mtaData = await fetchStartDate([""])
                setData( mtaData)

            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData();
    }, []);

    return (
        <div>
            {data ? (
                <pre>{JSON.stringify(data, null, 2)}</pre>
            ) : (
                <p>Loading data...</p>
            )}
        </div>
    );
};

export default TitleBar;