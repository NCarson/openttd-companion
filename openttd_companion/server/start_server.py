import subprocess

from .parser import Parser
import openttd_companion.app_logging as mylogger
import openttd_companion.__init__ as init

logger = mylogger.setup_logger()

def run(args):

    output_parser = Parser(args)
    logger.info(f"{init.__title__} Server {init.__version__}")
    logger.info("running command '{}' ...".format(" ".join(args.openttd_cmd)))

    try:
        with subprocess.Popen(
            args.openttd_cmd, 
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
    return process.returncode
