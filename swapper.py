#!/usr/bin/env python3

"""
Creates an i3blocks block that switches text when you scroll over it.
Requres format=json

e.g. in i3blocks config
[swapper]
command=python3 PATH/TO/THIS/swapper.py 'echo 1' 'echo 2' 'echo 3' 'echo Boom!'
interval=10
"""

from i3blocks_helper import run, get_var, to_json
import sys
import os
from subprocess import CalledProcessError

CURRENT_VAR = "_swap_state"

# which line to display
current = int(get_var(CURRENT_VAR) or 0)

vars_for_subprocess = os.environ.copy()
if get_var("BLOCK_BUTTON") in ("4", "5"):
    # to stop sub-commands scrolling too
    del vars_for_subprocess["BLOCK_BUTTON"]


def check_scrolling():
    global current
    button = get_var("BLOCK_BUTTON")
    if button == "4":  # scroll up
        current += 1
    elif button == "5":  # scroll down
        current -= 1
    # Make sure result is still in the right range
    current %= len(sys.argv) - 1


if __name__ == "__main__":
    assert len(sys.argv) > 1
    check_scrolling()
    command = sys.argv[1:][current]
    try:
        # get first line of command output
        output = run(command, env=vars_for_subprocess).split("\n")[0]
    except CalledProcessError:
        output = "ERROR!"
    print(to_json(output, (CURRENT_VAR, current)))
