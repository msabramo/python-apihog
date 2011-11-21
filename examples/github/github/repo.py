#!/usr/bin/env python

import sys

from apihog import resource


class Repo(resource.Resource):
    BASE_URL = 'https://api.github.com'

    # Get single repo
    URI = '/repos/:user/:repo'

    # Get repos belonging to a user
    # URI = '/users/:user/repos'


if __name__ == '__main__':
    (_program, user, repo) = sys.argv

    repo = Repo.objects.get(user=user, repo=repo)

    print(repo)
