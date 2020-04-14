""""
Copyright © Krypton 2019 - https://github.com/kkrypt0nn
Description:
This is a template to create your own discord bot in python.

Version: 1.2
"""

import discord
import asyncio
import aiohttp
import json
from discord.ext.commands import Bot
from random import randint
from discord.ext import commands
from platform import python_version
import os
import platform

BOT_PREFIX = ('BOT_PREFIX')
TOKEN = 'YOUR_BOT_TOKEN'
OWNERS = [123456789, 123456789]
BLACKLIST = []
client = Bot(command_prefix=BOT_PREFIX)

async def status_task():
	while True:
		await client.change_presence(activity=discord.Game("with you!"))
		await asyncio.sleep(10)
		await client.change_presence(activity=discord.Game("with Krypton!"))
		await asyncio.sleep(10)
		await client.change_presence(activity=discord.Game("YOUR_BOT_PREFIX_HERE help"))
		await asyncio.sleep(10)
		await client.change_presence(activity=discord.Game("with humans!"))
		await asyncio.sleep(10)

@client.event
async def on_ready():
	client.loop.create_task(status_task())
	print('Logged in as ' + client.user.name)
	print("Discord.py API version:", discord.__version__)
	print("Python version:", platform.python_version())
	print("Running on:", platform.system(), platform.release(), "(" + os.name + ")")
	print('-------------------')

@client.command(name='info', pass_context=True)
async def info(context):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!', description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await context.message.channel.send(embed=embed)
	else:
		e = discord.Embed(description='Used Krypons template', color=0x00FF00)
		e.set_author(name="Bot Informations")
		e.add_field(name="Owner:", value="Krypton#1337", inline=True)
		e.add_field(name="Python Version:", value="{0}".format(python_version()), inline=True)
		e.add_field(name="Prefix:", value="YOUR_PREFIX_HERE ", inline=False)
		e.set_footer(text="Requested by {0}".format(context.message.author))
		await context.message.channel.send(embed=e)

@client.command(name='serverinfo', pass_context=True)
async def serverinfo(context):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!', description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await context.message.channel.send(embed=embed)
	else:
		server = context.message.guild
		roles = [x.name for x in server.roles]
		role_length = len(roles)
		if role_length > 50:
			roles = roles[:50]
			roles.append('>>>> Displaying[50/%s] Roles' % len(roles))
		roles = ', '.join(roles)
		channelz = len(server.channels)
		time = str(server.created_at)
		time = time.split(' ')
		time = time[0]
		embed = discord.Embed(description='%s ' % (str(server)), title='**Server Name:**', color=0x00FF00)
		embed.set_thumbnail(url=server.icon_url)
		embed.add_field(name='__Owner__', value=str(server.owner) + '\n' + str(server.owner.id))
		embed.add_field(name='__Server ID__', value=str(server.id))
		embed.add_field(name='__Member Count__', value=str(server.member_count))
		embed.add_field(name='__Text/Voice Channels__', value=str(channelz))
		embed.add_field(name='__Roles (%s)__' % str(role_length), value=roles)
		embed.set_footer(text='Created at: %s' % time)
		await context.message.channel.send(embed=embed)

@client.command(name='ping', pass_context=True)
async def ping(context):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!', description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await context.message.channel.send(embed=embed)
	else:
		embed = discord.Embed(color=0x00FF00)
		embed.set_footer(text='Pong request by {0}'.format(context.message.author))
		embed.add_field(name='Pong!', value=':ping_pong:', inline=True)
		await context.message.channel.send(embed=embed)

@client.command(name='invite', pass_context=True)
async def invite(context):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!', description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await context.message.channel.send(embed=embed)
	else:
		await context.message.channel.send('I sent you a private message!')
		await context.message.channel.send('Invite me by clicking here: https://discordapp.com/oauth2/authorize?&client_id=YOUR_APPLICATION_ID_HERE&scope=bot&permissions=8')


@client.command(name='server', pass_context=True)
async def server(context):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!', description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await context.message.channel.send(embed=embed)
	else:
		await context.message.channel.send('I sent you a private message!')
		await context.message.channel.send('Join my discord server by clicking here: https://discord.gg/Vddcy76')

@client.command(name='poll', pass_context=True)
async def poll(context, *args):
	mesg = ' '.join(args)
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!', description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await context.message.channel.send(embed=embed)
	else:
		await context.message.delete()
		embed = discord.Embed(title='We have a poll !', description='{0}'.format(mesg), color=0x00FF00)
		embed.set_footer(text='Poll created by: {0} • React to vote!'.format(context.message.author))
		embed_message = await context.message.channel.send(embed=embed)
		await embed_message.add_reaction( '👍')
		await embed_message.add_reaction('👎')
		await embed_message.add_reaction('🤷')

@client.command(name='8ball', pass_context=True)
async def eight_ball(context, *args):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!',
							  description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await context.message.channel.send(embed=embed)
	else:
		answers = ['It is certain.', 'It is decidedly so.', 'You may rely on it.', 'Without a doubt.',
				   'Yes - definitely.', 'As I see, yes.', 'Most likely.', 'Outlook good.', 'Yes.',
				   'Signs point to yes.', 'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.',
				   'Cannot predict now.', 'Concentrate and ask again later.', 'Don\'t count on it.', 'My reply is no.',
				   'My sources say no.', 'Outlook not so good.', 'Very doubtful.']
		embed = discord.Embed(title='**My Answer:** ', description='{0}'.format(answers[randint(0, len(answers))]), color=0x00FF00)
		embed.set_footer(text='Question asked by: {0} • Ask your own now!'.format(context.message.author))
		await context.message.channel.send(embed=embed)

@client.command(pass_context=True)
async def bitcoin(context):
	url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
	async with aiohttp.ClientSession() as session:  # Async HTTP request
		raw_response = await session.get(url)
		response = await raw_response.text()
		response = json.loads(response)
		embed = discord.Embed(title=':information_source: Info',
							  description='Bitcoin price is: $' + response['bpi']['USD']['rate'], color=0x00FF00)
		await context.message.channel.send(embed=embed)


@client.command(name='shutdown', pass_context=True)
async def shutdown(context):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!',
							  description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await context.message.channel.send(embed=embed)
	else:
		if context.message.author.id in OWNERS:
			embed = discord.Embed(title='Shutdown!', description='Shutting down. Bye! :wave:', color=0x00FF00)
			await context.message.channel.send(embed=embed)
			await client.logout()
			await client.close()
		else:
			embed = discord.Embed(title='Error!', description='You don\'t have the permission to use this command.',
								  color=0x00FF00)
			await context.message.channel.send(embed=embed)


@client.command(name='say', pass_context=True)
async def echo(context, *, content):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!', description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await context.message.channel.send(embed=embed)
	else:
		if context.message.author.id in OWNERS:
			await context.message.delete()
			await context.message.channel.send(content)
		else:
			embed = discord.Embed(title='Error!', description='You don\'t have the permission to use this command.', color=0x00FF00)
			await context.message.channel.send(embed=embed)

@client.command(name='embed', pass_context=True)
async def embed(context, *args):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!', description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await context.message.channel.send(embed=embed)
	else:
		if context.message.author.id in OWNERS:
			mesg = ' '.join(args)
			embed = discord.Embed(description=mesg, color=0x00FF00)
			await context.message.channel.send(embed=embed)
			await context.message.delete()
		else:
			embed = discord.Embed(title='Error!', description='You don\'t have the permission to use this command.',
								  color=0x00FF00)
			await context.message.channel.send(embed=embed)


@client.command(name='kick', pass_context=True)
async def kick(context, member: discord.Member, *args):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!',
							  description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await context.message.channel.send(embed=embed)
	else:
		if context.message.author.guild_permissions.kick_members:
			if member.guild_permissions.administrator:
				embed = discord.Embed(title='Error!', description='User has Admin permissions.', color=0x00FF00)
				await context.message.channel.send(embed=embed)
			else:
				mesg = ' '.join(args)
				embed = discord.Embed(title='User Kicked!', description='**{0}** was kicked by **{1}**!'.format(member,
																												context.message.author),
									  color=0x00FF00)
				embed.add_field(name='Reason:', value=mesg)
				await context.message.channel.send(embed=embed)
				await context.message.delete()
				await member.send('You where warned by **{0}**!  '.format(context.message.author) + 'Reason: {0}'.format(mesg))
				await member.kick()
		else:
			embed = discord.Embed(title='Error!', description='You don\'t have the permission to use this command.',
								  color=0x00FF00)
			await context.message.channel.send(embed=embed)

@client.command(name='nick', pass_context=True)
async def nick(context, member: discord.Member, *, name : str):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!', description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await context.message.channel.send(embed=embed)
	else:
		if context.message.author.guild_permissions.administrator:
			if name.lower() == "!reset":
				name = None
			embed = discord.Embed(title='Changed Nickname!', description='**{0}** new nickname is **{1}**!'.format(member, name), color=0x00FF00)
			await context.message.channel.send(embed=embed)
			await context.message.delete()
			await member.change_nickname(name)
		else:
			embed = discord.Embed(title='Error!', description='You don\'t have the permission to use this command.', color=0x00FF00)
			await context.message.channel.send(embed=embed)

@client.command(name='ban', pass_context=True)
async def ban(context, member: discord.Member, *args):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!',
							  description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await context.message.channel.send(embed=embed)
	else:
		if context.message.author.guild_permissions.administrator:
			if member.guild_permissions.administrator:
				embed = discord.Embed(title='Error!', description='User has Admin permissions.', color=0x00FF00)
				await context.message.channel.send(embed=embed)
			else:
				mesg = ' '.join(args)
				embed = discord.Embed(title='User Banned!', description='**{0}** was banned by **{1}**!'.format(member,
																												context.message.author),
									  color=0x00FF00)
				embed.add_field(name='Reason:', value=mesg)
				await context.message.channel.send(embed=embed)
				await context.message.delete()
				await member.send('You where banned by **{0}**!'.format(
					context.message.author) + 'Reason: {0}'.format(mesg))
				await member.ban()
		else:
			embed = discord.Embed(title='Error!', description='You don\'t have the permission to use this command.',
								  color=0x00FF00)
			await context.message.channel.send(embed=embed)


@client.command(name='unban', pass_context=True)
async def unban(context, user: discord.Member):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!',
							  description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await context.message.channel.send(embed=embed)
	else:
		if context.message.author.guild_permissions.administrator:
			embed = discord.Embed(title='User Unbanned!',
								  description='**{0}** was unbanned by **{1}**!'.format(user, context.message.author),
								  color=0x00FF00)
			await context.message.channel.send(embed=embed)
			await context.message.delete()
			await user.send('You where unbanned by **{0}**!  '.format(context.message.author) + 'Reason: Ban revoked')
			await user.unban()
		else:
			embed = discord.Embed(title='Error!', description='You don\'t have the permission to use this command.',
								  color=0x00FF00)
			await context.message.channel.send(embed=embed)


@client.command(name='warn', pass_context=True)
async def warn(context, member: discord.Member, *args):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!',
							  description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await context.message.channel.send(embed=embed)
	else:
		if context.message.author.guild_permissions.administrator:
			mesg = ' '.join(args)
			embed = discord.Embed(title='User Warned!',
								  description='**{0}** was warned by **{1}**!'.format(member, context.message.author),
								  color=0x00FF00)
			embed.add_field(name='Reason:', value=mesg)
			await context.message.channel.send(embed=embed)
			await context.message.delete()
			await member.send('You where warned by **{0}**!  '.format(
				context.message.author) + 'Reason: {0}'.format(mesg))
		else:
			embed = discord.Embed(title='Error!', description='You don\'t have the permission to use this command.',
								  color=0x00FF00)
			await context.message.channel.send(embed=embed)


@client.command(name='purge', pass_context=True)
async def purge(context, number):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!',
							  description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await context.message.channel.send(embed=embed)
	else:
		if context.message.author.guild_permissions.administrator:
			number = int(number)
			await context.message.channel.purge(limit=number)
			embed = discord.Embed(title='Chat Cleared!',
								  description='**{0}** cleared **{1}** messages!'.format(context.message.author,
																						 number), color=0x00FF00)
			message = await context.message.channel.send(embed=embed)
			await asyncio.sleep(3)
			await message.delete()
		else:
			embed = discord.Embed(title='Error!', description='You don\'t have the permission to use this command.',
								  color=0x00FF00)
			await context.message.channel.send(embed=embed)

@client.command(name='blacklist', pass_context=True)
async def blacklist(context, mode : str, user : discord.User = None):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!',
							  description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await context.message.channel.send(embed=embed)
	else:
		if context.message.author.id in OWNERS:
			if (mode.lower() == "add"):
				userID = user.id
				try:
					BLACKLIST.append(userID)
					embed = discord.Embed(title="User Blacklisted", description='**{0}** has been successfully added to the blacklist'.format(user.name), color=0x00FF00)
					embed.set_footer(text='There are now {0} users in the blacklist'.format(len(BLACKLIST)))
					await context.message.channel.send(embed=embed)
				except:
					embed = discord.Embed(title=":x: Error!", description="An unknown error occurred when trying to add **{0}** to the blacklist.".format(user.name), color=0xFF0000)
					await context.message.channel.send(embed=embed)
			elif (mode.lower() == "remove"):
				userID = user.id
				try:
					BLACKLIST.remove(userID)
					embed = discord.Embed(title="User Unblacklisted",
										  description='**{0}** has been successfully removed from the blacklist'.format(
											  user.name), color=0x00FF00)
					embed.set_footer(text='There are now {0} users in the blacklist'.format(len(BLACKLIST)))
					await context.message.channel.send(embed=embed)
				except:
					embed = discord.Embed(title=":x: Error!",
										  description="An unknown error occurred when trying to remove **{0}** from the blacklist.\nAre you sure the user is in the blacklist?".format(
											  user.name), color=0xFF0000)
					await context.message.channel.send(embed=embed)
			elif (mode.lower() == "list"):
				embed = discord.Embed(title="There are currently {0} blacklisted IDs".format(len(BLACKLIST)),
									  description="{0}".format(BLACKLIST),
									  color=0x00FF00)
				await context.message.channel.send(embed=embed)
		else:
			embed = discord.Embed(title='Error!', description='You don\'t have the permission to use this command.',
								  color=0xFF0000)
			await context.message.channel.send(embed=embed)

client.remove_command('help')

@client.command(name='help', description='Help HUD.', brief='HELPOOOO!!!', pass_context=True)
async def help(context):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!', description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await context.message.channel.send(embed=embed)
	else:
		# Note that commands made only for the owner of the bot are not listed here.
		embed = discord.Embed(title='Bot', description='List of commands are:', color=0x00FF00)
		embed.add_field(name='Invite - Invite the bot', value='Usage: YOUR_PREFIX_HERE invite', inline=False)
		embed.add_field(name='Server - Join my own server', value='Usage: YOUR_PREFIX_HERE server', inline=False)
		embed.add_field(name='Poll - Create a poll for your users', value='Usage: YOUR_PREFIX_HERE poll <idea>', inline=False)
		embed.add_field(name='8Ball - Answers to your questions', value='Usage: YOUR_PREFIX_HERE 8ball <question>', inline=False)
		embed.add_field(name='Bitcoin - Shows the currency of the bitcoin', value='Usage: YOUR_PREFIX_HERE bitcoin', inline=False)
		embed.add_field(name='Info - Gives infos about the bot', value='Usage: YOUR_PREFIX_HERE info', inline=False)
		embed.add_field(name='Shutdown - Shutdowns the bot [OWNER]', value='Usage: YOUR_PREFIX_HERE shutdown', inline=False)
		embed.add_field(name='Say - I send a message of your choice [OWNER]', value='Usage: YOUR_PREFIX_HERE say <message>', inline=False)
		embed.add_field(name='Embed - I send a embed message of your choice [OWNER]', value='Usage: YOUR_PREFIX_HERE embed <message>', inline=False)
		embed.add_field(name='Kick - Kick a user', value='Usage: YOUR_PREFIX_HERE kick <user> <reason>', inline=False)
		embed.add_field(name='Ban - Ban a user', value='Usage: YOUR_PREFIX_HERE ban <user> <reason>', inline=False)
		embed.add_field(name='Warn - Warn a user in private messages', value='Usage: YOUR_PREFIX_HERE warn <user> <reason>', inline=False)
		embed.add_field(name='Unban - Unban a user', value='Usage: YOUR_PREFIX_HERE unban <user>', inline=False)
		embed.add_field(name='Purge - Remove an amount of messages', value='Usage: YOUR_PREFIX_HERE purge <number>', inline=False)
		embed.add_field(name='Help - Gives this menu', value='Usage: YOUR_PREFIX_HERE help', inline=False)
		await context.message.channel.send(embed=embed)

@client.event
async def on_command_error(context, error):
	if isinstance(error, commands.CommandOnCooldown):
		await context.message.delete()
		embed = discord.Embed(title="Error!", description='This command is on a %.2fs cooldown' % error.retry_after, color=0x00FF00)
		message = await context.message.channel.send(embed=embed)
		await asyncio.sleep(5)
		await message.delete()
	raise error

@blacklist.error
async def blacklist_error(context, error):
	embed = discord.Embed(title='**Command:** YOUR_PREFIX_HERE blacklist', description='**Description::** Prevents a user from using the bot \n **Usage:** YOUR_PREFIX_HERE blacklist [add/remove/list] [user] \n **Example:** YOUR_PREFIX_HERE blacklist add @RandomUser', color=0x00FF00)
	await context.message.channel.send(embed=embed)

@ban.error
async def ban_error(context, error):
	embed = discord.Embed(title='**Command:** YOUR_PREFIX_HERE ban', description='**Description:** Bans a member \n **Usage:** YOUR_PREFIX_HERE ban [user] [reason] \n **Example:** YOUR_PREFIX_HERE ban @RandomUser Get out!', color=0x00FF00)
	await context.message.channel.send(embed=embed)

@poll.error
async def poll_error(context, error):
	embed = discord.Embed(title='**Command:** YOUR_PREFIX_HERE poll', description='**Description:** Create a pool to vote \n **Usage:** YOUR_PREFIX_HERE poll [idea] \n **Example:** YOUR_PREFIX_HERE poll Add new emojis!', color=0x00FF00)
	await context.message.channel.send(embed=embed)

@eight_ball.error
async def eight_ball_error(context, error):
	embed = discord.Embed(title='**Command:** YOUR_PREFIX_HERE 8ball', description='**Description:** Get an answer to all of your questions \n **Usage:** YOUR_PREFIX_HERE 8ball [question] \n **Example:** YOUR_PREFIX_HERE 8ball Is this bot cool?', color=0x00FF00)
	await context.message.channel.send(embed=embed)

@echo.error
async def say_error(context, error):
	embed = discord.Embed(title='**Command:** YOUR_PREFIX_HERE say',
						  description='**Description:** I say what you say \n **Usage:** YOUR_PREFIX_HERE say [message] \n **Example:** YOUR_PREFIX_HERE say Hello!!',
						  color=0x00FF00)
	await context.message.channel.send(embed=embed)


@embed.error
async def embed_error(context, error):
	embed = discord.Embed(title='**Command:** YOUR_PREFIX_HERE embed',
						  description='**Description:** I say what you say as embed message \n **Usage:** YOUR_PREFIX_HERE embed [message] \n **Example:** YOUR_PREFIX_HERE embed Hello!!',
						  color=0x00FF00)
	await context.message.channel.send(embed=embed)


@kick.error
async def kick_error(context, error):
	embed = discord.Embed(title='**Command:** YOUR_PREFIX_HERE kick',
						  description='**Description:** Kicks a member \n **Usage:** YOUR_PREFIX_HERE kick [user] [reason] \n **Example:** YOUR_PREFIX_HERE kick @RandomUser Rejoin when you\'ll be smarter, like me!',
						  color=0x00FF00)
	await context.message.channel.send(embed=embed)


@unban.error
async def unban_error(context, error):
	embed = discord.Embed(title='**Command:** YOUR_PREFIX_HERE unban',
						  description='**Description:** Unbans a member \n **Usage:** YOUR_PREFIX_HERE unban [user] \n **Example:** YOUR_PREFIX_HERE unban @RandomUser',
						  color=0x00FF00)
	await context.message.channel.send(embed=embed)

@warn.error
async def warn_error(context, error):
	embed = discord.Embed(title='**Command:** YOUR_PREFIX_HERE warn',
						  description='**Description:** Warns a member \n **Usage:** YOUR_PREFIX_HERE warn [user] [reason] \n **Example:** YOUR_PREFIX_HERE warn @RandomUser Stop the caps, thanks!',
						  color=0x00FF00)
	await context.message.channel.send(embed=embed)


@purge.error
async def purge_error(context, error):
	embed = discord.Embed(title='**Command:** YOUR_PREFIX_HERE purge',
						  description='**Description:** Delete a certain amount of messages \n **Usage:** YOUR_PREFIX_HERE purge [numer of messages] \n **Example:** YOUR_PREFIX_HERE purge 20',
						  color=0x00FF00)
	await context.message.channel.send(embed=embed)

client.run(TOKEN)