"""
Interface towards Java's executable JAR files.
Assumes Java is already installed and set up,
i.e. `java` is in PATH variable and available
to be called.
"""

import subprocess


def pipe_call(jar_path: str, stdin: str, encoding="utf-8"):
    """
    Runs an executable JAR file specified by `jar_path `and
    pipes `stdin` to its standard input. `encoding` specifies
    input's and output's encodings. Returns the standard output
    of the terminated JAR subprocess.
    """

    # Runs the executable JAR file given the standard input 'stdin' to recieve an CompletedProcess Object
    output = subprocess.run(
        ["java", "-jar", jar_path], input=bytes(stdin, encoding), capture_output=True
    )

    # Check standard output 'stdout' whether it's empty to control errors
    if not output.stdout:
        raise Exception(output.stderr.decode())
    else:
        return output.stdout.decode()
