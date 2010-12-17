# -*- coding: utf-8 -*-
"""
    cyrax.events
    ~~~~~~~~~~~~~~~

    :copyright: 2007-2008 by Armin Ronacher as glashammer.utils.events
    :copyright: 2009 by Alexander Solovyov
    :license: MIT
"""

import logging
from collections import deque

logger = logging.getLogger(__name__)
# `events` global is defined at the end


class EventManager(object):
    """Helper class that handles event listeners and event emitting.
    """

    def __init__(self):
        self._listeners = {}
        self._last_listener = 0

    def connect(self, event, callback, prepend=False):
        """Connect a callback to an event.

        If `prepend` is True, prepend callback to a queue of callbacks.
        """
        listener_id = self._last_listener
        event = intern(event)

        if event not in self._listeners:
            self._listeners[event] = deque([callback])
        elif prepend:
            self._listeners[event].appendleft(callback)
        else:
            self._listeners[event].append(callback)

        self._last_listener += 1
        return listener_id

    def emit(self, event, *args, **kwargs):
        """Emit a event and return a `EventResult` instance."""
        if event != 'log':
            logger.debug('Emit: %s (%s)' % (event, ', '.join(map(repr, args))))
        return [cb(*args, **kwargs) for cb in self.iter(event)]

    def iter(self, event):
        """Return an iterator for all listeners of a given name."""
        if event not in self._listeners:
            return iter(())
        return iter(self._listeners[event])


events = EventManager()
