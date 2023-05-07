import sys
import argparse
from pathlib import Path

import ttd_companion.version as version

def parse():
    parser = argparse.ArgumentParser(
        usage=f"{sys.argv[0]} [OPTION, ...]",
        description="OpenTTD Game Observer"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} {version.version}"
    )

    parser.add_argument(
        "-m", "--map", action="store",
        help="map file to load",
    )
    args = parser.parse_args()

    if (args.map and not Path(args.map).exists()):
        raise SystemExit(f"the file '{args.map}' does not exist")
        
    return args

