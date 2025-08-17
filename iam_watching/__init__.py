import boto3
import json
import time

__version__ = "1.1.0"
VERBOSE = False
SLEEP_SECONDS = 5
MAX_RESULTS = 15
USER = ""

def main():

    client = boto3.client("cloudtrail")

    uniqueset = set()

    print(f"\nWatching every {SLEEP_SECONDS}s for last {MAX_RESULTS} operations currently being performed by {USER} \n")

    print(f"New events can take up to 2 minutes to show up. Repeated actions are reported only once\n")

    print("Hit Ctrl+C to stop watching security events\n")

    try:
        while True:

            # Filter for a single principal
            response = client.lookup_events(
                LookupAttributes=[
                    {
                        "AttributeKey": "Username",
                        "AttributeValue": f"{USER}"
                    }
                ],
                MaxResults=MAX_RESULTS
            )

            if VERBOSE:
                print(json.dumps(response, indent=2, default=str))

            # Filter out lookups as this script spams them
            for event in response["Events"]:
                if event["EventName"] != "LookupEvents":

                    action = f"{event['EventSource'].split(".")[0]}:{event['EventName']}"

                    if action not in uniqueset:
                        print(action)
                    
                    uniqueset.add(action)

            # Don't exceed the API call limit of 2 per second.
            time.sleep(SLEEP_SECONDS)

    except KeyboardInterrupt:
        print(f"\nThe following IAM actions were recently performed by {USER}:\n")

        print(f"\"Action\": {json.dumps(list(uniqueset), indent=2)}\n")
