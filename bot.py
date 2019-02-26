import discord
import asyncio
import aiohttp
import json
from discord import Game
from discord.ext.commands import Bot
from random import randint
from discord.ext.commands.cooldowns import BucketType
from discord.ext import commands
from datetime import datetime
from platform import python_version

BOT_PREFIX = ('YOUR_BOT_PREFIX_HERE')
TOKEN = 'YOUR_BOT_TOKEN_HERE'
OWNER = 'YOUR_DISCORD_USER_ID_HERE'
BLACKLIST = []
client = Bot(command_prefix=BOT_PREFIX)

async def status_task():
	while True:
		await client.change_presence(game=Game(name='with You'))
		await asyncio.sleep(10)
		await client.change_presence(game=Game(name='with Krypton'))
		await asyncio.sleep(10)
		await client.change_presence(game=Game(name='k>help'))
		await asyncio.sleep(10)
		await client.change_presence(game=Game(name='with Humans'))
		await asyncio.sleep(10)
		await client.change_presence(game=Game(name='with fellow peeps'))
		await asyncio.sleep(10)


@client.event
async def on_ready():
	client.loop.create_task(status_task())
	print('Logged in as ' + client.user.name)
	print('-------------------')

async def list_servers():
	await client.wait_until_ready()
	while not client.is_closed:
		print('Current servers:')
		for server in client.servers:
			print(server.name)
		await asyncio.sleep(600)

@client.command(name='info', pass_context=True)
@commands.cooldown(1, 5, BucketType.user)
async def info(context):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!', description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await client.say(embed=embed)
	else:
		e = discord.Embed(description='Used Krypons template', color=0x00FF00)
		e.set_author(name="Bot Informations")
		e.add_field(name="Owner:", value="Krypton#1337", inline=True)
		e.add_field(name="Python Version:", value="{0}".format(python_version()), inline=True)
		e.add_field(name="Prefix:", value="k>", inline=False)
		e.set_footer(text="Requested by {0}".format(context.message.author))
		await client.say(embed=e)
	await client.send_message(context.message.channel, embed=embed)

@client.command(name='serverinfo', pass_context=True)
@commands.cooldown(1, 10, BucketType.user)
async def serverinfo(context):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!', description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await client.say(embed=embed)
	else:
		server = context.message.server
		roles = [x.name for x in server.role_hierarchy]
		role_length = len(roles)
		if role_length > 50:
			roles = roles[:50]
			roles.append('>>>> Displaying[50/%s] Roles' % len(roles))
		roles = ', '.join(roles);
		channelz = len(server.channels);
		time = str(server.created_at);
		time = time.split(' ');
		time = time[0];
		join = discord.Embed(description='%s ' % (str(server)), title='**Server Name:**', color=0x00FF00);
		join.set_thumbnail(url=server.icon_url);
		join.add_field(name='__Owner__', value=str(server.owner) + '\n' + server.owner.id);
		join.add_field(name='__Server ID__', value=str(server.id))
		join.add_field(name='__Member Count__', value=str(server.member_count));
		join.add_field(name='__Text/Voice Channels__', value=str(channelz));
		join.add_field(name='__Roles (%s)__' % str(role_length), value=roles);
		join.set_footer(text='Created at: %s' % time);
		await client.send_message(context.message.channel, embed=join)


@client.command(name='ping', pass_context=True)
@commands.cooldown(1, 10, BucketType.user)
async def ping(context):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!', description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await client.say(embed=embed)
	else:
		embed = discord.Embed(color=0x00FF00)
		embed.set_footer(text='Pong request by {0}'.format(context.message.author))
		embed.add_field(name='Pong!', value=':ping_pong:', inline=True)
		await client.send_message(context.message.channel, embed=embed)

@client.command(name='invite', pass_context=True)
@commands.cooldown(1, 5, BucketType.user)
async def invite(context):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!', description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await client.say(embed=embed)
	else:
		await client.say('I sent you a private message!')
		await client.send_message(context.message.author, 'Invite me by clicking here: https://discordapp.com/oauth2/authorize?&client_id=YOUR_APPLICATION_ID_HERE&scope=bot&permissions=8')


@client.command(name='server', pass_context=True)
@commands.cooldown(1, 5, BucketType.user)
async def server(context):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!', description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await client.say(embed=embed)
	else:
		await client.say('I sent you a private message!')
		await client.send_message(context.message.author, 'Join my discord server by clicking here: https://discord.gg/yX6J7Cf')

@client.command(name='poll', pass_context=True)
@commands.cooldown(1, 5, BucketType.user)
async def poll(context, *args):
	mesg = ' '.join(args)
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!', description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await client.say(embed=embed)
	else:
		await client.delete_message(context.message)
		embed = discord.Embed(title='We have a poll !', description='{0}'.format(mesg), color=0x00FF00)
		embed.set_footer(text='Poll created by: {0} • React to vote!'.format(context.message.author))
		embed_message = await client.say(embed=embed)
		await client.add_reaction(embed_message, '👍')
		await client.add_reaction(embed_message, '👎')
		await client.add_reaction(embed_message, '🤷')

@client.command(name='8ball', pass_context=True)
@commands.cooldown(1, 5, BucketType.user)
async def eight_ball(context, *args):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!',
							  description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await client.say(embed=embed)
	else:
		answers = ['It is certain.', 'It is decidedly so.', 'You may rely on it.', 'Without a doubt.',
				   'Yes - definitely.', 'As I see, yes.', 'Most likely.', 'Outlook good.', 'Yes.',
				   'Signs point to yes.', 'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.',
				   'Cannot predict now.', 'Concentrate and ask again later.', 'Don\'t count on it.', 'My reply is no.',
				   'My sources say no.', 'Outlook not so good.', 'Very doubtful.']
		embed = discord.Embed(title='**My Answer:** ', description='{0}'.format(answers[randint(0, len(answers))]), color=0x00FF00)
		embed.set_footer(text='Question asked by: {0} • Ask your own now!'.format(context.message.author))
		await client.say(embed=embed)

@client.command()
@commands.cooldown(1, 5, BucketType.user)
async def bitcoin():
	url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
	async with aiohttp.ClientSession() as session:  # Async HTTP request
		raw_response = await session.get(url)
		response = await raw_response.text()
		response = json.loads(response)
		embed = discord.Embed(title=':information_source: Info',
							  description='Bitcoin price is: $' + response['bpi']['USD']['rate'], color=0x00FF00)
		await client.say(embed=embed)


@client.command(name='shutdown', pass_context=True)
@commands.cooldown(1, 10, BucketType.user)
async def shutdown(context):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!',
							  description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await client.say(embed=embed)
	else:
		if context.message.author.id == OWNER:
			embed = discord.Embed(title='Shutdown!', description='Shutting down. Bye! :wave:', color=0x00FF00)
			await client.send_message(context.message.channel, embed=embed)
			await client.logout()
			await client.close()
		else:
			embed = discord.Embed(title='Error!', description='You don\'t have the permission to use this command.',
								  color=0x00FF00)
			await client.send_message(context.message.channel, embed=embed)


@client.command(name='say', pass_context=True)
async def echo(context, *, content):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!', description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await client.say(embed=embed)
	else:
		if context.message.author.id == OWNER:
			await client.delete_message(context.message)
			await client.say(content)
		else:
			embed = discord.Embed(title='Error!', description='You don\'t have the permission to use this command.', color=0x00FF00)
			await client.send_message(context.message.channel, embed=embed)

@client.command(name='embed', pass_context=True)
async def embed(context, *args):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!', description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await client.say(embed=embed)
	else:
		if context.message.author.id == OWNER:
			mesg = ' '.join(args)
			embed = discord.Embed(description=mesg, color=0x00FF00)
			await client.say(embed=embed)
			await client.delete_message(context.message)
		else:
			embed = discord.Embed(title='Error!', description='You don\'t have the permission to use this command.',
								  color=0x00FF00)
			await client.send_message(context.message.channel, embed=embed)


@client.command(name='kick', pass_context=True)
@commands.cooldown(1, 5, BucketType.user)
async def kick(context, member: discord.Member, *args):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!',
							  description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await client.say(embed=embed)
	else:
		if context.message.author.server_permissions.kick_members or context.message.author.id == OWNER:
			if member.server_permissions.administrator:
				embed = discord.Embed(title='Error!', description='User has Admin permissions.', color=0x00FF00)
				await client.send_message(context.message.channel, embed=embed)
			else:
				mesg = ' '.join(args)
				embed = discord.Embed(title='User Kicked!', description='**{0}** was kicked by **{1}**!'.format(member,
																												context.message.author),
									  color=0x00FF00)
				embed.add_field(name='Reason:', value=mesg)
				await client.say(embed=embed)
				await client.delete_message(context.message)
				await client.send_message(member, 'You where warned by **{0}**!  '.format(
					context.message.author) + 'Reason: {0}'.format(mesg))
				await client.kick(member)
		else:
			embed = discord.Embed(title='Error!', description='You don\'t have the permission to use this command.',
								  color=0x00FF00)
			await client.send_message(context.message.channel, embed=embed)

@client.command(name='nick', pass_context=True)
@commands.cooldown(1, 5, BucketType.user)
async def nick(context, member: discord.Member, *, name : str):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!', description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await client.say(embed=embed)
	else:
		if context.message.author.server_permissions.administrator or context.message.author.id == OWNER:
			if name.lower() == "!reset":
				name = None
			embed = discord.Embed(title='Changed Nickname!', description='**{0}** new nickname is **{1}**!'.format(member, name), color=0x00FF00)
			await client.say(embed=embed)
			await client.delete_message(context.message)
			await client.change_nickname(member, name)
		else:
			embed = discord.Embed(title='Error!', description='You don\'t have the permission to use this command.', color=0x00FF00)
			await client.send_message(context.message.channel, embed=embed)

@client.command(name='ban', pass_context=True)
@commands.cooldown(1, 5, BucketType.user)
async def ban(context, member: discord.Member, *args):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!',
							  description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await client.say(embed=embed)
	else:
		if context.message.author.server_permissions.administrator or context.message.author.id == OWNER:
			if member.server_permissions.administrator:
				embed = discord.Embed(title='Error!', description='User has Admin permissions.', color=0x00FF00)
				await client.send_message(context.message.channel, embed=embed)
			else:
				mesg = ' '.join(args)
				embed = discord.Embed(title='User Banned!', description='**{0}** was banned by **{1}**!'.format(member,
																												context.message.author),
									  color=0x00FF00)
				embed.add_field(name='Reason:', value=mesg)
				await client.say(embed=embed)
				await client.delete_message(context.message)
				await client.send_message(member, 'You where banned by **{0}**!'.format(
					context.message.author) + 'Reason: {0}'.format(mesg))
				await client.ban(member)
		else:
			embed = discord.Embed(title='Error!', description='You don\'t have the permission to use this command.',
								  color=0x00FF00)
			await client.send_message(context.message.channel, embed=embed)


@client.command(name='unban', pass_context=True)
@commands.cooldown(1, 3, BucketType.user)
async def unban(context, user: discord.User):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!',
							  description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await client.say(embed=embed)
	else:
		if context.message.author.server_permissions.administrator or context.message.author.id == OWNER:
			embed = discord.Embed(title='User Unbanned!',
								  description='**{0}** was unbanned by **{1}**!'.format(user, context.message.author),
								  color=0x00FF00)
			await client.say(embed=embed)
			await client.delete_message(context.message)
			await client.send_message(user, 'You where unbanned by **{0}**!  '.format(
				context.message.author) + 'Reason: Ban revoked')
			await client.unban(user)
		else:
			embed = discord.Embed(title='Error!', description='You don\'t have the permission to use this command.',
								  color=0x00FF00)
			await client.send_message(context.message.channel, embed=embed)


@client.command(name='warn', pass_context=True)
@commands.cooldown(1, 5, BucketType.user)
async def warn(context, member: discord.Member, *args):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!',
							  description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await client.say(embed=embed)
	else:
		if context.message.author.server_permissions.administrator or context.message.author.id == OWNER:
			mesg = ' '.join(args)
			embed = discord.Embed(title='User Warned!',
								  description='**{0}** was warned by **{1}**!'.format(member, context.message.author),
								  color=0x00FF00)
			embed.add_field(name='Reason:', value=mesg)
			await client.say(embed=embed)
			await client.delete_message(context.message)
			await client.send_message(member, 'You where warned by **{0}**!  '.format(
				context.message.author) + 'Reason: {0}'.format(mesg))
		else:
			embed = discord.Embed(title='Error!', description='You don\'t have the permission to use this command.',
								  color=0x00FF00)
			await client.send_message(context.message.channel, embed=embed)


@client.command(name='purge', pass_context=True)
@commands.cooldown(1, 5, BucketType.user)
async def purge(context, number):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!',
							  description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await client.say(embed=embed)
	else:
		if context.message.author.server_permissions.administrator or context.message.author.id == OWNER:
			await client.delete_message(context.message)
			number = int(number)
			counter = 0
			async for x in client.logs_from(context.message.channel, limit=number):
				if counter < number:
					await client.delete_message(x)
					counter += 1
					await asyncio.sleep(0.2)
			embed = discord.Embed(title='Chat Cleared!',
								  description='**{0}** cleared **{1}** messages!'.format(context.message.author,
																						 number), color=0x00FF00)
			message = await client.send_message(context.message.channel, embed=embed)
			await asyncio.sleep(3)
			await client.delete_message(message)
		else:
			embed = discord.Embed(title='Error!', description='You don\'t have the permission to use this command.',
								  color=0x00FF00)
			await client.send_message(context.message.channel, embed=embed)


client.remove_command('help')

@client.command(name='help', description='Help HUD.', brief='HELPOOOO!!!', pass_context=True)
@commands.cooldown(1, 5, BucketType.user)
async def help(context):
	if context.message.author.id in BLACKLIST:
		embed = discord.Embed(title='You\'re blacklisted!', description='Ask the owner to remove from the list if it was unfair.', color=0x00FF00)
		await client.say(embed=embed)
	else:
		embed = discord.Embed(title='Bot', description='List of commands are:', color=0x00FF00)
		embed.add_field(name='Invite - Invite the bot', value='Usage: k>invite', inline=False)
		embed.add_field(name='Server - Join my own server', value='Usage: k>server', inline=False)
		embed.add_field(name='Poll - Create a poll for your users', value='Usage: k>poll <idea>', inline=False)
		embed.add_field(name='8Ball - Answers to your questions', value='Usage: k>8ball <question>', inline=False)
		embed.add_field(name='Bitcoin - Shows the currency of the bitcoin', value='Usage: k>bitcoin', inline=False)
		embed.add_field(name='Info - Gives infos about the bot', value='Usage: k>info', inline=False)
		embed.add_field(name='Shutdown - Shutdowns the bot [OWNER]', value='Usage: k>shutdown', inline=False)
		embed.add_field(name='Say - I send a message of your choice [OWNER]', value='Usage: k>say <message>', inline=False)
		embed.add_field(name='Embed - I send a embed message of your choice [OWNER]', value='Usage: k>embed <message>', inline=False)
		embed.add_field(name='Kick - Kick a user', value='Usage: k>kick <user> <reason>', inline=False)
		embed.add_field(name='Ban - Ban a user', value='Usage: k>ban <user> <reason>', inline=False)
		embed.add_field(name='Warn - Warn a user in private messages', value='Usage: k>warn <user> <reason>', inline=False)
		embed.add_field(name='Unban - Unban a user', value='Usage: k>unban <user>', inline=False)
		embed.add_field(name='Purge - Remove an amount of messages', value='Usage: k>purge <number>', inline=False)
		embed.add_field(name='Help - Gives this menu', value='Usage: k>help', inline=False)
		await client.send_message(context.message.channel, embed=embed)

@client.event
async def on_message(message):
	contents = message.content.split(' ')
	for word in contents:
		if word.lower() in BLOCKED_WORDS:
			if not message.author.id in UNBLOCKED_USERS:
				await client.delete_message(message)
				embed = discord.Embed(title='Error!', description='You don\'t have the permission to send this word.', color=0x00FF00)
				message = await client.send_message(message.channel, embed=embed)
				await asyncio.sleep(3)
				await client.delete_message(message)

	await client.process_commands(message)

@client.event
async def on_command_error(error, context):
	if isinstance(error, commands.CommandOnCooldown):
		await client.delete_message(context.message)
		embed = discord.Embed(title="Error!", description='This command is on a %.2fs cooldown' % error.retry_after, color=0x00FF00)
		message = await client.send_message(context.message.channel, embed=embed)
		await asyncio.sleep(5)
		await client.delete_message(message)
	raise error

@softban.error
async def softban_error(error, context):
	embed = discord.Embed(title='**Command:** k>softban', description='**Description:** Softbans a member \n **Cooldown:** 5 second(s) \n **Usage:** k>softban [user] [reason] \n **Example:** k>softban @RandomUser Get out!', color=0x00FF00)
	await client.send_message(context.message.channel, embed=embed)

@ban.error
async def ban_error(error, context):
	embed = discord.Embed(title='**Command:** k>ban', description='**Description:** Bans a member \n **Cooldown:** 5 second(s) \n **Usage:** k>ban [user] [reason] \n **Example:** k>ban @RandomUser Get out!', color=0x00FF00)
	await client.send_message(context.message.channel, embed=embed)

@poll.error
async def poll_error(error, context):
	embed = discord.Embed(title='**Command:** k>poll', description='**Description:** Create a pool to vote \n **Cooldown:** 5 second(s) \n **Usage:** k>poll [idea] \n **Example:** k>poll Add new emojis!', color=0x00FF00)
	await client.send_message(context.message.channel, embed=embed)

@eight_ball.error
async def eight_ball_error(error, context):
	embed = discord.Embed(title='**Command:** k>8ball', description='**Description:** Get an answer to all of your questions \n **Cooldown:** 5 second(s) \n **Usage:** k>8ball [question] \n **Example:** k>8ball Is this bot cool?', color=0x00FF00)
	await client.send_message(context.message.channel, embed=embed)

@echo.error
async def say_error(error, context):
	embed = discord.Embed(title='**Command:** k>say',
						  description='**Description:** I say what you say \n **Cooldown:** 0 second(s) \n **Usage:** k>say [message] \n **Example:** k>say Hello!!',
						  color=0x00FF00)
	await client.send_message(context.message.channel, embed=embed)


@embed.error
async def embed_error(error, context):
	embed = discord.Embed(title='**Command:** k>embed',
						  description='**Description:** I say what you say as embed message \n **Cooldown:** 0 second(s) \n **Usage:** k>embed [message] \n **Example:** k>embed Hello!!',
						  color=0x00FF00)
	await client.send_message(context.message.channel, embed=embed)


@kick.error
async def kick_error(error, context):
	embed = discord.Embed(title='**Command:** k>kick',
						  description='**Description:** Kicks a member \n **Cooldown:** 5 second(s) \n **Usage:** k>kick [user] [reason] \n **Example:** k>kick @RandomUser Rejoin when you\'ll be smarter, like me!',
						  color=0x00FF00)
	await client.send_message(context.message.channel, embed=embed)


@unban.error
async def unban_error(error, context):
	embed = discord.Embed(title='**Command:** k>unban',
						  description='**Description:** Unbans a member \n **Cooldown:** 3 second(s) \n **Usage:** k>unban [user] \n **Example:** k>unban @RandomUser',
						  color=0x00FF00)
	await client.send_message(context.message.channel, embed=embed)

@warn.error
async def warn_error(error, context):
	embed = discord.Embed(title='**Command:** k>warn',
						  description='**Description:** Warns a member \n **Cooldown:** 5 second(s) \n **Usage:** k>warn [user] [reason] \n **Example:** k>warn @RandomUser Stop the caps, thanks!',
						  color=0x00FF00)
	await client.send_message(context.message.channel, embed=embed)


@purge.error
async def purge_error(error, context):
	embed = discord.Embed(title='**Command:** k>purge',
						  description='**Description:** Delete a certain amount of messages \n **Cooldown:** 5 second(s) \n **Usage:** k>purge [numer of messages] \n **Example:** k>purge 20',
						  color=0x00FF00)
	await client.send_message(context.message.channel, embed=embed)

client.loop.create_task(list_servers())
client.run(TOKEN)
