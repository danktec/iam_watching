# IAM Action Watcher

If you write software that runs in the cloud, or deploy IaC of any kind, you know that it's notoriously
difficult to know exactly what permissions are required to run your code.

This tool monitors in real-time all IAM actions performed by a user/principal during a time window.

It provides a looking glass to see the security actions performed by a program, we can then craft a permissions policy to deploy.

It's also useful as an auditing & security review tool.

## Usage

```bash
poetry install
poetry run python3 -m iam_watching --help
```

## Publishing

Increment version numbers

Create a pip wheel & install globally with pipx

Push to PyPi

```bash
# Build & install locally
poetry build
pipx install dist/iam_watching-1.1.0-py3-none-any.whl --force

# Run locally
iam_watching --help
```
