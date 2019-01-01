#!/usr/bin/env python3

import argparse
import datetime
import json
import os
import re
import sys
from subprocess import check_output

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--json-output",
                    help="JSON output file", default="build.json")
parser.add_argument("-t", "--tag-output",
                    help="TAG output file", default="tag.txt")
parser.add_argument("-v", "--version-output",
                    help="Version output file", default="version.txt")
args = parser.parse_args()


def cmd_output(cmd):
    return check_output(cmd, shell=True).decode('utf-8').strip()


with open("package.json") as f:
    package_json = json.load(f)

# Getting the branch from the CI or local repo
if os.environ.get('CI_COMMIT_BRANCH'):  # drone
    git_branch = os.environ.get('CI_COMMIT_BRANCH')
elif os.environ.get('CIRCLE_BRANCH'):  # circleci
    git_branch = os.environ.get('CIRCLE_BRANCH')
else:
    git_branch = cmd_output("git branch | grep \\* | cut -d ' ' -f2")
git_branch_clean = re.sub('\\W+', '-', git_branch).lower()

# Getting the tag from the CI or local repo
if os.environ.get('CI_TAG'):  # drone
    git_tag = os.environ.get('CI_TAG')
elif os.environ.get('CIRCLE_TAG'):  # circleci
    git_tag = os.environ.get('CIRCLE_TAG')
else:
    git_tag = cmd_output("git tag --points-at HEAD")

git_hash = cmd_output("git show -s --format=%h")
git_date = cmd_output("git show --quiet --format='%ci'")[0:16]

git_date_short = git_date.replace('-', '').replace(' ', '-').replace(':', '')

print("branch: %s, hash: %s, date: %s, tag: %s" %
      (git_branch, git_hash, git_date_short, git_tag))

core_version = package_json['version']

if git_tag:
    git_target_tag = str('v' + core_version)
    if git_target_tag != git_tag:
        sys.exit("Boy you really messed up! tag=%s version=%s" %
                 (git_tag, core_version))
    version_full = core_version
else:
    version_full = "%s-%s-%s-%s" % (core_version,
                                    git_date_short, git_hash, git_branch_clean)

print("version: %s" % version_full)

build_info = {
    'version': version_full,
    'git_hash': git_hash,
    'git_date': git_date_short,
    'git_branch': git_branch,
    'build_date': datetime.datetime.utcnow().isoformat(),
}

if git_tag:
    build_info['git_tag'] = git_tag
    with open(args.tag_output, 'w') as f:
        f.write(git_tag)

if args.json_output:  # Always set for now
    with open(args.json_output, 'w') as f:
        f.write(json.dumps(build_info))

if args.version_output:  # Always set for now
    with open(args.version_output, 'w') as f:
        f.write(version_full)
