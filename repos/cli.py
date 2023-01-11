#!/usr/bin/env python3
"""NAME
    repos —  Manages your git repos

USAGE
    repos                       # Lists all repos
    repos --json                # Exports the repos as json
    repos --yaml                # Exports the repos as yaml
    repos show REPO             # Saves configured repos
    repos save                  # Saves configured repos
    repos push                  # Pushes to upstream
    repos pull                  # Pulls from upstream
    repos sync                  # Pull from upstream and save
    repos --help                # Shows this help
    repos --version             # Prints the current version
"""
import os
import sys
import time

from .ui import Colors
from .repos import Repos


VERSION = "v0.1.0"
PROGRAM = os.path.basename(__file__)
REPOS_REMOTES = bool(os.environ.get("REPOS_REMOTES", "1"))
REPOS_TIMER = bool(os.environ.get("REPOS_TIMER", "0"))


def main():
    if len(sys.argv) < 2:
        cmd = "text"
        args = []
    else:
        cmd = sys.argv[1]
        args = sys.argv[1:]

    # root  = os.path.expanduser("~/code")
    root = os.getcwd()
    repo = Repo(root)
    repo.load()
    if repo.git:
        print(f"\033[31;1mError:\033[0m Run this command outside a git repo (using {root}).")
        # print(f"       Using {root} dir.")
        # print(f"↪  Using {root} dir.")
        exit(1)

    repos = Repos(root)
    try:
        start = time.perf_counter()
        call = getattr(repos, f"{cmd}Cmd")
        call(repos, *args[1:])
        done = time.perf_counter() - start

        if REPOS_TIMER:
            print(f"\n  {Colors.PALE}Took {(done * 1000):0.0f} ms{Colors.RESET}", file=sys.stderr)

    except Exception as e:
        print(f"Error: `{e}`.", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
