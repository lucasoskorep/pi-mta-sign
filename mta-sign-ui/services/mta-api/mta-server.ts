import { MtaStartTime} from "@/services/mta-api/types";

export const fetchStartDate = async (stations: [string]): Promise<MtaStartTime> => {
    const res = await fetch("/api/start_time", {method: "POST"})
    const data = await res.text()
    const date = new Date(data.replaceAll("\"", ""))
    return {
        startTime: date
    };
};