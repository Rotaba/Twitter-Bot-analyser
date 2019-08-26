#!/bin/bash

git rev-list --objects --all \
| git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' \
| sed -n 's/^blob //p' \
| sort --numeric-sort --key=2 \
| cut -c 1-12,41- \
| numfmt --field=2 --to=iec-i --suffix=B --padding=7 --round=nearest


# from https://stackoverflow.com/questions/10622179/how-to-find-identify-large-files-commits-in-git-history
#
# https://help.github.com/articles/removing-sensitive-data-from-a-repository/
#
# https://stackoverflow.com/questions/1072171/how-do-you-remove-an-invalid-remote-branch-reference-from-git
# git fetch -p
# It'll remove all your local branches which are remotely deleted.
