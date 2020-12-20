"""
*****************************
Communication Module Template
*****************************

:Author: Michael Murton
"""
# Copyright (c) 2019-2020 MQTTany contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import typing as t
from collections import OrderedDict

import logger

log = logger.get_logger("comm_pkg_template")
CONFIG: t.Dict[str, t.Any] = {}

# This queue is used to request that MQTTany exit. If a fatal error is encountered put
# a plain string on this queue using `put_nowait()` that will fit in this log entry
# such as `__name__`: "Received exit request from {}"
# An error that results in the module not being able to transmit messages, such as being
# unable to connect to the server, is considered fatal. If a module is unable to transmit
# it must request that MQTTany exit, otherwise it's transmit queue would overflow.
core_queue: "mproc.Queue[str]" = None  # type: ignore

# If the module can receive messages it must have the `receive_queue` attribute.
# A listener thread should be spawned in the `start` function and should use the `put_nowait()`
# method on the queue to put `BusMessage` objects in this queue
# omit this if module is transmit only
receive_queue: "mproc.Queue[BusMessage]" = None  # type: ignore

# Configuration keys, best to define them here so they can be changed easily
CONF_KEY_STRING = "string"
CONF_KEY_FIXED_TYPE = "fixed type"
CONF_KEY_SELECTION = "selection"
CONF_KEY_SUBSECTION = "sub section"

# Configuration layout for `parse_config`
# it should be an OrderedDict of `(key, {})`
CONF_OPTIONS: t.MutableMapping[str, t.Dict[str, t.Any]] = OrderedDict(
    [
        (  # an empty dict means any value is valid and option is required
            CONF_KEY_STRING,
            {},
        ),
        (  # fixed type options should provide a type to compare with
            CONF_KEY_FIXED_TYPE,
            {
                # if a `default` is given the option is assumed to be optional
                "type": int,
                "default": 200,
                "secret": True,  # This will cause the value to appear as *'s in the log
            },
        ),
        (  # subsections are also possible
            CONF_KEY_SUBSECTION,
            {
                # they must have type set to "section"
                "type": "section",
                # if a subsection is optional you must specify this, if this
                # is omitted the subsection is assumed to be required.
                "required": False,
                # conditions allows you to match a key at the same level (where CONF_KEY_SUBSECTION
                # is in this example) to a specific value. Must provide a list of tuples
                # where the first element is the key and the second is the value to match.
                # If any of the conditions match the option will be parsed. This can be
                # used ex. to have required sections only if an option is set to a specific
                # value. Can also be used on regular options.
                "conditions": [(CONF_KEY_FIXED_TYPE, 200)],
                CONF_KEY_SELECTION: {
                    # you can limit the possible values by providing a list or dict of
                    # possibilities. The config will be invalid if the value is not in
                    # "selection". If "selection" is a dict then the key's value will be
                    # returned, not the key.
                    "default": None,
                    "selection": {"option 1": 1, "option 2": 2},
                },
            },
        ),
        (  # regex pattern sections can also be used, their key must be "regex:{pattern}"
            # when using regex sections that may match other keys they should be last
            # and CONF_OPTIONS
            "regex:pattern",
            {"type": "section"},
        ),
    ]
)
