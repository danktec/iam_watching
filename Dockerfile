FROM python:3.13.7-slim-trixie

RUN python3 -m pip install iam-watching && iam_watching --version

ENTRYPOINT ["iam_watching"]