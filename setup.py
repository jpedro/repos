from setuptools import setup # find_packages
from repos import cli

setup(
    name="git-repos",
    version="1.0.0",
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
    # packages=find_packages(),
    packages=["repos"],
    install_requires=[
        "click",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "git-repos=repos.cli:main",
            "repos=repos.cli:main",
        ],
    },
)
