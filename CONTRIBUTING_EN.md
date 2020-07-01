# How to contribute to sidrapy
Thank you for considering contributing to sidrapy!

## Support questions
Please, don't use the issue tracker for this.
The issue tracker is a tool to address bugs and feature requests in sidrapy itself.
Use our Telegram group for questions about using sidrapy or issues with your own code:
* [Telegram Group](https://t.me/joinchat/AmdQix1KKeZ5KGpsKVFsKw)

## Reporting issues
Include the following information in your post:
* Describe what you expected to happen.
* If possible, include a [minimal reproducible](https://stackoverflow.com/help/minimal-reproducible-example) example to help us identify the issue. This also helps check that the issue is not with your own code.
* Describe what actually happened. Include the full traceback if there was an exception.
* List your Python and sidrapy. If possible, check if this issue is already fixed in the latest releases or the latest code in the repository.

## Submitting patches
If there is not an open issue for what you want to submit, prefer opening one for discussion before working on a PR. You can work on any issue that doesn't have an open PR linked to it or a maintainer assigned to it. These show up in the sidebar. No need to ask if you can work on an issue that interests you.

Include the following in your patch:
* Use [Black](https://black.readthedocs.io/) to format your code. This and other tools will run automatically if you install [pre-commit](https://pre-commit.com/) using the instructions below.
* Include tests if your patch adds or changes code. Make sure the test fails without your patch.
* Update any relevant docs pages and docstrings. Docs pages and docstrings should be wrapped at 72 characters.

### First time setup
* Download and install the [latest version of git](https://git-scm.com/downloads).

* Configure git with your [username](https://help.github.com/en/articles/setting-your-username-in-git) and [email](https://help.github.com/en/articles/setting-your-commit-email-address-in-git).
```shell script
$ git config --global user.name 'your name'
$ git config --global user.email 'your email'
```

* Make sure you have a [GitHub account](https://github.com/join).

* Fork sidrapy to your GitHub account by clicking the [Fork](https://github.com/AlanTaranti/sidrapy/fork) button.

* [Clone](https://help.github.com/en/articles/fork-a-repo#step-2-create-a-local-clone-of-your-fork) the main repository locally.
```shell script
$ git clone https://github.com/AlanTaranti/sidrapy
$ cd sidrapy
```

* Add your fork as a remote to push your work to. Replace `{username}` with your username. This names the remote "fork", the default AlanTaranti remote is "origin".
```shell script
$ git remote add fork https://github.com/{username}/sidrapy
```

* Create a virtualenv.
```shell script
$ python3 -m venv venv
$ . venv/bin/activate
```

On Windows, activating is different.
```shell script
> env\Scripts\activate
```

* Install sidrapy in editable mode with development dependencies.
```shell script
$ pip install -e . -r requirements/dev.txt
```

* Optional: Install the pre-commit hooks.
```shell script
$ pre-commit install
```

### Start coding

* Create a branch to identify the issue you would like to work on. If you're submitting a bug or documentation fix, branch off of the latest ".x" branch.
```shell script
$ git fetch origin
$ git checkout -b your-branch-name origin/0.1.x
```

* If you're submitting a feature addition or change, branch off of the "develop" branch.
```shell script
$ git fetch origin
$ git checkout -b your-branch-name origin/develop
```

* Using your favorite editor, make your changes, [committing as you go](https://dont-be-afraid-to-commit.readthedocs.io/en/latest/git/commandlinegit.html#commit-your-changes).

* Include tests that cover any code changes you make. Make sure the test fails without your patch. Run the tests as described below.

* Push your commits to your fork on GitHub and [create a pull request](https://help.github.com/en/articles/creating-a-pull-request). Link to the issue being addressed with `fixes #123` in the pull request.
```shell script
$ git push --set-upstream fork your-branch-name
```

### Running the tests
Run the basic test suite with pytest.
```shell script
$ pytest -v
```
This runs the tests for the current environment, which is usually sufficient. CI will run the full suite when you submit your pull request.

You can run the full test suite with tox if you don't want to wait.
```shell script
$ tox
```

### Running test coverage
Generating a uncovered lines report may give a hint where to start contributing.
Run pytest using coverage to generate a report.
```shell script
$ pytest --cov=src --cov-report=term-missing
```
The report will be printed on screen.
More about [pytest-cov](https://github.com/pytest-dev/pytest-cov).
