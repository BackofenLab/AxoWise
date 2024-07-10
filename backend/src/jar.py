"""
Interface towards Java's executable JAR files.
Assumes Java is already installed and set up,
i.e. `java` is in PATH variable and available
to be called.
"""

import os
import re
import subprocess


def validate_and_sanitize_jar_path(jar_path: str) -> str:
    """
    Validates and sanitizes the JAR file path.
    """
    # Ensure the path exists
    if not os.path.exists(jar_path):
        raise ValueError("JAR path does not exist.")

    # Ensure the path points to a .jar file
    if not jar_path.endswith(".jar"):
        raise ValueError("Path does not point to a .jar file.")

    # Resolve to absolute path
    abs_path = os.path.abspath(jar_path)

    # Ensure the path does not contain any dangerous characters
    if not re.match(r"^[\w./-]+$", abs_path):
        raise ValueError("Path contains invalid characters.")

    return abs_path


def validate_and_sanitize_stdin(stdin):
    """
    Validates and sanitizes the stdin string to ensure it only contains
    alphanumeric characters, hyphens, commas, and tildes.
    Newline characters are not allowed.
    """

    # Ensure 'stdin' is a string
    if not isinstance(stdin, str):
        raise ValueError("'stdin' must be a string.")

    # Define a pattern for allowed characters, including tilde (~)
    pattern = re.compile(r"[a-zA-Z0-9,~\n-]+")

    # Validate stdin with the defined pattern
    if not pattern.match(stdin):
        raise ValueError("stdin contains invalid characters.")

    return stdin


def pipe_call(jar_path: str, stdin: str, encoding="utf-8"):
    """
    Runs an executable JAR file specified by `jar_path` and
    pipes `stdin` to its standard input. `encoding` specifies
    input's and output's encodings. Returns the standard output
    of the terminated JAR subprocess.
    """

    # Validate and sanitize 'jar_path'
    jar_path = validate_and_sanitize_jar_path(jar_path)

    # Validate and sanitize 'stdin'
    stdin = validate_and_sanitize_stdin(stdin)

    # Run JAR file and capture its standard output
    output = subprocess.run(
        ["java", "-jar", jar_path],
        input=bytes(stdin, encoding),
        capture_output=True,
        shell=False,
    )

    if not output.stdout:
        raise Exception(output.stderr.decode())
    else:
        return output.stdout.decode()
