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

Run the following command glint the pull request:
```
python glint.py --repo_name="OWNER/REPO" --pull=PULL_NUM --github-username="USERNAME" --github-password="PASSWORD"
```

Optionally you can glint on a comma seperated list of files:

```
--filenames="file1.txt,file2.txt"
```