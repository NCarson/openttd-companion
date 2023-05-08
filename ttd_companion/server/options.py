import sys
import argparse
import shlex
from pathlib import Path
from os.path import expanduser

import version


def parse():
    parser = argparse.ArgumentParser(
        usage=f'{sys.argv[0]} [OPTION, ...] "openttd [OPTION, ...]"',
        description="OpenTTD Game Observer UDP Server"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} {version.version}"
    )

    parser.add_argument(
        "openttd", action="store",
        help = "quoted path to openttd executable with options; like \"openttd -D\""
    )

    parser.add_argument(
        "--host", 
        default="127.0.0.1",
        help="hostname of this server (not opentdd's); default=%(default)s",
    )
    parser.add_argument(
        "--port", 
        default=3978,
        type=int,
        help="port number of this server (not openttd's); default=%(default)s",
    )
    parser.add_argument(
        "--ids", 
        help="comma delimited list of script ids to follow; like 1,2,3; "\
            + "dont set to monitor all scripts",
    )
    args = parser.parse_args()

    ttd_args = []
    for arg in shlex.split(args.openttd):
        if not ttd_args:
            p = Path(expanduser(arg)).resolve()
            if not p.exists():
                raise SystemExit(f"Cannot find executable: {p!r}")
            ttd_args.append(str(p))
        else:
            ttd_args.append(arg)

    if "-d" not in ttd_args and "--debug" not in ttd_args: # make sure we listen to game script
        ttd_args.append("-dscript=3")

    if args.ids:
        args.ids = [int(i) for i in args.ids.split(",")]

    args.openttd = ttd_args
    return args

