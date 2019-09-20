# pmcm

Python Markdown Content Manager.

This is a desktop wiki tool to manage notes and files,
inspired by [TiddlyWiki](https://tiddlywiki.com/).

The content is written in
[markdown](https://daringfireball.net/projects/markdown/syntax).

Each page of markdown text is stored in separate files in the `data/pages/` directory.

Non-markdown files can be "uploaded" and stored in the `media/` directory structure.

Tested on Ubuntu 18.04.

## Setup

1. `git clone https://github.com/ahernp/pmcm.git`
1. `cd pmcm`
1. `python3 -m venv pmcm` Create Python 3 virtual environment.
1. `source pmcm/bin/activate` Activate Python virtual environment.
1. `pip install markdown`
1. `cp -r initial_content/data .` Create and populate data directories.
1. `cp -r initial_content/media .` Create and populate media directories.
1. `python server.py -p 8088` Start application/server.
1. Visit <http://localhost:8088/> to use Wiki tool.

Read the [Help](http://localhost:8088/pages/Help) page in wiki for instructions on how to use the tool.
