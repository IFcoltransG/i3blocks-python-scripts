#!/usr/bin/env python3

"""
A helper script for writing i3blocks programs.

Example standalone use:

#in i3blocks config
[example]
command=python3 PATH/TO/THIS/FILE/i3blocks_helper.py echo Button!
_mouse_1_command=notify-send Clicked!
_mouse_2_command=notify-send Middle clicked!
_mouse_3_command=notify-send Right clicked!
_mouse_4_command=notify-send Scrolled up!
_mouse_6_command=notify-send Scrolled down!
interval=1
markup=none

Example library use:

#as a python file
from i3blocks_helper import check_clicks, run
from subprocess import CalledProcessError
commands = {
    "1": "notify-send Clicked!",
    "2": "notify-send Middle clicked!"
    "3": "you get the idea",
}
check_clicks(commands)
try:
    print(run("echo Button"))
except CalledProcessError:
    print("Error occured!")
"""

import os
import sys
import subprocess
import json

# environment variable to check for the main command to run
COMMAND_VAR = "_command"


def button_to_var(button):
    """
    Gets an environment variable name from a mouse button number.
    """
    return "_mouse_" + str(button) + "_command"


def get_var(name, default=""):
    """
    Gets the text of an environment variable, or default if it doesn't exist.
    """
    if name in os.environ:
        return os.environ[name]
    return default


def run(command, shell=True, suppress_error=False, **kwargs):
    """
    Returns the stdout of a shell command.
    Raises a subprocess.CalledProcessError if
    the command has a non-zero exit code.

    suppress_error: if set to true, non-zero exit codes will be ignored

    All other keyword arguments are passed to subprocess.check_output
    """
    try:
        result = subprocess.check_output(
            command, shell=shell, stderr=subprocess.DEVNULL, **kwargs
        )
    except subprocess.CalledProcessError as error:
        if suppress_error:
            result = error.output
        else:
            raise
    return result.decode("utf8").strip()


def check_clicks(commands=None):
    """
    Check for i3blocks clicks using the BLOCK_BUTTON environment variable,
    and runs an appropriate command from a dictionary passed in or from an
    environment variable.
    The dictionary should have string keys containing the appropriate digits,
    and any environment variables should match button_to_var() output.
    The button order, starting from "1", is: left mouse, middle mouse,
    right mouse, scroll up, scroll down.
    """
    button = get_var("BLOCK_BUTTON")
    if button:
        if commands is None:
            command_var = button_to_var(button)
            command = get_var(command_var)
        else:
            command = commands.get(button, "")
        if command:
            run(command)


def colour(text, colour):
    """
    Colours text.
    Requires markup=pango
    """
    if colour == "default":
        return text
    if colour == "empty":
        return ""
    if colour == "blank":
        return " " * len(text)
    return f"<span color='{colour}'>{text}</span>"


def to_json(text, *args, **kwargs):
    """
    Creates text that, when printed (with format=json in i3blocks config),
    will set environment variables in order to save state between runs.

    Pass it text for the program to display,
    followed by (variable_name, value) pairs to set environment variables for
    the next time the script is run.
    Alternatively, pass keyword arguments to
    set corresponding environment variables.

    e.g. print(to_json("Spam!", state=state))
    """
    kwargs["full_text"] = text
    kwargs.update(dict(args))
    return json.dumps(kwargs)


if __name__ == "__main__":
    check_clicks()
    if len(sys.argv) > 1:
        # take command from command line arguments if present
        print(run(sys.argv[1:], shell=False))
    else:
        # otherwise, take command from the environment variable
        print(run(get_var(COMMAND_VAR)))
