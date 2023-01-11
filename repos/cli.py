#!/usr/bin/env python3
"""NAME
    repos —  Manages your git repos

USAGE
    repos                       # Lists all repos in text format
    repos export --json         # Exports all repos as json
    repos export --yaml         # Exports all repos as yaml
    repos show REPO             # Saves configured repos
    repos save                  # Saves configured repos
    repos push                  # Pushes to upstream
    repos pull                  # Pulls from upstream
    repos sync                  # Pull from upstream and save
    repos help                  # Shows this help
    repos version               # Prints the current version
"""
import os
import sys
import time

from .ui import Colors
from .repos import Repos


VERSION = "0.1.2"
REPOS_TIMER = bool(os.environ.get("REPOS_TIMER", ""))

class CliException(BaseException):
    pass


class Cli:

    def __init__(self, repos: Repos):
        self.repos = repos


    def exportCmd(self, *args):
        format = args[1] if len(args) > 1 else "--yaml"
        if format == "--json":
            self.repos.export("json")
            return

        if format == "--yaml":
            self.repos.export("yaml")
            return

        raise CliException(f"Unknown export format {format}.")


    def slowCmd(self, *_):
        self.repos.list()
        for _, repo in self.repos.items():
            repo.load()
        self.textCmd()


    def textCmd(self, *_):
        self.repos.load()
        self.repos.text()


    def helpCmd(self, *args):
        # print(args); exit(99)
        # print(Format.text(__doc__)) #.replace("$0", PROGRAM)))
        print(__doc__)
        exit()


    def versionCmd(self, *_):
        print(VERSION)
        exit()


    # def saveCmd(self, *args):
    #     repos = args[1:]
    #     if len(self.repos.repos) > 0:
    #         for repo in repos:
    #             self.save(repo)
    #     else:
    #         print(f"Saving all configured repos")
    #         self.configs()
    #         for _, repo in self.repos.items():
    #             config = repo.config
    #             save = config.get("save", False)
    #             if save == "true":
    #                 # print(f"REPO {repo.dir}: {repo.config}")
    #                 self.save(repo.name)


    # def enableCmd(self, *args):
    #     name = args[1]
    #     for arg in args[2:]:
    #         self.enable(name, arg)


    # def pushCmd(self, *args):
    #     for arg in args[1:]:
    #         self.push(arg)
    #     # self._load()
    #     # for dir, repo in self.repos.items():
    #     #     if repo.changes > 0:
    #     #         print(f"{repo.changes:2}  {dir}")
    #     #         repo.run("git add --all")
    #     #         repo.run("git commit --message 'Saving it all'")


    def archiveCmd(self, *args):
        for arg in args[1:]:
            self.repos.archive(arg)


    def archivedCmd(self, *_):
        self.repos.archived()


    def restoreCmd(self, *args):
        for arg in args[1:]:
            self.repos.restore(arg)


    def flipCmd(self, *args):
        for arg in args[1:]:
            self.repos.flip(arg)


    def showCmd(self, *args):
        self.repos.load()
        for arg in args[1:]:
            self.repos.show(arg)


    def todosCmd(self, *args):
        print()
        print("TODOS:")
        print("- Sync colors with prompt")
        print("- Implement repo config:")
        print()
        print("    repos config repo1                  # Shows all configs for repo1")
        print("    repos config repo1,repo2 key1,key2  # Shows key1 and key2 configs")
        print("    repos config repo1,repo2 key=value  # Sets value for key")
        print()
        print("    Available configs:")
        print("       repos.save      always| never | ask")
        print("       repos.push      always| never | ask")
        print("       repos.fetch     always| never | ask")
        print("       repos.sync      always| never | ask")


    # def configCmd(self, *args):
    #     name  = args[1] if len(args) > 1 else None
    #     key   = args[2] if len(args) > 2 else None
    #     value = args[3] if len(args) > 3 else None

    #     if name is None:
    #          print("Usage: repos config <repo>")
    #          exit(1)

    #     path = os.path.join(self.root, name)
    #     repo = Repo(path)
    #     # configFile = os.path.join(path, ".git", "repos.yaml")
    #     # configExists = os.path.isfile(configFile)
    #     # print(f"Running config repo {name}: {key} --> {value}")

    #     repo.load()

    #     if not repo.git:
    #         print(f"Error: Repo {name} is not a valid git repo")
    #         exit(1)

    #     if key is None:
    #         print(yaml.dump(repo.config))
    #         return

    #     if value is None:
    #         print(repo.config(key, "(none)"))
    #         return

    #     data = {}
    #     if configExists:
    #         with open(configFile, "r") as f:
    #             text = f.read()
    #         if len(text.strip()) > 0:
    #             data = yaml.safe_load(text)

    #     data[key] = value
    #     with open(configFile, "w") as f:
    #         yaml.dump(
    #             data,
    #             f,
    #             sort_keys=False,
    #             indent=2,
    #         )

    #     # print(f"Saved config for repo {name}: {key} = {value} in {configFile} file.")
    #     print(f"Saved config for repo '{name}': '{key}' = '{value}'")


def main():
    if len(sys.argv) < 2:
        cmd = "text"
        args = []
    else:
        cmd = sys.argv[1]
        args = sys.argv[1:]

    # root  = os.path.expanduser("~/code")
    root = os.getcwd()
    repos = Repos(root)
    if repos.isGitRepo():
        print(f"\033[31;1mError:\033[0m You are running this command inside a git repo ({root}).")
        # print(f"       Using {root} dir.")
        # print(f"↪  Using {root} dir.")
        exit(1)

    cli = Cli(repos)
    try:
        start = time.perf_counter()
        call = getattr(cli, f"{cmd}Cmd")
        call(cli, *args[1:])

        if REPOS_TIMER:
            done = time.perf_counter() - start
            print(f"\n  {Colors.GRAY}Took {(done * 1000):0.0f} ms{Colors.RESET}", file=sys.stderr)

    except Exception as e:
        print(f"Error: `{e}`.", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
