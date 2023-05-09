#!/usr/bin/python

import openttd_companion.server.options as options
import openttd_companion.server.start_server as start_server
from openttd_companion.config import Config

if __name__ == '__main__':
    config = Config()
    args = options.parse(config)
    start_server.run(args)


