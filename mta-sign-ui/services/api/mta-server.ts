export type MtaData = {
    mtaData: any;
};

export const fetchStationData = async (stations:[string]):Promise<MtaData> =>  {
    const res = await fetch("")
    const data = await res.json()
    return {
        mtaData: data
    };
};