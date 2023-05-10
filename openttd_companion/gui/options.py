import sys
import argparse
from pathlib import Path

import openttd_companion.__init__ as init
from openttd_companion.common_options import finish_options

def parse(config):
    parser = argparse.ArgumentParser(
        usage=f"{sys.argv[0]} [OPTION, ...]", #FIXME openttd is now an opt arg
        description=init.__title__
    )

    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} {init.__version__}"
    )

    parser.add_argument(
        "-m", "--map", 
        action="store",
    )
        
    args = finish_options(config, parser)

    if (args.map and not Path(args.map).exists()):
        raise SystemExit(f"the file '{args.map}' does not exist")
        
    return args

