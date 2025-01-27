#!/bin/bash

VERSION=$(cat digitalocean_manager/__version__.py | sed -n "s/^__version__ = ['\"]\(.*\)['\"]/\1/p")

if [ -z "$VERSION" ]; then
    echo "Version not found in __version__.py"
    exit 1
fi

echo git tag -a v$VERSION -m "Release version $VERSION"
echo git push origin v$VERSION
