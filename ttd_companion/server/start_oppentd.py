import subprocess
import sys
import shlex

args = shlex.split(" ".join(sys.argv[1:]))
with subprocess.Popen(
    args, 
    stderr=subprocess.PIPE, 
    encoding="utf-8",
    ) as process:

        while True:
            output = process.stderr.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())

        rc = process.poll()
