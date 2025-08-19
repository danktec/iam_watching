import boto3
import json
import time

__version__ = "1.2.0"
VERBOSE = False
SLEEP_SECONDS = 5
MAX_RESULTS = 50
USER = ""


def main() -> None:

    client: boto3.client = boto3.client("cloudtrail")

    uniqueset: set = set()

    print(f"""
        Querying every {SLEEP_SECONDS}s for last {MAX_RESULTS} operations
        currently being performed by {USER}
        Events can take up to 2 minutes to show up
    """)

    print("""
        Displaying unique actions only
    """)

    print("""
        Hit Ctrl+C to stop watching security events
    """)

    try:
        while True:

            # Filter for a single principal
            response: boto3.client.lookup_event = client.lookup_events(
                LookupAttributes=[
                    {
                        "AttributeKey": "Username",
                        "AttributeValue": f"{USER}"
                    }
                ],
                MaxResults=MAX_RESULTS
            )

            if VERBOSE:
                print(
                    json.dumps(response, indent=2, default=str)
                )

            # Filter out lookups as this script spams them
            for event in response["Events"]:
                if event["EventName"] != "LookupEvents":

                    event_source: str = event['EventSource'].split(".")[0]

                    action: str = f"{event_source}:{event['EventName']}"

                    if action not in uniqueset:
                        print(f"{event["EventTime"]} | {action}")

                    uniqueset.add(action)

            # Don't exceed the API call limit of 2 per second.
            time.sleep(SLEEP_SECONDS)

    except KeyboardInterrupt:
        print(f"""
        The following actions were recently
        performed by {USER}:
        """)

        print(f"""
\"Action\": {json.dumps(list(uniqueset), indent=2)}
        """)
