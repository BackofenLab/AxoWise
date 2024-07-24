import os
import re
import shlex
import subprocess  # nosec
from shutil import which


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

    pattern = re.compile(r"^[a-zA-Z0-9,:~_\-\(\)\s]+$")

    lines = stdin.splitlines()
    # Check if any non-empty line contains invalid characters
    invalid_lines = [line for line in lines if line and not pattern.match(line)]
    if invalid_lines:
        print(f"stdin contains invalid characters: {invalid_lines}")
        raise ValueError(f"stdin contains invalid characters: {invalid_lines}")

    print("Validated and sanitized stdin")
    return stdin


def get_java_path() -> str:
    """
    Gets the full path to the Java executable.
    """
    java_path = which("java")
    if java_path is None:
        raise EnvironmentError("Java executable not found in PATH.")
    return java_path


def pipe_call(jar_path: str, stdin: str, encoding="utf-8") -> str:
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

    # Get the full path to the Java executable
    java_path = get_java_path()

    # Prepare the command with shlex
    # to ensure proper quoting of arguments
    command = [java_path, "-jar", jar_path]
    command = [shlex.quote(arg) for arg in command]

    # Run JAR file and capture its standard output
    try:
        output = subprocess.run(
            command,
            input=stdin.encode(encoding),
            capture_output=True,
            # Bandit warning suppressed after implementation of input validation and shlex.quote
            shell=False,  # nosec
            check=True,  # This will raise an error if the command fails
        )
        return output.stdout.decode(encoding)
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error running JAR file: {e.stderr.decode(encoding)}")
