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


def validate_and_sanitize_stdin(stdin: str) -> str:
    """
    Validates and sanitizes each line of the stdin string to ensure it only contains
    alphanumeric characters, hyphens, commas, and tildes.
    Newline characters are allowed between lines but not within a line.
    """
    if not isinstance(stdin, str):
        print("'stdin' must be a string.")
        raise ValueError("'stdin' must be a string.")

    pattern = re.compile(r"^[a-zA-Z0-9,~_\-]+$")

    lines = stdin.splitlines()
    # Check if any non-empty line contains invalid characters
    invalid_lines = [line for line in lines if line and not pattern.match(line)]
    if invalid_lines:
        print(f"stdin contains invalid characters: {invalid_lines}")
        raise ValueError(f"stdin contains invalid characters: {invalid_lines}")

    print("Validated and sanitized stdin")
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
