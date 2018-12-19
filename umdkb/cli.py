#!/usr/bin/env python3

import argparse
import logging as log


def cli():
    parser = argparse.ArgumentParser(
        description="Command line interface for the University of Maryland "
        "Physics Maker Space's Kibble balance."
    )
    parser.add_argument("--verbose", "-v", action="count")
    subparsers = parser.add_subparsers(title="commands")

    parser_velocity = subparsers.add_parser(
        "velocity",
        help="run the Kibble balance in velocity mode.",
        description="Run the Kibble balance in velocity mode.",
    )
    parser_velocity.add_argument(
        "--plot",
        "-p",
        action="store_true",
        default=False,
        help="show a plot of the velocity vs voltage with the fit line.",
    )
    parser_velocity.add_argument(
        "savefile",
        metavar="DATA_FILE",
        nargs="?",
        type=argparse.FileType("w"),
        help="an optional output file to save the collected data.",
    )
    parser_velocity.set_defaults(function=velocity_mode)

    parser_force = subparsers.add_parser(
        "force",
        help="run the Kibble balance in force mode.",
        description="Run the Kibble balance in force mode.",
    )
    parser_force.add_argument(
        "savefile",
        metavar="DATA_FILE",
        nargs="?",
        type=argparse.FileType("w"),
        help="an optional output file to save the collected data.",
    )
    parser_force.set_defaults(function=force_mode)

    args = parser.parse_args()

    if args.verbose > 0:
        log.basicConfig(level=args.verbose * 10)

    args.function(**vars(args))


def velocity_mode(plot, savefile, **kwargs):
    print("Not yet implemented.")


def force_mode(savefile, **kwargs):
    print("Not yet implemented.")


if __name__ == "__main__":
    cli()
