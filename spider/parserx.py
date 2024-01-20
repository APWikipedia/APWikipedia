import argparse


def setup_args(parser):
    parser.add_argument(
        "--debug",
        type=bool,
        default=False,
        help="Activate debug mode to enable detailed logging, helping to trace program execution and diagnose issues. Default: False",
    )
