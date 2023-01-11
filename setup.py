from setuptools import setup
from repos import cli

with open("README.md", "r") as f:
    readme = f.read()


setup(
    name="git-repos",
    version=cli.VERSION,
    description="Manages git repos inside a directory",
    # long_description="Manages git repos inside a directory.",
    long_description=readme,
    long_description_content_type="text/markdown",
    readme="README.md",
    author="jpedro",
    author_email="jpedro.barbosa@gmail.com",
    url="https://github.com/jpedro/repos",
    download_url="https://github.com/jpedro/repos/tarball/master",
    keywords="git repos",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
    ],
    # packages=find_packages(),
    packages=[
        "repos",
    ],
    install_requires=[
        # "click",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "git-repos=repos.cli:main",
            "repos=repos.cli:main",
        ],
    },
)
