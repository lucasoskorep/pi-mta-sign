'use client'
import React, {useEffect, useState} from 'react';
import {fetchStationData} from "@/services/api/mta-server";


const TitleBar = () => {
    const [data, setData] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                console.log("CALLING API")
                const mtaData = await fetchStationData([""])
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