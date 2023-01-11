import os
import sys
import json
import yaml
import subprocess
import threading
import time
import datetime

from .ui import Format, Colors, Icons
from .spinner import Spinner
from .repo import Repo


class ReposException:
    pass

class Repos:

    def __init__(self, root):
        self.root = root
        self.repos = {}


    def list(self):
        names = []
        for name in os.listdir(self.root):
            if name[0] == ".":
                continue

            dir = os.path.join(self.root, name)
            if os.path.isdir(dir):
                names.append(name)

        sort = sorted(names)
        for name in sort:
            dir = os.path.join(self.root, name)
            repo = Repo(dir)
            self.repos[name] = repo


    def configs(self):
        self.list()

        for _, repo in self.repos.items():
            repo.configs()
            # print(f"REPO {repo.dir}: {configs}")


    def archived(self):
        dirs   = []
        topDir = f"{self.root}/.archived"
        for name in os.listdir(topDir):
            fullDir = os.path.join(topDir, name)
            if os.path.isdir(fullDir):
                dirs.append(name)

        sort = sorted(dirs)
        print("\n".join(sort))


    def save(self, name):
        print(f"Saving repo {name}... ", end="", flush=True)
        repoDir = f"{self.root}/{name}"
        repo = Repo(repoDir)
        isOn = repo.run("git config repos.save")
        # print(f"isOn: {isOn}")

        if isOn == "true":
            repo.run("git add --all")
            repo.run("git commit --message 'Saving it all'")
            print(f"{Colors.GREEN}Saved{Colors.RESET}")
            return True
        else:
            print(f"{Colors.GRAY}Skipped{Colors.RESET}")


    def push(self, name):
        if not self.save(name):
            print(f"Pushing repo {name}... {Colors.GRAY}Skipped{Colors.RESET}", flush=True)
            return

        print(f"Pushing repo {name}... ", end="", flush=True)
        repoDir = f"{self.root}/{name}"
        repo = Repo(repoDir)
        isOn = repo.run("git config repos.push")

        if isOn == "true":
            repo.run("git push origin HEAD")
            print(f"{Colors.GREEN}Pushed{Colors.RESET}")
        else:
            print(f"{Colors.GRAY}Skipped{Colors.RESET}")


    def enable(self, name, feature):
        print(f"Enabling {feature} in repo {name}... ", end="", flush=True)
        repoDir = f"{self.root}/{name}"
        repo = Repo(repoDir)
        isOn = repo.run(f"git config repos.{feature}")

        if isOn == "true":
            print(f"{Colors.GRAY}Skipped{Colors.RESET}")
        else:
            repo.run(f"git config repos.{feature} true")
            print(f"{Colors.GREEN}Enabled{Colors.RESET}")


    def archive(self, name):
        now = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
        print(f"Archiving repo {name}... ", end="", flush=True)
        repoDir = f"{self.root}/{name}"
        archDir = f"{self.root}/.archived/{name}@{now}"

        if os.path.isdir(archDir):
            print(f" {Colors.GRAY}Skipped{Colors.RESET}")
            return

        if not os.path.isdir(repoDir):
            print(f" {Colors.RED}Fail{Colors.RESET}")
            exit(f"Error: Repo {name} is not an active repo.")

        os.system(f"mkdir -p {self.root}/_archived")
        os.system(f"mv {repoDir} {archDir}")
        print(f" {Colors.YELLOW}Archived{Colors.RESET} into {archDir}")


    def restore(self, name):
        print(f"Restoring repo {name}... ", end="", flush=True)
        repoDir = f"{self.root}/{name}"
        archDir = f"{self.root}/.archived/{name}"

        if os.path.isdir(repoDir):
            print(f" {Colors.GRAY}Skipped{Colors.RESET}")
            return

        if not os.path.isdir(archDir):
            print(f" {Colors.RED}Fail{Colors.RESET}")
            exit(f"Error: Repo {name} is not an archived repo.")

        os.system(f"mv {self.root}/_archived/{name} {self.root}/{name}")
        print(f" {Colors.GREEN}Restored{Colors.RESET}")


    def flip(self, name):
        print(f"Flipping repo {name}... ", end="", flush=True)
        repoDir = f"{self.root}/{name}"
        archDir = f"{self.root}/.archived/{name}"
        if os.path.isdir(repoDir):
            os.system(f"mkdir -p {self.root}/.archived")
            os.system(f"mv {self.root}/{name} {self.root}/.archived/{name}")
            print(f" {Colors.YELLOW}Archived{Colors.RESET}")
            return

        if os.path.isdir(archDir):
            os.system(f"mv {self.root}/_archived/{name} {self.root}/{name}")
            print(f" {Colors.GREEN}Restored{Colors.RESET}")
            return

        print(f" {Colors.RED}Fail{Colors.RESET}")
        exit(f"Error: Repo {name} is neither an active nor an archived repo.")


    def calc_pads(self, repos):
        self.pads = {
            "changes"  : 0,
            "ahead"    : 0,
            "behind"   : 0,
            "name"     : 0,
            "branch"   : 0,
            "branches" : 0,
            "remotes"  : 0,
        }

        for _, repo in self.repos.items():
            # repo.ago = self.ago(repo.modified)
            # if len(repo.ago) > pads["ago"]:
            #     pads["ago"] = len(repo.ago)
            if len(repo.name) > self.pads["name"]:
                self.pads["name"] = len(repo.name)

            if not repo.git:
                repo.name = repo.name + "/"
                continue

            if len(repo.branch) > self.pads["branch"]:
                self.pads["branch"] = len(repo.branch)
            if len(str(len(repo.branches))) > self.pads["branches"]:
                self.pads["branches"] = len(str(len(repo.branches)))
            if len(str(len(repo.remotes))) > self.pads["remotes"]:
                self.pads["remotes"] = len(str(len(repo.remotes)))
            if len(str(repo.changes)) > self.pads["changes"]:
                self.pads["changes"] = len(str(repo.changes))
            if len(str(repo.ahead)) > self.pads["ahead"]:
                self.pads["ahead"] = len(str(repo.ahead))
            if len(str(repo.behind)) > self.pads["behind"]:
                self.pads["behind"] = len(str(repo.behind))


    def text(self):
        print(f"{Colors.GRAY}  Repos in {Colors.GREEN}{self.root}{Colors.RESET}\n")

        self.calc_pads(self.repos)
        self.total = {
            "dir":      0,
            "solo":     0,
            "detached": 0,
            "clean":    0,
            "changed":  0,
            "ahead":    0,
            "behind":   0,
        }

        status_pad = 8 + self.pads['changes'] + self.pads['ahead'] + self.pads['behind'] + self.pads['branches'] + self.pads['remotes']
        if REPOS_REMOTES:
            status_pad += 2 + self.pads['remotes']

        print(f"  {Colors.GRAY}{self.pad('STATUS', status_pad, False)}    {self.pad('NAME', self.pads['name'], False)}    {self.pad('BRANCH', self.pads['branch'], False)}{Colors.RESET}")
        print(f"  {Colors.GRAY}{'─' * status_pad}    {'─' * (self.pads['name'])}    {'─' * (self.pads['branch'] + 2)}{Colors.RESET}")

        for _, repo in self.repos.items():
            changes = f"{Colors.GRAY}{ICON_DOT}{Colors.RESET}"
            ahead   = f"{Colors.GRAY}{ICON_DOT}{Colors.RESET}"
            behind  = f"{Colors.GRAY}{ICON_DOT}{Colors.RESET}"

            if repo.changes > 0:
                changes = f"{Colors.YELLOW}{repo.changes}{ICON_DIFF}{Colors.RESET}"

            if repo.ahead > 0:
                ahead = f"{Colors.GREEN}{repo.ahead}{ICON_UP}{Colors.RESET}"

            if repo.behind > 0:
                behind = f"{Colors.PURPLE}{repo.behind}{ICON_DOWN}{Colors.RESET}"

            if not repo.git:
                self.total["dir"] += 1
                color   = Colors.BLUE
                changes = ""
                ahead   = ""
                behind  = ""

            elif len(repo.remotes) < 1:
                self.total["solo"] += 1
                color = Colors.RED
                ahead = ""
                behind = f"{Colors.RED}{ICON_FLAG}{Colors.RESET}"

            elif repo.upstream is None:
                self.total["detached"] += 1
                color = Colors.ORANGE
                ahead = f"{Colors.ORANGE}{ICON_FLAG}{Colors.RESET}"
                behind = ""

            if repo.changes > 0:
                self.total["changed"] += 1
                color = Colors.YELLOW

            elif repo.behind > 0:
                self.total["behind"] += 1
                color = Colors.PURPLE

            elif repo.ahead > 0:
                self.total["ahead"] += 1
                color = Colors.GREEN

            elif repo.changes + repo.ahead + repo.behind == 0:
                self.total["clean"] += 1
                if repo.upstream:
                    color = Colors.GRAY

            else:
                print(repo)
                exit(55)

            if len(repo.branches) == 1:
                branches = f"{Colors.GRAY}{ICON_DOT}{Colors.RESET}"
            elif len(repo.branches) > 1:
                branches = f"{Colors.GRAY}{str(len(repo.branches))}{Colors.RESET}"
            else:
                branches = ""

            if len(repo.remotes) == 1:
                remotes = f"{Colors.GRAY}{ICON_DOT}{Colors.RESET}"
            elif len(repo.remotes) > 1:
                remotes = f"{Colors.GRAY}{str(len(repo.remotes))}{Colors.RESET}"
            else:
                remotes = ""

            status = self.status(changes, ahead, behind, branches, remotes)
            text = f"{color}  "
            text += f"{self.pad(repo.name, self.pads['name'], False)}    "
            # text += f"{self.pad(repo.branch, self.pads['branch'], False)}"

            text += f"{repo.icon} {repo.branch}"
            text += f"{Colors.RESET}"
            print(f" {status}  {text}")

        self.stats()


    def status(self, changes: str, ahead: str, behind: str, branches: str, remotes: str) -> str:
        text = f"{self.pad(changes, self.pads['changes'] + 2)} "
        text += f"{self.pad(behind, self.pads['behind'] + 2)} "
        text += f"{self.pad(ahead, self.pads['ahead'] + 2)}"
        if REPOS_REMOTES:
            text += f"{self.pad(remotes, self.pads['remotes'] + 2)}"
        text += f"{self.pad(branches, self.pads['branches'] + 2)}"

        return f"{text}"

    # def test(self):
    #     pad = 6
    #     tests = {
    #         "\033[38;5;220mBlah\033[0m": "--\033[38;5;220mBlah\033[0m",
    #         "\033[1mBla\033[0m": "---\033[1mBla\033[0m",
    #         "B": "-----B",
    #     }
    #     for text, expected in tests.items():
    #         returned = self.pad(text, pad)
    #         if returned != expected:
    #             print(f"Failed test on '{text}': expected '{expected}' vs returned '{returned}'.")
    #             exit(1)

    #     exit()


    def pad(self, text: str, pad: int, right: bool = True) -> str:
        # print(f"==> {len(text)}")
        # 1. '\033[38;5;220mBlah\033[0m'
        # 2. '\033[1mBlah\033[0m'
        # 3. 'Blah'
        fill = " "
        tag = "\033["
        if tag in text:
            pos = text.find(tag)
            end = text.find("m", pos)
            plain = text[end+1:]
            plain = plain.replace(f"{tag}0m", "")
            # print(f"==> PLAIN_TEXT: {plain}")
            pad = pad + len(text) - len(plain)
            # print(f"==> NEW PAD: {pad}")

        if right:
            return text.rjust(pad, fill)
        return text.ljust(pad, fill)


    # def ago(self, value):
    #     # print(f"AGO {value}")
    #     # if value is None:
    #     #     return ""

    #     timestamp = time.time()
    #     duration = math.floor(timestamp - value)

    #     SECOND = 1
    #     MINUTE = SECOND * 60
    #     HOUR   = MINUTE * 60
    #     DAY    = HOUR   * 24
    #     MONTH  = DAY    * 30
    #     YEAR   = DAY    * 365
    #     # WEEK   = DAY    * 7

    #     if duration < SECOND:
    #         return "A moment ago"

    #     if duration < MINUTE:
    #         return f"{math.floor(duration / SECOND)}s"

    #     if duration < HOUR:
    #         return f"{math.floor(duration / MINUTE)}m"

    #     if duration < DAY:
    #         return f"{math.floor(duration / HOUR)}h"

    #     if duration < MONTH:
    #         return f"{math.floor(duration / DAY)}d"

    #     if duration < YEAR:
    #         return f"{math.floor(duration / MONTH)}m"

    #     diff = datetime.datetime.fromtimestamp(value)
    #     return time.strftime("%Y-%m-%d", diff.timetuple())


    def stats(self):
        report = ""
        if self.total["dir"]:
            report += f"\n{self.total['dir']:9} directories"

        if self.total["solo"]:
            report += f"\n{self.total['solo']:9} without a remote {Colors.RED}{Icons.FLAG}{Colors.PALE}"

        if self.total["detached"]:
            # report += f"\n{self.total['detached']:9} without upstream {Colors.ORANGE}⚑{Colors.PALE}"
            report += f"\n{self.total['detached']:9} without upstream {Colors.ORANGE}{Icons.FLAG}{Colors.PALE}"

        if self.total["changed"]:
            report += f"\n{self.total['changed']:9} changed"

        if self.total["behind"]:
            report += f"\n{self.total['behind']:9} behind"

        if self.total["ahead"]:
            report += f"\n{self.total['ahead']:9} ahead"

        if self.total["clean"]:
            report += f"\n{self.total['clean']:9} clean"

        print(f"{Colors.PALE}{report}{Colors.RESET}")


    # @yaspin(text=f"Loading from root...", color="green")
    # @spinner
    def load(self):
        # if self.loaded:
        #     return

        self.list()
        threads = []

        showSpinner = bool(os.environ.get("REPOS_SPINNER", "false"))
        if showSpinner:
            spinner = threading.Thread(
                target=Spinner.start,
                args=(f" Loading from \033[32;1m{self.root}\033[0m...",)
            )
            spinner.start()

        for _, repo in self.repos.items():
            thread = threading.Thread(target=repo.load)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        if showSpinner:
            Spinner.stop()
        Spinner.show()
        self.loaded = True

    def show(self, name: str):
        repo = self.repos[name]
        print(repo)

    def jsonCmd(self, *_):
        self.load()
        data = {}
        for dir, repo in self.repos.items():
            data[dir] = repo.dict()

        print(json.dumps(data, indent=2))


    def yamlCmd(self, *_):
        self.load()
        data = {}
        for dir, repo in self.repos.items():
            data[dir] = repo.dict()

        print(yaml.dump(data, indent=2))


    def slowCmd(self, *_):
        self.list()
        for _, repo in self.repos.items():
            repo.load()
        self.textCmd()


    def textCmd(self, *_):
        self.load()
        self.text()


    def helpCmd(self, *_):
        print(Format.text(__doc__)) #.replace("$0", PROGRAM)))
        exit()


    def versionCmd(self, *_):
        print(VERSION)
        exit()


    def saveCmd(self, *args):
        repos = args[1:]
        if len(repos) > 0:
            for repo in repos:
                self.save(repo)
        else:
            print(f"Saving all configured repos")
            self.configs()
            for _, repo in self.repos.items():
                config = repo.config
                save = config.get("save", False)
                if save == "true":
                    # print(f"REPO {repo.dir}: {repo.config}")
                    self.save(repo.name)


    def enableCmd(self, *args):
        name = args[1]
        for arg in args[2:]:
            self.enable(name, arg)


    def pushCmd(self, *args):
        for arg in args[1:]:
            self.push(arg)
        # self._load()
        # for dir, repo in self.repos.items():
        #     if repo.changes > 0:
        #         print(f"{repo.changes:2}  {dir}")
        #         repo.run("git add --all")
        #         repo.run("git commit --message 'Saving it all'")


    def archiveCmd(self, *args):
        for arg in args[1:]:
            self.archive(arg)


    def archivedCmd(self, *_):
        self.archived()


    def restoreCmd(self, *args):
        for arg in args[1:]:
            self.restore(arg)


    def flipCmd(self, *args):
        for arg in args[1:]:
            self.flip(arg)


    def showCmd(self, *args):
        self.load()
        for arg in args[1:]:
            self.show(arg)


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


    def configCmd(self, *args):
        name  = args[1] if len(args) > 1 else None
        key   = args[2] if len(args) > 2 else None
        value = args[3] if len(args) > 3 else None

        if name is None:
             print("Usage: repos config <repo>")
             exit(1)

        path = os.path.join(self.root, name)
        repo = Repo(path)
        # configFile = os.path.join(path, ".git", "repos.yaml")
        # configExists = os.path.isfile(configFile)
        # print(f"Running config repo {name}: {key} --> {value}")

        repo.load()

        if not repo.git:
            print(f"Error: Repo {name} is not a valid git repo")
            exit(1)

        if key is None:
            print(yaml.dump(repo.config))
            return

        if value is None:
            print(repo.config(key, "(none)"))
            return

        data = {}
        if configExists:
            with open(configFile, "r") as f:
                text = f.read()
            if len(text.strip()) > 0:
                data = yaml.safe_load(text)

        data[key] = value
        with open(configFile, "w") as f:
            yaml.dump(
                data,
                f,
                sort_keys=False,
                indent=2,
            )

        # print(f"Saved config for repo {name}: {key} = {value} in {configFile} file.")
        print(f"Saved config for repo '{name}': '{key}' = '{value}'")
