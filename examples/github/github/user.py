#!/usr/bin/env python

import sys

from apihog import resource

from repo import Repo


class User(resource.Resource):
    BASE_URL = 'https://api.github.com'
    URI = '/users/:user'

    # Fields
    user = resource.TextField('user', primary_key=True)

    # Associations
    repos = resource.ZeroOrMore(Repo)


if __name__ == '__main__':
    user = sys.argv[1]

    user = User.objects.get(user=user)

    print(user)
    print('\n# of repos: %d' % len(user.repos.all()))
