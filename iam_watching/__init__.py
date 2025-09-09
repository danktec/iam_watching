import boto3
import botocore
import json
import time
import re
import os
import botocore.exceptions
from datetime import datetime, timedelta, timezone

__version__ = "1.6.0"
VERBOSE = False
SLEEP_SECONDS = 5
MAX_RESULTS = 100
USER = ""
LOG_MODE = False
DEV_MODE = True

def main() -> None:

    global USER
    uniqueset: set = set()

    now = datetime.now(timezone.utc)
    now_formatted = now.strftime("%a, %d %b %Y %H:%M:%S GMT")

    try:
        sts: botocore.client.STS = boto3.client("sts")
        identity: dict = sts.get_caller_identity()
        client: botocore.client.CloudTrail = boto3.client("cloudtrail")

        auth_type: dict = identity["Arn"].split(":")[2]

        if USER == "":
            if auth_type == "sts":
                USER = identity["Arn"].split("/")[2]
                print(f"""
        Using sts identity: {identity["Arn"]}""")
            if auth_type == "iam":
                USER = identity["Arn"].split("/")[1]
                print(f"""
        Using iam identity: {identity["Arn"]}""")

    except botocore.exceptions.NoCredentialsError:
        print("No AWS credentials found.")
    except botocore.exceptions.PartialCredentialsError:
        print("Incomplete AWS credentials.")
    except botocore.exceptions.ClientError as e:
        print(f"Authentication failed: {e}")

    print(f"""
        Watching for security actions being performed by {USER}
        Events can take up to 2 minutes to show up""")

    print(f"""
        Displaying unique actions only from:
        {now_formatted}""")

    print("""
        Hit Ctrl+C to stop watching security events
    """)

    try:
        while True:

            # Filter for a single principal
            response: boto3.client.lookup_events = client.lookup_events(
                LookupAttributes=[
                    {
                        "AttributeKey": "Username",
                        "AttributeValue": f"{USER}"
                    }
                ],
                MaxResults=MAX_RESULTS,
                StartTime=now_formatted,
                EndTime=now + timedelta(days=1),
            )

            if VERBOSE:
                print(
                    json.dumps(response, indent=2, default=str)
                )

            # Filter out lookups as this script spams them
            for event in response["Events"]:
                if event["EventName"] != "LookupEvents":

                    event_source: str = event['EventSource'].split(".")[0]

                    # Strip out API versions which lead to inconsistencies
                    # e.g 'lambda:CreateFunction (event name: CreateFunction20150331)'
                    event_name = re.split(r"(\d+)", event["EventName"])[0]

                    action: str = f"{event_source}:{event_name}"

                    # In log mode we show the event and time seen by CW
                    if LOG_MODE:
                        if action not in uniqueset:
                            print(f"{event["EventTime"]} | {action}")

                    uniqueset.add(action)

            # In dev mode we continually refresh a policy json document
            if DEV_MODE:
                os.system('clear')
                print(
                    json.dumps(
                    {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Effect": "Allow",
                                "Action": list(uniqueset),
                                "Resource": "*"
                            }
                        ]
                    },
                    sort_keys=False,
                    indent=4,
                    separators=(',', ': ')
                    )
                )

            # Don't exceed the API call limit of 2 per second.
            time.sleep(SLEEP_SECONDS)

    except KeyboardInterrupt:
        print(f"""
        Policy document for actions seen by {USER}:
        """)

        # Print an iam policy
        print(
            json.dumps(
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": list(uniqueset),
                        "Resource": "*"
                    }
                ]
            },
            sort_keys=False,
            indent=4,
            separators=(',', ': ')
            )
        )

