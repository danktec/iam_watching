import boto3
import json
import time

__version__ = "1.1.0"
VERBOSE = False
SLEEP_SECONDS = 5
MAX_RESULTS = 10

def main():

    client = boto3.client("cloudtrail")

    uniqueset = set()

    filter_user = input("\nEnter the IAM username to filter events for: ")

    print(f"\nWatching every {SLEEP_SECONDS}s for last {MAX_RESULTS} operations currently being performed by {filter_user} \n")

    print(f"Events can take between 1 to 2 mins to show up. Repeated actions are registered only once\n")

    print("Hit Ctrl+C to stop watching security events\n")

    try:
        while True:

            # Filter for a single principal
            response = client.lookup_events(
                LookupAttributes=[
                    {
                        "AttributeKey": "Username",
                        "AttributeValue": f"{filter_user}"
                    }
                ],
                MaxResults=MAX_RESULTS
            )

            if VERBOSE:
                print(json.dumps(response, indent=2, default=str))

            # Filter out lookups as this script spams them
            for event in response["Events"]:
                if event["EventName"] != "LookupEvents":

                    if event["EventName"] not in uniqueset:
                        print(f"{event['EventSource'].split(".")[0]}:{event['EventName']}")
                    
                    uniqueset.add(event["EventName"])

            # Don't exceed the API call limit of 2 per second.
            time.sleep(SLEEP_SECONDS)

    except KeyboardInterrupt:
        print(f"\nThe following IAM operations were recently performed by {filter_user}:\n")
        print(f"{', '.join(uniqueset)}\n")
        print("You can use this list to construct an IAM policy for your project with minimum required privileges :)")
