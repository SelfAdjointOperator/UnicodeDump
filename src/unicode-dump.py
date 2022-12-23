#!/usr/bin/env python3

from typing import *
import sys
import argparse

def csi(n: int) -> str:
    return f"\x1b[{n}m"

CSI_BOLD = csi(1)
CSI_RESET = csi(0)

def int_to_unicode_format(x: int):
    return f"U+{x:04X}"

MAX_UNICODE_CODEPOINT = 0x10FFFF
MAX_UNICODE_FORMAT_LENGTH = len(int_to_unicode_format(MAX_UNICODE_CODEPOINT))

def get_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description = "UTF-8 to codepoints. A bit like hexdump. Uses argv[1:] strings if specified else reads from stdin"
    )

    parser.add_argument("strings",
        metavar = "STRING",
        help = "strings to convert to codepoints",
        nargs = "*"
    )

    MAX_PER_LINE_DEFAULT = 8
    parser.add_argument("--max-per-line", "-N",
        metavar = "N",
        help = f"Maximum number of codepoints to print out on one line. Defaults to {MAX_PER_LINE_DEFAULT}",
        type = int,
        default = MAX_PER_LINE_DEFAULT
    )

    args = parser.parse_args()

    return args

def main() -> None:
    args = get_cli_args()

    argv_strings: List[str] = getattr(args, "strings")
    max_per_line: int = getattr(args, "max_per_line")

    if argv_strings:
        strings = [" ".join(argv_strings)] # bloated str.join; could intersperse " " among argv_strings instead
    else:
        strings = sys.stdin # read line by line

    end = "\n"

    for string in strings:
        for index, (c, codepoint) in enumerate(((c, ord(c)) for c in string)):
            codepoint_formatted = int_to_unicode_format(codepoint).ljust(MAX_UNICODE_FORMAT_LENGTH)

            if index % max_per_line == max_per_line - 1:
                end = "\n"
            else:
                end = " "

            if codepoint < 32:
                # naive check for non printable
                c = "."

            to_print = f"{CSI_BOLD}{c}{CSI_RESET} {codepoint_formatted}{end}"

            print(to_print, end = "")

        if end != "\n":
            print()

if __name__ == "__main__":
    main()
