#!/usr/bin/env python3
"""Check that every braid command the page shows exists in the CLI.

Braid changes often during the preview, and a renamed command or flag leaves
the page wrong without breaking the build. This reads each `braid ...` command
in docs/index.md, from inline code and from shell blocks, and checks it
against the installed CLI's own help: each subcommand must be listed under its
parent, each flag must be accepted, and a flag value must be one the help names
when it names a fixed set, as in `approved|requested-changes|blocked`.

It needs a braid binary. Braid publishes macOS builds only, so CI runs this on
a macOS runner against the latest release.
"""

import argparse
import functools
import pathlib
import re
import shlex
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "docs" / "index.md"

# Fences can be indented, as they are inside list items.
FENCE = re.compile(r"^[ \t]*```(\w*)\n(.*?)^[ \t]*```", re.MULTILINE | re.DOTALL)
INLINE = re.compile(r"`(braid [^`]+)`")
SHELL_LANGUAGES = {"", "sh", "bash", "shell", "console"}


def page_commands(text):
    """Return each braid command on the page, in order, without duplicates."""
    commands = []
    for language, body in FENCE.findall(text):
        if language not in SHELL_LANGUAGES:
            continue
        for line in body.splitlines():
            line = line.strip()
            if line.startswith("braid "):
                commands.append(line)
    prose = FENCE.sub("", text)
    commands.extend(match.strip() for match in INLINE.findall(prose))
    return list(dict.fromkeys(commands))


def parse_help(text):
    """Return the subcommands and flags one `--help` page lists."""
    subcommands = set()
    in_commands = False
    for line in text.splitlines():
        if line.startswith("Available Commands:"):
            in_commands = True
            continue
        if in_commands:
            match = re.match(r"^  (\S+)\s", line)
            if match:
                subcommands.add(match.group(1))
            elif not line.strip():
                in_commands = False
    flags = {}
    for line in text.splitlines():
        match = re.match(r"^\s+(?:-\w, )?(--[\w-]+)(.*)$", line)
        if match:
            flags[match.group(1)] = match.group(2)
    return subcommands, flags


def flag_choices(description):
    """Return the fixed values a flag's help names, or None when it names none."""
    match = re.search(r":\s*([\w-]+(?:\|[\w-]+)+)", description)
    return set(match.group(1).split("|")) if match else None


def is_placeholder(token):
    return token.startswith("<") and token.endswith(">")


def check_command(command, read_help):
    """Return the problems with one command, given a help reader."""
    tokens = shlex.split(command)
    path = [tokens[0]]
    subcommands, flags = read_help(tuple(path))
    errors = []
    index = 1
    while index < len(tokens):
        token = tokens[index]
        if token.startswith("--"):
            name, _, inline_value = token.partition("=")
            if name not in flags:
                errors.append(f"`{command}`: `{' '.join(path)}` has no {name} flag")
                index += 1
                continue
            choices = flag_choices(flags[name])
            value = inline_value
            if not value and index + 1 < len(tokens) and not tokens[index + 1].startswith("-"):
                value = tokens[index + 1]
                index += 1
            if choices and value and not is_placeholder(value) and value not in choices:
                errors.append(
                    f"`{command}`: {name} takes {'|'.join(sorted(choices))}, not {value}"
                )
        elif not is_placeholder(token) and token in subcommands:
            path.append(token)
            subcommands, flags = read_help(tuple(path))
        elif not is_placeholder(token) and subcommands and len(path) == index:
            # Still walking the command path, and this word is not a subcommand.
            errors.append(f"`{command}`: `{' '.join(path)}` has no {token} subcommand")
        index += 1
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--braid", default="braid", help="the braid binary to check against")
    parser.add_argument("page", nargs="?", type=pathlib.Path, default=PAGE)
    args = parser.parse_args()

    @functools.lru_cache(maxsize=None)
    def read_help(path):
        result = subprocess.run(
            [args.braid, *path[1:], "--help"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise SystemExit(f"`{' '.join(path)} --help` failed:\n{result.stderr}")
        return parse_help(result.stdout)

    version = subprocess.run(
        [args.braid, "--version"], capture_output=True, text=True, check=False
    ).stdout
    tag = re.search(r"Version:\s+(\S+)", version)

    commands = page_commands(args.page.read_text(encoding="utf-8"))
    errors = [error for command in commands for error in check_command(command, read_help)]
    for error in errors:
        print(f"{args.page}: {error}", file=sys.stderr)
    if errors:
        return 1
    print(
        f"{len(commands)} braid commands match braid {tag.group(1) if tag else '(unknown version)'}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
