#!/usr/bin/env python3

"""
i3blocks script for playerctl. Displays a colourful title and artist.
Left click to pause-play.
Middle click for previous song, right click for next song.
Scroll to change volume.
"""

from i3blocks_helper import colour, check_clicks, run, pango
from subprocess import CalledProcessError

commands = {
    "1": "playerctl play-pause",
    "2": "playerctl previous",
    "3": "playerctl next",
    "4": "pactl set-sink-volume @DEFAULT_SINK@ +5%",
    "5": "pactl set-sink-volume @DEFAULT_SINK@ -5%",
}

check_clicks(commands)

try:
    title = run("playerctl metadata title").strip()
    artist = (
        run("playerctl metadata artist") or
        run("playerctl metadata album")
    ).strip()
    status = run("playerctl status")
except CalledProcessError:
    print(colour("Radio Silence", "pink"))
else:
    # shorten titles like 'Song (version version)' or 'Song - Acoustic'
    patterns = {" (", " {", " [", " |", " -", " featuring", " feat."}
    cutoffs = (title.find(pattern) for pattern in patterns if pattern in title)
    cutoff = min(cutoffs, default=None)
    if cutoff:
        title = title[:cutoff].strip()
        # title will be non-empty
    
    # status one of "Playing", "Paused", "Stopped"
    if status == "Playing":
        main_colour = "cyan"
        accent_colour = "dark cyan"
    elif status == "Paused":
        main_colour = "dark cyan"
        accent_colour = "dark cyan"
    
    if status != "Playing":
        print("Over")
    else:
        print(
            colour(pango(title)[:50], main_colour),
            colour(pango(artist)[:30], accent_colour)
        )
