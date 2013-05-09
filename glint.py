import logging
import json
import tempfile
import urllib2
import re
import os

import envoy
import requests
from github import Github

logging.basicConfig()
log = logging.getLogger(__name__)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
            description="Posts static analysis results to github.")
    parser.add_argument(
        '--repo_name', required=True,
        help="Github repository name in owner/repo format")
    parser.add_argument('--pull', required=True,
                         help="The pull request number to run the lint on.")
    parser.add_argument(
        '--filenames', nargs="+",
        help="filenames you want static analysis to be limited to.")
    parser.add_argument(
        '--debug', action='store_true',
        help="Will dump debugging output and won't clean up after itself.")
    parser.add_argument(
        '--github-username',
        required=True,
        help='Github user to post comments as.')
    parser.add_argument(
        '--github-password',
        required=True,
        help='Github password for the above user.')

    args = parser.parse_args()
    repo_name = args.repo_name
    pull = int(args.pull)

    credentials = {
        'user': args.github_username,
        'password': args.github_password}

    g = Github(credentials['user'], credentials['password'])

    repo = g.get_repo(repo_name)

    pull = repo.get_pull(pull)

    files = pull.get_files()

    import pdb; pdb.set_trace()
    for file in files:
        fname = re.findall(r'[^\/]+$', file.filename)
        if len(fname) <= 0:
            #TODO(cam-stitt): Error
            continue
        fname = fname[0]
        req = requests.get(file.raw_url,
            auth=(credentials['user'], credentials['password']))
        if req.status_code != 200:
            continue
        tf = open("{0}/{1}".format(tempfile.gettempdir(), fname), "w+")
        tf.write(req.text)
        tf.close()
        cmd = 'pylint {0} --output-format=parseable'.format(tf.name)
        result = envoy.run(cmd)
        
        for line in result.std_out.split("\n{0}".format(tf.name)):
            if len(line) == 0:
                continue
            filename, line_num, error = line.split(':', 2)
            
            to_return[filename][line_num].append(error)
        
        os.remove(tf.name)
