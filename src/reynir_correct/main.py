#!/usr/bin/env python
"""

    Greynir: Natural language processing for Icelandic

    Spelling and grammar checking module

    Copyright (C) 2022 Miðeind ehf.

    This software is licensed under the MIT License:

        Permission is hereby granted, free of charge, to any person
        obtaining a copy of this software and associated documentation
        files (the "Software"), to deal in the Software without restriction,
        including without limitation the rights to use, copy, modify, merge,
        publish, distribute, sublicense, and/or sell copies of the Software,
        and to permit persons to whom the Software is furnished to do so,
        subject to the following conditions:

        The above copyright notice and this permission notice shall be
        included in all copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
        EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
        MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
        IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
        CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
        TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
        SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


    This is an executable program wrapper (main module) for the GreynirCorrect
    package. It can be used to invoke the corrector from the command line,
    or via fork() or exec(), with the command 'correct'. The main() function
    of this module is registered as a console_script entry point in setup.py.

"""

from typing import (
    Dict,
    Union,
)

import sys
import argparse
from .wrappers import check_errors


# File types for UTF-8 encoded text files
ReadFile = argparse.FileType("r", encoding="utf-8")
WriteFile = argparse.FileType("w", encoding="utf-8")

# Define the command line arguments

parser = argparse.ArgumentParser(description="Corrects Icelandic text")

parser.add_argument(
    "infile",
    nargs="?",
    type=ReadFile,
    default=sys.stdin,
    help="UTF-8 text file to correct",
)
parser.add_argument(
    "outfile",
    nargs="?",
    type=WriteFile,
    default=sys.stdout,
    help="UTF-8 output text file",
)

parser.add_argument(
    "--suppress_suggestions",
    "-ss",
    action="store_true",
    help="Suppress more agressive error suggestions",
)

parser.add_argument(
    "--spaced", "-sp", help="Separate tokens with spaces", action="store_true"
)

# Determines the output format
parser.add_argument(
    "--format",
    "-f",
    nargs="?",
    type=str,
    default="text",
    help="Determine output format.\ntext: Corrected text only.\ncsv: One token per line in CSV format.\njson: One token per line in JSON format.\nm2: M2 format, GEC standard.",
)

# Determines whether we supply only token-level annotations or also sentence-level annotations
parser.add_argument(
    "--all_errors",
    "-a",
    help="Annotate both grammar and spelling errors",
    action="store_true",
)

# Add --grammar for compatibility; works the same as --all_errors
parser.add_argument(
    "--grammar",
    "-g",
    help="Annotate both grammar and spelling errors",
    action="store_true",
)

# Add --json for compatibility; works the same as --format=json
parser.add_argument(
    "--json",
    "-j",
    help="Output in JSON format",
    action="store_true",
)

# Add --csv for compatibility; works the same as --format=csv
parser.add_argument(
    "--csv",
    "-c",
    help="Output in CSV format",
    action="store_true",
)

# Add --normalize
parser.add_argument(
    "--normalize",
    "-n",
    help="Normalize punctuation",
    action="store_true",
)


def main() -> None:
    """Main function, called when the 'correct' command is invoked"""

    args = parser.parse_args()
    # Fill options with information from args
    if args.infile is sys.stdin and sys.stdin.isatty():
        # terminal input is empty, most likely no value was given for infile:
        # Nothing we can do
        print("No input has been given, nothing can be returned")
        sys.exit(1)
    options: Dict[str, Union[bool, str]] = {}
    options["input"] = args.infile
    if args.suppress_suggestions:
        options["suppress_suggestions"] = args.suppress_suggestions
    options["format"] = args.format
    if args.json:
        options["format"] = "json"
    elif args.csv:
        options["format"] = "csv"
    options["spaced"] = args.spaced
    options["normalize"] = args.normalize
    options["all_errors"] = args.all_errors or args.grammar
    print(check_errors(**options), file=args.outfile)


if __name__ == "__main__":
    main()
