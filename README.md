# Python Discord Bot Template

<p align="center">
  <a href="https://discord.gg/mTBrXyWxAF"><img src="https://img.shields.io/discord/739934735387721768?logo=discord"></a>
  <a href="https://github.com/kkrypt0nn/Python-Discord-Bot-Template/releases"><img src="https://img.shields.io/github/v/release/kkrypt0nn/Python-Discord-Bot-Template"></a>
  <a href="https://github.com/kkrypt0nn/Python-Discord-Bot-Template/commits/main"><img src="https://img.shields.io/github/last-commit/kkrypt0nn/Python-Discord-Bot-Template"></a>
  <a href="https://github.com/kkrypt0nn/Python-Discord-Bot-Template/blob/main/LICENSE.md"><img src="https://img.shields.io/github/license/kkrypt0nn/Python-Discord-Bot-Template"></a>
  <a href="https://github.com/kkrypt0nn/Python-Discord-Bot-Template"><img src="https://img.shields.io/github/languages/code-size/kkrypt0nn/Python-Discord-Bot-Template"></a>
  <a href="https://conventionalcommits.org/en/v1.0.0/"><img src="https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

Welcome to the Discord Bot Template, a resource designed to streamline the process of creating your own Discord bot.

When embarking on my journey to create a Discord bot, I faced a steep learning curve setting up cogs and other essential components. I wished for a comprehensive template, but none existed. As a result, I developed this template to empower **you** to easily craft your own Discord bot.

Please note that while this template may not be the ultimate solution, it serves as an excellent starting point for learning how to utilize discord.py effectively and for swiftly building your custom bot.

## Usage Guidelines

If you intend to use this template for developing your own bot or creating another template, there are a few important conditions to meet:

- **Maintain Credits**: Ensure that you retain the appropriate credits and provide a link to this repository in all files that contain my code.
- **Preserve License**: Keep the same license for any unchanged code.

Refer to the [license file](https://github.com/kkrypt0nn/Python-Discord-Bot-Template/blob/master/LICENSE.md) for detailed information. Please be aware that I reserve the right to remove any repository that does not adhere to these requirements.

---

## Getting Started

To use this template, you can either:

1. **Use This Template**: Click the "Use this template" button to create your GitHub repository based on this template.
2. **Clone/Download**: Clone or download this repository to your local machine.

### Prerequisites

Before setting up your bot, you'll need:

- A basic knowledge of Python.
- A Discord bot application. You can create one [here](https://discord.com/developers/applications).
- Invite your bot on servers using the following invite:
  https://discord.com/oauth2/authorize?&client_id=YOUR_APPLICATION_ID_HERE&scope=bot+applications.commands&permissions=PERMISSIONS (
  Replace `YOUR_APPLICATION_ID_HERE` with the application ID and replace `PERMISSIONS` with the required permissions
  your bot needs that it can be get at the bottom of a this
  page https://discord.com/developers/applications/YOUR_APPLICATION_ID_HERE/bot)

## Setup

1. **Configure `config.json`**:
   - Set your bot's prefix and invite link in the `config.json` file.
   - Here is an explanation of what everything is:
    
      
      | Variable                  | What it is                                     |
      | ------------------------- | ---------------------------------------------- |
      | YOUR_BOT_PREFIX_HERE      | The prefix you want to use for normal commands |
      | YOUR_BOT_INVITE_LINK_HERE | The link to invite the bot                     |
      

2. **Set the Bot Token**:
   - Create an environment variable named `TOKEN` or edit the `.env` file with your bot token.
   - To set up the token you will have to either make use of the [`.env.example`](.env.example) file, either copy or rename it to `.env` and replace `YOUR_BOT_TOKEN_HERE` with your bot's token.

3. **Install Requirements**:
   - Run `python -m pip install -r requirements.txt` to install the required packages.

4. **Start the Bot**:
   - Run `python bot.py` to launch your bot.

## Support

If you need help or have questions, feel free to join our [Discord server](https://discord.com/invite/mTBrXyWxAF) for assistance.


## Versioning

We use [SemVer](https://semver.org/) for versioning. Check the repository's tags for available versions.

## Built With

- Python 3.11.5

## Disclaimer

Slash commands can take some time to get registered globally, so if you want to test a command you should use
the `@app_commands.guilds()` decorator so that it gets registered instantly. Example:

```py
@commands.hybrid_command(
  name="command",
  description="Command description",
)
@app_commands.guilds(discord.Object(id=GUILD_ID)) # Place your guild ID here
```

When using the template you confirm that you have read the [license](LICENSE.md) and comprehend that I can take down
your repository if you do not meet these requirements.

---

**Note:** Slash commands may take time to get registered globally. Consider using `@app_commands.guilds()` decorator for testing.

Happy bot development!
## License

This project is licensed under the Apache License 2.0 - see the [LICENSE.md](LICENSE.md) file for details
