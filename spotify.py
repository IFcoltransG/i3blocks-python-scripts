#!/usr/bin/env python3

"""
i3blocks script for Spotify. Displays a colourful title and artist.
Left click to pause-play.
Middle click for previous song, right click for next song.
Scroll to change volume.
"""

from i3blocks_helper import colour, check_clicks, run
from subprocess import CalledProcessError

commands = {
    "1": "playerctl --player=spotify play-pause",
    "2": "playerctl --player=spotify previous",
    "3": "playerctl --player=spotify next",
    "4": "pactl set-sink-volume @DEFAULT_SINK@ +5%",
    "5": "pactl set-sink-volume @DEFAULT_SINK@ -5%",
}

check_clicks(commands)

try:
    title = run("playerctl --player=spotify metadata title")
    artist = run("playerctl --player=spotify metadata artist") or run("playerctl --player=spotify metadata album")
    status = run("playerctl --player=spotify status")
except CalledProcessError:
    print(colour("Spotless", "pink"))
else:
    # status one of "Playing", "Paused", "Stopped"
    if status == "Playing":
        main_colour = "cyan"
        accent_colour = "dark cyan"
    elif status == "Paused":
        main_colour = "dark cyan"
        accent_colour = "dark cyan"
    if status == "Stopped":
        print("Stopify")
    else:
        print(colour(title, main_colour), colour(artist, accent_colour))
