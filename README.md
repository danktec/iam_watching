# IAM Action Watcher

When it comes to AWS IAM it can be hard to know exactly what permissions are required to run your code. IaC tooling generally makes many different types of AWS API calls which invoke different security actions requiring different permissions which are not always obvious or predictable due to variability in API styles & standards at AWS.

E.g: Invoking a few different high-level functions on a simple program/module will do different things:
- refresh makes 'list/describe/get' calls
- up/apply makes 'create' calls
- down/destroy makes 'destroy/delete/deregister/de-provison' calls

I've found there is no good way to know exactly what these calls will be until all the functions have been tested and this usually means a lot of IAM back-forth debugging to raise or lower access permissions to a reasonable level.

This simple tool monitors in real-time all security actions performed by a user/principal during a time window, which removes the guesswork and toil of testing every function to failure.

## Using It

```bash
poetry install
poetry run python3 -m iam_watching --user [iam_username]
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
- Generate an iam policy json structure
