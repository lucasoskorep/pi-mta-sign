'use client'
import React, {useState} from 'react';
// import {fetchStartDate} from "@/services/mta-api/mta-server";
import {MtaStartTime} from "@/services/mta-api/types";
// import Image from 'next/image';
import {RouteResponse} from "@/gen-sources/mta-sign-api";

const Line = (props: RouteResponse) => {
    // const [data, setData] = useState<MtaStartTime | null>(null);
    //
    // useEffect(() => {
    //     const fetchData = async () => {
    //         try {
    //             console.log("CALLING API")
    //             const mtaData = await fetchStartDate([""])
    //             setData(mtaData)
    //
    //         } catch (error) {
    //             console.error('Error fetching data:', error);
    //         }
    //     };
    //
    //     fetchData();
    // }, []);

    return (
        <div className="align-middle lg:flex  w-full">
            TRAIN LINE HERE - {props.arrival_times.toJSON().toString()}
        </div>
    );
};

export default Line;