# Updates List

Here is the list of all the updates that I made on this template.

### Version 5.1 (12 September 2022)

* Added the `help` command once again
* Created a group for the `warning` command, has following sub-commands:
  * `add` - Adds a warning to the user
  * `remove` - Removes a warning from the user
  * `list` - Lists all the warnings of the user

### Version 5.0 (20 August 2022)

> ⚠️ **Moved to discord.py 2.0 as it is now officially released**

* Added `warnings` command that will show you all the warnings a user has
* Moved the blacklist to `sqlite3` database
* Now using **Hybrid Commands**, both prefix and slash commands will get created
* When using the `warn` command, the warning will also be added in a new `sqlite3` database

### Version 4.1.1 (18 July 2022)

* Fixed the custom checks not being sent in the channels correctly

### Version 4.1 (09 January 2022)

* Added the `hackban` command
* Separated slash commands and normal commands so that you remove one of them more easily
    * Moved normal commands in [`cogs/normal`](cogs/normal)
    * Moved slash commands in [`cogs/slash`](cogs/slash)

### Version 4.0.1

* Fixed some *weird* code

### Version 4.0

* Now using [`disnake`](https://docs.disnake.dev)
* Added a command that uses buttons *(coinflip)*
* Added a command that uses selection dropdown *(rps)*
* **Every** command is now in slash command **and** normal command (old way with prefix)
    * Make sure to **enable the message intents** for normal commands as it's now a privileged intent.
    * The **slash command** is **above**, the **normal command** is **below**

### Version  3.1.1

* Fixed `TypeError: 'NoneType' object is not iterable` for prefix -> Python 3.10

### Version 3.1

* Added a `@checks.is_owner` check which raises a `UserNotOwner` exception
* Added a `@checks.not_blacklisted` check which raises a `UserBlacklisted` exception
* Using checks instead of same code for every command
* Various code cleanup

### Version 3.0

**Now using slash commands**

### Version 2.8

* Blacklisted users are now **saved** in the file
* Moved config file to JSON
* Moved the blacklist in a separate file (`blacklist.json`)
* The colors are no longer saved in the config file

### Version 2.7

* Added a check for `commands.MissingRequiredArgument` in the error handler
* Added a disclaimer section in the [README](README.md) file
* Added the latency of the bot in the `ping` command
* Created the [TODO list](TODO.md) file
* Fixed some error embeds having success (green) colors
* Removed an unnecessary `self.bot.logout()` statement
* Removed the `dick` command, as I want to keep this template safe for work
* Renamed the names of the arguments in some commands
* The bot now **tries** to send an embed in the private message of the command author for the `invite` and `server`
  commands, if this was not successful it will be sent in the channel

### Version 2.6

* Added new `dailyfact` command that gives a random fact every day, using cool down
* Fixed some typos in [README.md](README.md)
* Remade the `on_command_error` event for `CommandOnCooldown`

### Version 2.5

* Code reformat
* Rewrote the status task
* Now using the `has_permissions` decorator for user permissions
* Using `.yaml` instead of `.py` file for config

### Version 2.4.3

* Fixed intents for `serverinfo` command

### Version 2.4.2

* Blacklisted users are being ignored when executing a command

### Version 2.4.1

* Added config import to moderation cog

### Version 2.4

* Added some fun commands
* Colors are saved in the [config file](config.json) for easier usage
* Cogs are now being loaded automatically
* Fixed some typos

### Version 2.3

* Made the kick command actually kick
* Added a template cog to create cogs easily

### Version 2.2

* Fixed the purge command
* Made the error embeds actually red...

### Version 2.1

* Made the help command dynamic
* Added a small description to all commands
* Added intents when creating the bot

### Version 2.0

* Added cogs
* Added f-strings and removed `.format()`
* Created [config file](config.json) for easier setup

### Version 1.2

* Added blacklist command
* Removed commands cool down