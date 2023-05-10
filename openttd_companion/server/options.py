import sys
import argparse

import openttd_companion.__init__ as init
from openttd_companion.common_options import finish_options

def parse(config):
    parser = argparse.ArgumentParser(
        usage=f'{sys.argv[0]} [OPTION, ...] ["openttd [OPTION, ...]"]',
        description="OpenTTD Game Observer UDP Server"
    )

    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} {init.__version__}"
    )


    args = finish_options(config, parser)
    args.ids = None #FIXME
    return args

