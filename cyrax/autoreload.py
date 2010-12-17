# Autoreloading launcher.
# Borrowed from Peter Hunt and the CherryPy project (http://www.cherrypy.org).
# Some taken from Ian Bicking's Paste (http://pythonpaste.org/).
#
# Borrowed from Django and adapted for Cyrax.
#
# Portions copyright (c) 2004, CherryPy Team (team@cherrypy.org)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright notice,
#       this list of conditions and the following disclaimer in the documentation
#       and/or other materials provided with the distribution.
#     * Neither the name of the CherryPy Team nor the names of its contributors
#       may be used to endorse or promote products derived from this software
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os, sys, time

import logging

try:
    import thread
except ImportError:
    import dummy_thread as thread

# This import does nothing, but it's necessary to avoid some race conditions
# in the threading module. See http://code.djangoproject.com/ticket/2330 .
try:
    import threading
except ImportError:
    pass

logger = logging.getLogger(__name__)

RUN_RELOADER = True

_mtimes = {}
_win = (sys.platform == "win32")


def normpath(p):
    return os.path.normpath(os.path.abspath(p))


def _should_ignore(path, exclude):
    root, subpart = os.path.split(path)
    if root == path:
        # reached the /
        return False

    for exc in exclude:
        if normpath(path) == normpath(exc):
            return True

    return _should_ignore(root, exclude)


def _get_mtime(path):
    try:
        stat = os.stat(path)
    except OSError:
        return None
    mtime = stat.st_mtime
    if _win:
        mtime -= stat.st_ctime
    return mtime


def source_changed(path, exclude=None):
    global _mtimes
    if exclude is None:
        exclude = []
    for root, dirs, files in os.walk(path):
        if _should_ignore(root, exclude):
            continue
        for filename in files:
            filepath = os.path.join(root, filename)
            mtime = _get_mtime(filepath)
            if filepath not in _mtimes:
                _mtimes[filepath] = mtime
                continue
            if mtime != _mtimes[filepath]:
                logger.debug('File %r is changed', filepath)
                _mtimes = {}
                return True
    return False


def reloader_thread(source, dest):
    while RUN_RELOADER:
        if source_changed(source, exclude=[dest]):
            logger.info('Source changed, restarting')
            sys.exit(3) # force reload
        time.sleep(1)


def restart_with_reloader():
    while True:
        args = [sys.executable] + sys.argv
        if sys.platform == "win32":
            args = ['"%s"' % arg for arg in args]
        new_environ = os.environ.copy()
        new_environ["RUN_MAIN"] = 'true'
        exit_code = os.spawnve(os.P_WAIT, sys.executable, args, new_environ)
        if exit_code != 3:
            return exit_code


def reloader(main_func, args, kwargs):
    if os.environ.get("RUN_MAIN") == "true":
        thread.start_new_thread(main_func, args, kwargs)
        try:
            reloader_thread(kwargs['source'], kwargs['dest'])
        except KeyboardInterrupt:
            pass
    else:
        try:
            sys.exit(restart_with_reloader())
        except KeyboardInterrupt:
            pass


def main(main_func, args=None, kwargs=None):
    if args is None:
        args = ()
    if kwargs is None:
        kwargs = {}
    reloader(main_func, args, kwargs)

