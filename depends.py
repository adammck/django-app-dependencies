#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


import sys, traceback


class DependencyError(Exception):
    pass


class DependencyImportError(ImportError):
    pass


def _try_import(module_name):
    """Attempts to import and return *module_name*, returning None if an
       ImportError was raised. Unlike the standard try/except approach to
       optional imports, this method jumps through some hoops to avoid
       catching ImportErrors raised from within *module_name*."""

    try:
        __import__(module_name)
        return sys.modules[module_name]

    except ImportError:

        # extract a backtrace, so we can find out where the exception was
        # raised from. if there is a NEXT frame, it means that the import
        # statement succeeded, but an ImportError was raised from _within_
        # the imported module. we must allow this error to propagate, to
        # avoid silently masking it with this optional import
        traceback = sys.exc_info()[2]
        if traceback.tb_next:
            raise

        # otherwise, the exception was raised
        # from this scope. *module_name* couldn't
        # be imported,which isn't such a big deal
        return None


def _dependencies(app_name):
    """Returns the module names of the apps that *app_name* claims to depend
       upon, or an empty list if it has no dependencies (ie, the app does not
       export an iterable REQUIRED_APPS).

       Raises DependencyImportError (which is a subclass of ImportError, to be
       handled easily) if *app_name* does not exist. Any exception raised from
       within the module during import is allowed to propagate, to avoid masking
       errors which are unrelated to dependency management."""

    # try to import the app
    module = _try_import(app_name)
    if module is None:
        raise(DependencyImportError(
            "No module named %s" %
            (app_name)))

    # return the required apps unchecked, since this
    # function will probably be re-called for each of
    # them, which will import their module (aboe)
    if hasattr(module, "REQUIRED_APPS"):
        return module.REQUIRED_APPS

    # default to no dependencies
    return []


def build(*app_names):
    apps = []

    def _build(app_name):
        for x in _dependencies(app_name):

            # if this dependency has not already been
            # added, recurse to find its own dependencies
            if x not in apps:
                _build(x)

        # add the app itself _last_, to ensure that
        # its dependencies are imported before it is
        apps.append(app_name)

    # find all of the dependencies of the named
    # apps, to build the final INSTALLED_APPS
    for app_name in app_names:
        if app_name not in apps:
            _build(app_name)

    return apps
