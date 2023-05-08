import sys
import subprocess
import socket
import json


import options
import version
from ttd_output_parser import TTDOutputParser

from mylogger import Logging, SimpleStreamFormatter
logger = Logging.getLogger(
    "test.log",
    stream_formatter=SimpleStreamFormatter(),
    )

BUF_SIZE = 1024

def sendMessage(msg):
    msg = json.dumps(msg)

    def split_msg(msg, size):
        return ([msg[i:i+size] for i in range(0, len(msg), size)])

    for piece in split_msg(msg, BUF_SIZE):
        piece = bytes(piece, 'utf-8')
        logger.debug(f"sending msg on {args.host, args.port}: {piece[:20]} ...")
        sock.sendto(piece, (args.host, args.port))


args = options.parse()
f = lambda x : sendMessage(x)
output_parser = TTDOutputParser(f, ids=args.ids)
logger.info(f"{version.title} {version.version}")

logger.info(f"starting udp server on {args.host}:{args.port} ...")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet UDP

logger.info("running command '{}' ...".format(" ".join(args.openttd)))
try:
    with subprocess.Popen(
        args.openttd, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT,
        encoding="utf-8",
        ) as process:

            while True:

                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    try:
                        output_parser.onData(output.strip())
                    except:
                        process.kill()
                        raise


except:
    raise
sys.stdout.write(f"openttd exited with code {process.returncode}\n")





    
