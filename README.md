# Git repos

[![PyPI version](https://badge.fury.io/py/git-repos.svg)](https://badge.fury.io/py/git-repos)
[![Unstable package](https://img.shields.io/badge/_Unstable_package_-_This_code_is_a_work_in_progress_-red)](https://semver.org)


Manages git repos inside a directory.


## Install

    pip install git-repos


## Usage

Inside a directory with several git repos run:

    repos

To check all available commands:

```
$ repos help
NAME
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
```


## Todos

- [ ] Code the `repos config <repo> [key] [value]` subcommand to
      store `git config repos.*` in `./.git/config` file.

- [ ] Create the `repos add <url>` subcommand to clone a git repo from
      an url.

- [ ] Create the `repos install [file]` subcommand to clone git repos
      from a file, by default `repos.yaml`.

- [ ] Code the `repos save [repo] [--yes]` subcommand to commit all
      changes (obeys the `repo.save = always | never | ask` git config).

- [ ] Code the `repos push [repo] [--yes]` subcommand to send all
      commits to the upstream (obeys the `repo.push = always | never |
      ask` git config).

- [ ] Code the `repos pull [repo] [--yes]` subcommand to pull all the
      latest commits from the upstream (obeys the `repo.pull = always |
      never | ask` git config).

- [ ] Code the `repos sync [repo] [--yes]` subcommand to commits all
      changes, pull the latest commits, and push local commits to the
      upstream (obeys the `repo.sync = always | never | ask` git config).

- [ ] Code the `repos.enabled` git config to turn off all other `repos.*`
      configs.
