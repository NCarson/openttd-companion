import sys
import argparse
import shlex
from pathlib import Path
from os.path import expanduser

import openttd_companion.__init__ as init

def parse(config):
    parser = argparse.ArgumentParser(
        usage=f'{sys.argv[0]} [OPTION, ...] ["openttd [OPTION, ...]"]',
        description="OpenTTD Game Observer UDP Server"
    )
    parser.add_argument(
        "openttd_cmd", action="store",
        default=config.openttd_cmd,
        nargs="?",
        help = "quoted path to openttd executable with options; default=%(repr(default))s"
    )

    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} {init.__version__}"
    )

    parser.add_argument(
        "--host", 
        default=config.udp_host,
        help="hostname of this server (not opentdd's); default=%(default)s",
    )

    parser.add_argument(
        "--port", 
        default=config.udp_port,
        type=int,
        help="port number of this server (not openttd's); default=%(default)s",
    )

    parser.add_argument(
        "--bufsize", 
        default=config.udp_buffer_size,
        help="packet size of this server (not openttd's); default=%(default)s",
    )

    parser.add_argument(
        "--ids",  ##FIXME lest figure this on loading. Give a shout when script loads
        default=config.script_ids,
        help="comma delimited list of script ids to follow; like 1,2,3; "\
            + "dont set to monitor all scripts",
    )

    args = parser.parse_args()

    ttd_args = []
    for arg in shlex.split(args.openttd_cmd):
        if not ttd_args:
            p = Path(expanduser(arg)).resolve()
            if not p.exists():
                raise SystemExit(f"Cannot find executable: {p!r}")
            ttd_args.append(str(p))
        else:
            ttd_args.append(arg)

    if "-d" not in ttd_args and "--debug" not in ttd_args: # make sure we listen to game script
        ttd_args.append("-dscript=4")

    if args.ids:
        args.ids = [int(i) for i in args.ids.split(",")]

    args.openttd = ttd_args
    return args

