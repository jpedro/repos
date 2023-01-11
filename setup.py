from setuptools import setup, find_packages
from git_repos.cli import VERSION, Repos

setup(
  name="git-repos",
  version=VERSION,
  description="Manages git repos inside a directory",
  long_description="Manages git repos inside a directory.",
  author="jpedro",
  author_email="jpedro.barbosa@gmail.com",
  url="https://github.com/jpedro/git-repos",
  download_url="https://github.com/jpedro/git-repos/tarball/master",
  keywords="git repos",
  license="MIT",
  classifiers=[
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Build Tools",
    "License :: OSI Approved :: MIT License",
  ],
  packages=find_packages(),
  install_requires=[
    "click",
  ],
  entry_points={
    "console_scripts": [
      "git-repos=git_repos.cli:main"
      "repos=git_repos.cli:main"
    ]
  },
)
