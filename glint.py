import logging
import json
import tempfile
import urllib2
import re
import os
import mimetypes

import envoy
import requests
from github import Github

logging.basicConfig()
log = logging.getLogger(__name__)

ACCEPTABLE_TYPES_CHOICES = {
    u'text/x-python': u'python',
    u'application/javascript': u'javascript'
}

ACCEPTABLE_TYPES = ACCEPTABLE_TYPES_CHOICES.keys()


def create_comment(commit, body, filename, line_num):
    print body
    commit.create_comment(
        body=body,
        path=filename,
        line=int(line_num))


def do_pylint(fle, temp_file, pull, commit):
    filename = fle.filename
    cmd = u'flake8 {0}'.format(temp_file.name)
    result = envoy.run(cmd)

    newline_stripped = result.std_out.replace(u'\n', u'')
    for line in newline_stripped.split(u"{0}/".format(os.path.dirname(temp_file.name))):
        if len(line) == 0:
            continue
        filename, line_num, column, error = line.split(u':', 3)
        
        line_link = u'{0}#L{1}'.format(fle.blob_url, line_num)
        
        commit_body = u'Line [{0}]({1}): {2}'.format(line_num, line_link, 
            error.strip())
        
        create_comment(
            commit,
            commit_body,
            filename,
            line_num)


def do_jshint(fle, temp_file, pull, commit):
    import pdb; pdb.set_trace()
    filename = fle.filename
    cmd = u'jshint --reporter=reporter.js {0}'.format(temp_file.name)
    result = envoy.run(cmd)

    newline_stripped = result.std_out.replace(u'\n', u'')

    for line in newline_stripped.split(u"{0}/".format(os.path.dirname(temp_file.name))):
        if len(line) == 0:
            continue
        filename, line_num, column, error = line.split(u':', 3)

        line_link = u'{0}#L{1}'.format(fle.blob_url, line_num)

        commit_body = u'Line [{0}]({1}): {2}'.format(line_num, line_link,
            error.strip())
            
        create_comment(
            commit,
            commit_body,
            filename,
            line_num)


def do_lint(g, repo_name, pull_number, credentials, filenames):
    repo = g.get_repo(repo_name)

    pull = repo.get_pull(pull_number)

    commit = repo.get_commit(pull.head.sha)

    files = pull.get_files()

    for fle in files:
        fname = re.findall(r'[^\/]+$', fle.filename)
        if len(fname) <= 0:
            continue
            
        block_list = re.findall(u'@@ -\d+,\d+ \+\d+,\d+ @@', fle.patch)
        
        fname = fname[0]
        if fname not in filenames:
            continue

        req = requests.get(fle.raw_url,
                           auth=(credentials[u'user'], credentials[u'password']))
        if req.status_code != 200:
            continue
        temp_file = open(u"{0}/{1}".format(tempfile.gettempdir(), fname), u"w+")
        temp_file.write(req.text)
        temp_file.close()

        file_type = mimetypes.guess_type(temp_file.name)

        if unicode(file_type[0]) in ACCEPTABLE_TYPES:
            name = ACCEPTABLE_TYPES_CHOICES[file_type[0]]
            if name == 'python':
                do_pylint(fle, temp_file, pull, commit)
            elif name == 'javascript':
                do_jshint(fle, temp_file, pull, commit)

        os.remove(temp_file.name)


if __name__ == u'__main__':
    """
    python glint.py --repo_name="cam-stitt/glint" --pull=2 --github-username="secret" --github-password="squirrel"
    """
    import argparse
    parser = argparse.ArgumentParser(
            description=u"Posts static analysis results to github.")
    parser.add_argument(
        u'--repo_name', required=True,
        help=u"Github repository name in owner/repo format")
    parser.add_argument(u'--pull', required=True,
                         help=u"The pull request number to run the lint on.")
    parser.add_argument(
        u'--filenames',
        help=u"filenames you want static analysis to be limited to.")
    parser.add_argument(
        u'--debug', action=u'store_true',
        help=u"Will dump debugging output and won't clean up after itself.")
    parser.add_argument(
        u'--github-username',
        required=True,
        help=u'Github user to post comments as.')
    parser.add_argument(
        u'--github-password',
        required=True,
        help=u'Github password for the above user.')

    args = parser.parse_args()
    repo_name = args.repo_name
    pull_number = int(args.pull)
    if args.filenames:
        filenames = unicode(args.filenames).split(',')

    credentials = {
        u'user': args.github_username,
        u'password': args.github_password}

    g = Github(credentials[u'user'], credentials[u'password'])

    do_lint(g, repo_name, pull_number, credentials, filenames)
