glint
=====

Lint checking on pull requests.

Currently the following file types are supported:
- Python - using [pylint](http://www.pylint.org/)
- Javascript - using [jshint](http://www.jshint.com/)

Run the following command to comment on the commit:
```
python glint.py --repo_name="OWNER/REPO" --pull=PULL_NUM --github-username="USERNAME" --github-password="PASSWORD"
```
