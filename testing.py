import requests
import os
import json

from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

#endpoint definitions - should be loaded form the env if possible, woudl make it easily maintaine from docker
ACE_ENDPOINT = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace"
SUBWAY_ALERTS = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts"
SUBWAY_ALERTS_JSON = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-status.json"


def create_api_call_header(api_key):
    return {
        "x-api-key":api_key
    }


def test_api_calls():
    print("Testing the api")
    api_key = os.getenv('MTA_API_KEY', '')
    r = requests.get(
        SUBWAY_ALERTS_JSON,
        headers=create_api_call_header(api_key)
    )
    print(r)
    print(r.status_code)
    pprint(r.json())
    with open("mta_status_alerts.json", "w+") as f:
        f.write(json.dumps(r.json()))



    r = requests.get(
        ACE_ENDPOINT,
        headers=create_api_call_header(api_key)
    )
    print(r)
    print(r.status_code)
    print(r.content)

    # alerts_data = json.loads()


if __name__ == '__main__':
    test_api_calls()
