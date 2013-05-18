glint
=====

Lint checking on pull requests.

Currently the following file types are supported:
- Python - using [pylint](http://www.pylint.org/)
- Javascript - using [jshint](http://www.jshint.com/)

To setup glint, run the following commands:

```
git clone git@github.com:cam-stitt/glint.git

cd glint

pip install -r requirements.txt

npm install -g jshint
```

Run the following command to comment on the commit:
```
python glint.py --repo_name="OWNER/REPO" --pull=PULL_NUM --github-username="USERNAME" --github-password="PASSWORD"
```
