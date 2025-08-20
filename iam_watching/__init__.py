import boto3
import botocore
import json
import time
import botocore.client
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

__version__ = "1.4.0"
VERBOSE = False
SLEEP_SECONDS = 5
MAX_RESULTS = 50
USER = ""


def main() -> None:

    global USER
    uniqueset: set = set()

    try:
        sts: botocore.client.STS = boto3.client("sts")
        identity: dict = sts.get_caller_identity()
        client: botocore.client.CloudTrail = boto3.client("cloudtrail")

        auth_type: dict = identity["Arn"].split(":")[2]

        if USER == "":
            print("No user specified")
            if auth_type == "sts":
                USER = identity["Arn"].split("/")[2]
                print(f"Using sts identity: {identity["Arn"]}")
            if auth_type == "iam":
                USER = identity["Arn"].split("/")[1]
                print(f"Using iam identity: {identity["Arn"]}")

    except NoCredentialsError:
        print("No AWS credentials found.")
    except PartialCredentialsError:
        print("Incomplete AWS credentials.")
    except ClientError as e:
        print(f"Authentication failed: {e}")

    print(f"""
        Querying every {SLEEP_SECONDS}s for last {MAX_RESULTS} operations
        currently being performed by {USER}
        Events can take up to 2 minutes to show up""")

    print("""
        Displaying unique actions only""")

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
