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

    SPLIT_STDIN_LINES_DEFAULT = "auto"
    parser.add_argument("--split-stdin-lines",
        help = f"start each line read from stdin on a new line. Defaults to {repr(SPLIT_STDIN_LINES_DEFAULT)}",
        choices = ["auto", "always", "never"],
        default = "auto"
    )

    args = parser.parse_args()

    return args

def main() -> None:
    args = get_cli_args()

    argv_strings: List[str] = getattr(args, "strings")
    max_per_line: int = getattr(args, "max_per_line")

    if argv_strings:
        reading_from_stdin = False
        strings = [" ".join(argv_strings)] # bloated str.join; could intersperse " " among argv_strings instead
    else:
        reading_from_stdin = True
        strings = sys.stdin # read line by line

    end = "\n"

    index_total = 0 # total number of characters read

    for string in strings:
        for c, codepoint, end in (
            (c, ord(c), "\n" if c_index % max_per_line == max_per_line - 1 else " ")
            for (c_index, c) in enumerate(string, start = index_total)
        ):
            if codepoint < 32 or codepoint == 0x7F:
                # naive check for non printable
                c = "."

            print(f"{CSI_BOLD}{c}{CSI_RESET} {int_to_unicode_format(codepoint):{MAX_UNICODE_FORMAT_LENGTH}}", end = end)

        if reading_from_stdin and (
            args.split_stdin_lines == "never"
            or (args.split_stdin_lines == "auto" and not sys.stdin.isatty())
        ):
            index_total += len(string)
        elif end != "\n":
            print()

if __name__ == "__main__":
    main()
