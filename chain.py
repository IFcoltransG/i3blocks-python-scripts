#!/usr/bin/env python3

"""
An i3blocks helper for concatenating the output of multiple commands.
For each command you want to concatenate, pass a label then a command as
command line arguments, in that order.

e.g. in i3blocks config
[memory]
command=python3 PATH/TO/THIS/chain.py 'MEM: ' ~/.config/i3blocks/memory/memory 'SWAP: ' 'instance=swap ~/.config/i3blocks/memory/memory'
interval=10
"""

from i3blocks_helper import run, colour
import sys
from subprocess import CalledProcessError


def chain(labelled_commands, error_colour="red"):
    for label, command in labelled_commands:
        try:
            output = run(command).split("\n")[0]
        except CalledProcessError as result:
            if result.output:
                output = colour(
                    result.output.decode("utf8").split("\n")[0], error_colour
                )
            else:
                output = f"ERROR {result.returncode}!"
        yield label + output


if __name__ == "__main__":
    commands = sys.argv[2::2]
    labels = sys.argv[1::2]
    outputs = chain(zip(labels, commands))
    print(*outputs)
