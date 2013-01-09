Starter 
==============

This is a repo from which I start my application development with python, flask, mongo, and heroku.

To install python, mongo, and heroku on a mac:
1. install macports and xcode
2. run: sudo port install python
3. run: sudo port install py27-virtualenv (virtual environment to be able to control python installs)
3. run: sudo port install mongodb
4. install heroku toolbelt, https://toolbelt.heroku.com/ (foreman, git, heroku client)
5. set up github, https://help.github.com/articles/set-up-git and then fork/clone this repo

To begin on a mac (while in a local copy of the starter repo):
1. run: python /opt/local/Library/Frameworks/Python.framework/Versions/2.7/bin/virtualenv-2.7 env 
2. run:source env/bin/activate (now you should see env at the beginning of the terminal command line)
3. run: pip install -r requirements.txt (installing flask, extensions, mongoengine, etc...)
4. run: python loaddata.py (populates initial data from data.json in app folder)
5. run: foreman start Procfile.dev (runs in development environment)
