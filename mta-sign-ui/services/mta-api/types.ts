import {Configuration, MtaDataApi} from "@/gen-sources/mta-sign-api"

export interface MtaStartTime {
    startTime: Date
}

export const mtaApiConfiguration = new Configuration(
    {basePath:"http://localhost:8000"}
)

export const mtaDataClient = new MtaDataApi(mtaApiConfiguration);
