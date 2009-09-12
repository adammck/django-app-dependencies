#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


import depends


DATABASE_ENGINE = "sqlite3"
DATABASE_NAME   = "db.sqlite3"


INSTALLED_APPS =\
depends.build(
    "alpha",
    "echo"
)
