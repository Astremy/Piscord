<img src="https://github.com/Astremy/Piscord/blob/master/assets/Logo_Piscord.png" width="170" align="right" />

[![pypi](https://img.shields.io/pypi/v/piscord)][package]
[![docs](https://readthedocs.org/projects/piscord/badge/?version=latest&style=plastic)][documentation]
[![licence](https://img.shields.io/github/license/Astremy/Piscord)][licence]
![build](https://img.shields.io/github/workflow/status/Astremy/Piscord/Python package)
[![discord](https://img.shields.io/badge/chat-discord?logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2)][discord]

# Piscord

Piscord is a python framework to communicate with the Discord api.

In particular, it simplifies the creation of a bot that interacts with
a Web server.  
It thus allows to do much more easily various things like bot control
panels.

## Quickstart

Download and install piscord using `pip` (use `pip` instead of `pip3`
if the later is not found).

    $ pip3 install piscord

Write your first bot `mybot.py`.

    #!/usr/bin/env python3
    from piscord import Bot

    TOKEN = ...  # Put your discord token here
    bot = Bot(TOKEN)

    @bot.event
    def on_ready(ready):
            print(f"Bot {ready.user.name} connected")

    @bot.event
    def on_message(msg):
        if msg.content == "!ping":
	    msg.channel.send("Pong !")

    bot.run()

Launch it (use `python` or `py` instead of `python3` if the later is
not found)

    $ python3 mybot.py

Learn more in the online [documentation][tutorial]

## Meta

This project is primary developed and maintened by [Astremy][astremy-gh].

This project is licenced against the MIT licence, you are free to use,
modify and distribute it as long as we are cited. Please read the
[full licence][licence] for more informations.

## How to contribute

Thank you for your interrest in piscord, you can contribute the
standard way:

1) fork
2) create a new branch
3) do your changes
4) pass the tests and the sanity checker
5) rebase on our [master branch][master]
6) create a pull request

If you are fixing a bug, make sure an *issue* exists with clear steps
to reproduce the problem.

[pypi]: https://pypi.org/project/piscord/
[documentation]: https://piscord.readthedocs.io/en/latest/
[astremy-gh]: https://github.com/Astremy
[licence]: https://github.com/Astremy/Piscord/blob/master/LICENSE
[tutorial]: https://piscord.readthedocs.io/en/latest/tutorial.html
[master]: https://github.com/Astremy/Piscord/tree/master
[discord]: https://discord.com/invite/U9X7XzP
