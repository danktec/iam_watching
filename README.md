# IAM Action Watcher

Monitors IAM activities (Actions) for a given user or role in realtime. Outputs a list of actions to help construct a policy document.

"A CLI helper tool which runs alongside your IaC project to determine exactly what permissions your policy will require"

```
> poetry run iam_watching -u testuser

        Watching every 5s for last 50
        operations currently being performed by testuser
        Events can take up to 2 minutes to show up

        Displaying unique actions only

        Hit Ctrl+C to stop watching security events


2025-08-18 15:28:07-07:00 | ec2:DescribeInstances
2025-08-18 15:21:10-07:00 | rds:DescribeDBClusters
2025-08-18 15:21:04-07:00 | iam:GetUser
^C
        The following actions were recently
        performed by testuser:

"Action": [
  "ec2:DescribeInstances",
  "rds:DescribeDBClusters",
  "iam:GetUser"
]
```

## Why?
With AWS IAM it can be hard to know exactly what permissions are required to run your code. IaC tooling makes many different API calls invoking actions requiring specific permissions.

E.g: Running a few different high-level functions on a simple program/module will do different things:
- refresh makes 'list/describe/get' calls
- up/apply makes 'create' calls
- down/destroy makes 'destroy/delete/deregister/de-provision' calls

I've found there is no good way to know exactly what these calls will be until all the functions have been tested and this usually means a lot of back & forth debugging to raise or lower access permissions to a reasonable level. Best-practice for IaC is a policy carrying the exact/minimum security.

This simple CLI tool monitors CloudTrail for all security actions performed by a user/principal during a time window, this removes the guesswork and toil of testing every function to failure.

## Using It

```bash
poetry install
poetry run iam_watching --user [iam_username]|[role_session_name]
```

## Publishing the Package

```bash
# Build & install locally
poetry build
pipx install dist/iam_watching-1.1.0-py3-none-any.whl --force

# Run locally
iam_watching --help
```

## TODO
- Publish to pypy
