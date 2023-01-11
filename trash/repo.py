import os
import yaml
import subprocess


class Repo:

    def __init__(self, dir):
        self.dir      = dir
        self.name     = os.path.basename(dir)
        self.git      = False

        self.branch   = ""
        self.ref      = ""
        self.changes  = 0
        self.ahead    = 0
        self.behind   = 0
        self.branches = []
        self.remotes  = []

        self.upstream = None
        self.remote   = None
        self.url      = None
        self.config   = None
        self.icon     = " "
        # self.modified = None


    def load(self):
        # stat = os.stat(self.dir)
        # print(f"STAT {self.name} {stat.st_mtime}")
        # self.modified = stat.st_mtime

        self.git = bool(self.run("git rev-parse --is-inside-work-tree"))
        if self.git is False:
            return

        self.ref      = self.run("git symbolic-ref HEAD")
        self.branch   = self.ref.replace("refs/heads/", "")
        self.changes  = int(self.run("git status --porcelain | wc -l"))
        # self.remotes  = int(self.run("git remote | wc -l"))

        self.loadConfig()

        branches = self.run("git branch | cut -c 3-")
        if branches != "":
            self.branches = branches.split("\n")

        remotes = self.run("git remote")
        if remotes == "":
            return

        self.remotes = remotes.split("\n")
        if len(self.remotes) < 1:
            return

        upstream = self.run("git rev-parse --abbrev-ref @{u}")
        remote   = self.run(f"git config branch.{self.branch}.remote")

        self.upstream = upstream if upstream else None
        self.remote   = remote if remote else None

        if self.remote:
            self.url = self.run(f"git config remote.{self.remote}.url")
            if "git@github.com:" in self.url:
                self.icon = ""
            elif "https://github.com/" in self.url:
                self.icon = ""
            elif "@bitbucket.org/" in self.url:
                self.icon = ""
            elif "git@gitlab.com:" in self.url:
                self.icon = ""
            elif "git.heroku.com/" in self.url:
                self.icon = "\ue77b"
            elif "://git-codecommit." in self.url:
                self.icon = "\uf270"

        if self.upstream:
            cmd = f"git rev-list --count --left-right {self.upstream}...HEAD"
            diff = self.run(cmd).split("\t")
            self.behind = int(diff[0])
            self.ahead = int(diff[1])


    def loadConfig(self):
        config = os.path.join(self.dir, ".git", "repos.yaml")
        exists = os.path.isfile(config)
        if not exists:
            return

        with open(config, "r") as f:
            text = f.read()

        if len(text.strip()) < 1:
            return

        data = yaml.safe_load(text)
        self.config = data


    def saveConfig(self):
        config = os.path.join(self.dir, ".git", "repos.yaml")

        with open(config, "w") as f:
            yaml.dump(self.config, f)


    # git remote add origin git@github.com:jpedro/danger.git
    def __str__(self):
        return f"""
        Repo
            name      {self.name}
            dir       {self.dir}
            git       {self.git}

            branch    {self.branch}
            ref       {self.ref}
            changes   {self.changes}
            behind    {self.behind}
            ahead     {self.ahead}
            branches  {self.branches}
            remotes   {self.remotes}

            remote    {self.remote}
            url       {self.url}
            upstream  {self.upstream}
            config    {self.config}
        """

    def dict(self):
        return {
            "name":      self.name,
            "dir":       self.dir,
            "git":       self.git,

            "branch":    self.branch,
            "ref":       self.ref,
            "changes":   self.changes,
            "behind":    self.behind,
            "ahead":     self.ahead,
            "branches":  self.branches,
            "remotes":   self.remotes,

            "remote":    self.remote,
            "url":       self.url,
            "upstream":  self.upstream,
            "config":    self.config,
        }

    def configs(self) -> dict:
        if self.config:
            return self.config

        self.config = {}
        # print(f"Loading {self.dir} config")
        lines = self.run(f"git config --list").split("\n")
        for line in lines:
            pos = line.find("=")
            if pos > -1:
                parts = line.split("=")
                key = parts[0]
                if key.find("repos.") == 0:
                    key = key[len("repos:"):]
                    val = "=".join(parts[1:])
                    # print(f"Found {key}: {val}")
                    self.config[key] = val

        return self.config

    def run(self, cmd) -> str:
        cmd = f"cd {self.dir} && {cmd}"
        try:
            res = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL)
            dec = res.decode("UTF-8").strip()
            # if dec == "":
            #     return None
            return dec

        except Exception as e:
            return None
