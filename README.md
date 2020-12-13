# i3blocks helper scripts

Python scripts for convenience when working with [i3blocks](https://github.com/vivien/i3blocks).

## `i3blocks_helper.py`
This is the important file. It has innumerable utility functions, and is also a self-contained i3block for easily adding mouse support to an otherwise inert block. See the docstring at the top of the file for details.

## `swapper.py`
This is for making those blocks that you can scroll over that you might be used to from the likes of py3status. That way you can unclutter your bar but still have all of the information available in the different modes you scroll through. Again, see the docstring for details.

## `chain.py`
Simple tool for concatenating multiple commands' outputs, complete with labels. The main reason you might use this is with the swapper script above, so that each mode can have multiple components. I doubt I have to tell you a third time that the info is in the docstring.

## `spotify.py`
This is a Spotify script tailored to my preferences, but it should show you how easy it is to create your own i3blocks script. If you want, you can swap out all of the shell commands, and replace the last clump from `try:` onwards with `print(run("YOUR SHELL COMMAND HERE"))`. You'll have made your very own interactive i3blocks script, with minimal Python.

## Installation
If you pester me I'll likely put these on pypi. Otherwise, just clone the repo and start mangling it to suit your ends.
