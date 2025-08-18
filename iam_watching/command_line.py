import argparse
import iam_watching


def main(assigned_args: list = None) -> None:
    """
    Parse and execute the call from command-line.

    Args:
        assigned_args: List of strings to parse.
        The default is taken from sys.argv.

    Returns:
        .
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="iam_watching",
        description="Monitors IAM Actions to construct permissions policies"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=iam_watching.__version__
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Verbose output, displays ALL events"
    )
    parser.add_argument(
        "-u",
        "--user",
        action="store",
        type=str,
        required=True,
        help="The IAM User or Role name to filter"
    )
    parser.add_argument(
        "-m",
        "--maxresults",
        action="store",
        type=int,
        default=50,
        help="How far to look back on each query"
    )

    args = parser.parse_args(assigned_args)

    iam_watching.USER = args.user
    iam_watching.VERBOSE = args.verbose
    iam_watching.MAX_RESULTS = args.maxresults

    iam_watching.main()


if __name__ == "__main__":
    main()
