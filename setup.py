from setuptools import setup
from repos import cli, VERSION

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="repos",
    version=VERSION,
    description="Manages git repos inside a directory",
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
    packages=[
        "repos",
    ],
    install_requires=[
        "click",
        "pyaml",
    ],
    entry_points={
        "console_scripts": [
            "repos=repos.cli:main",
        ],
    },
)
