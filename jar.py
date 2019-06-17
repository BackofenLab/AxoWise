"""
Interface towards Java's executable JAR files.
"""

import subprocess

def pipe_call(jar_path: str, stdin: str, encoding="utf-8"):
    """
    Runs an executable JAR file specified by `jar_path `and
    pipes `stdin` to its standard input. `encoding` specifies
    input's and output's encodings. Returns the standard output
    of the terminated JAR subprocess.
    """

    process = subprocess.Popen(
        ["java", "-jar", jar_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    )
    process.stdin.write(bytes(stdin, encoding))
    process.stdin.close() # EOF
    process.wait()
    return str(process.stdout.read(), encoding)
