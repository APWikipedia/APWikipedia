import argparse


def setup_args(parser):
    parser.add_argument(
        "--debug",
        type=bool,
        default=False,
        help="Activate debug mode to enable detailed logging, helping to trace program execution and diagnose issues. Default: False",
    )
    parser.add_argument(
        "--fetch-links", 
        type=bool,
        default=False,
        help="Whether to fetch links or not")
