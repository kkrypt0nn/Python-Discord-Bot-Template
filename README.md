# Python Discord Bot Template
[![Python Versions](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-orange)](https://github.com/kkrypt0nn/Python-Discord-Bot-Template)  [![Project Version](https://img.shields.io/badge/version-v2.0-blue)](https://github.com/kkrypt0nn/Python-Discord-Bot-Template)

This repository is a template that everyone can use for the start of their discord bot.

When I first started creating my discord bot it took me a while to get everything setup and working with cogs and more. I would've been happy if there were any template existing. But there wasn't any existing template. That's why I decided to create my own template to let <b>you</b> guys create your discord bot in an easy way.

## Authors
* **[Krypton (@kkrypt0nn)](https://github.com/kkrypt0nn)** - The only and one developer

## Support

If you need some help for something, do not hesitate to join my discord server [here](https://discord.gg/xkWRGBY).

All the updates of the template are available [here](UPDATES.md).

## How to download it

This repository is now a template, on the top left you can simple click on "**Use this template**" to create a GitHub repository based on this template.

Alternatively you can do the following:
* Clone/Download the repository
    * To clone it and get the updates you can definitely use the command
    `git clone`
* Create a discord bot [here](https://discord.com/developers/applications)
* Get your bot token
* Invite your bot on servers using the following invite:
https://discordapp.com/oauth2/authorize?&client_id=YOUR_APPLICATION_ID_HERE&scope=bot&permissions=8 (Replace `YOUR_APPLICATION_ID_HERE` with the application ID)

## How to setup

To setup the bot I made it as simple as possible. I now created a [config.py](config.py) file where you can put the needed things to edit.

Here is an explanation of what everything is:

| Variable          | What it is                                                            |
| ------------------| ----------------------------------------------------------------------|
| BOT_PREFIX        | The prefix(es) of your bot                                            |
| TOKEN             | The token of your bot                                                 |
| APPLICATION_ID    | The application ID of your bot                                        |
| OWNERS            | The user ID of all the bot owners                                     |
| BLACKLIST         | The user ID of all the users who can't use the bot                    |
| STARTUP_COGS      | The cogs that should be automatically loaded when you start the bot   |

## How to start

To start the bot you simply need to launch, either your terminal (Linux, Mac & Windows) or your Command Prompt (Windows).

If you have multiple versions of python installed (2.x and 3.x) then you will need to use the following command:
```
python3 bot.py
```
or eventually
```
python3.8 bot.py
```
<br>

If you have just installed python today, then you just need to use the following command:
```
python bot.py
```

## Built With

* [Python 3.8](https://www.python.org/)

## Issues or Questions

If you have any issues or questions of how to code a specific command, make sure to post them [here](https://github.com/kkrypt0nn/Python-Discord-Bot-Template/issues). I will take time to answer and help you.

## Versioning

We use [SemVer](http://semver.org) for versioning. For the versions available, see the [tags on this repository](https://github.com/kkrypt0nn/Python-Discord-Bot-Template/tags). 

## Bots who used this template

*DM Krypton#2188 to get yourself in this list*

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE.md](LICENSE.md) file for details
