import discord
import json
import random
import time
import os
from  discord.ext import commands, tasks
from itertools import cycle

def get_prefix(bot, message):
    with open('prefix.json', 'r') as x:
        prefixses = json.load(x)

    return prefixses[str(message.guild.id)]

bot = commands.Bot(command_prefix = get_prefix)
status = cycle(["your commands", ".help to ask for help", "helpful commands"])
bot.remove_command("help")

reaction_role_message_id = ""
reaction_role_emoji = ""
reaction_role_role = ""


#bot events
@bot.event
async def on_ready():
    status_change.start()
    os.system("cls")
    print('\u001b[36mBot status= "Ready"\u001b[37m')

@bot.event
async def on_member_join(member):
    print(f"{member} has joined a server")

@bot.event
async def on_member_remove(member):
    print(f"{member} has left a server")

@bot.event
async def on_guild_join(guild):
    with open('prefix.json', 'r') as x:
        prefixses = json.load(x)

    prefixses[str(guild.id)] = "."

    with open('prefix.json', 'w') as x:
        json.dump(prefixses, x, indent=4)

@bot.event
async def on_guild_remove(guild):
    with open('prefix.json', 'r') as x:
        prefixses = json.load(x)

    prefixses.pop(str(guild.id))

    with open('prefix.json', 'w') as x:
        json.dump(prefixses, x, indent=4)

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"```java\n{error}\n```")
    print(f"\u001b[31;1mBot Command Error: {error}\u001b[37m")

@bot.event
async def on_message(message):
    filter = ["fuck", "kut", "idioot", "godverdomme"]

    for word in filter:
        if message.content.count(word) > 0 :
            print("%s has cursed" % (message.author))
            await message.channel.purge(limit=1)
    await bot.process_commands(message)

@bot.event
async def convert(ctx, reason):
    reason = await commands.MemberConverter().convert(ctx, reason)
    permission = reason.guild_permissions.manage_message

@bot.event
async def on_disconnect(ctx):
    channel = ctx.athor.voice.channel
    print(f"Left voice channel: {channel} > {ctx.guild}:{ctx.guild.id}")

@bot.event
async def on_raw_reaction_add(payload):
    global reaction_role_message_id
    global reaction_role_emoji
    global reaction_role_role
    message_id = payload.message_id
    emoji = reaction_role_emoji
    if f"{message_id}" == reaction_role_message_id:
        if emoji == payload.emoji.name:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)

            role = reaction_role_role

            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None:
                    await discord.Member.add_roles(member, role)
                    print(f"Added {role} to {member}")
                else:
                    print(f"Error while adding role: member {member} not found")
            else:
                print(f"Error while adding role: role {role} not found")
        else:
            print(f'Error while adding reaction role: emoji "{emoji}" not found')

# BotCommands
@bot.command()
async def invite(ctx):
    await ctx.send("`Invite link` has been send :banana:")
    invite = discord.Embed(
        title="Invite Link:",
        description="https://discord.com/api/oauth2/authorize?client_id=727967252657471550&permissions=8&scope=bot",
        colour=discord.Colour.from_rgb(250, 250, 0)
    )

    invite.set_footer(text="#Banathon Invite Link")
    invite.set_image(url="https://media.discordapp.net/attachments/619413581145833472/729691884351651931/ezgif-5-c742e4b59516.gif?width=622&height=350")
    invite.set_author(name="Banathon Invite", icon_url="https://cdn.discordapp.com/avatars/727967252657471550/1fcacc779f361241eb5505e4de99ed81.png?size=128")
    invite.set_thumbnail(url="https://cdn.discordapp.com/avatars/727967252657471550/1fcacc779f361241eb5505e4de99ed81.png?size=128")

    await ctx.author.send(embed=invite)
    print(f"An invite link has been send to {ctx.author}")

@bot.command()
async def ping(ctx):
    await ctx.send(f":banana:'s ping is around: `{round(bot.latency * 1000)}ms`")
    print(f"{ctx.author} has checked the bot ping: {round(bot.latency * 1000)}ms")

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await discord.VoiceChannel.connect(channel)
    await ctx.send("`Joined your voice channel` :banana:")
    print(f"Joined voice channel: {channel} > {ctx.guild}:{ctx.guild.id}")

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    userinfo = discord.Embed(
        colour=discord.Colour.from_rgb(250, 250, 0)
    )

    userinfo.set_footer(text=f"#User Info: {member}")
    userinfo.set_author(name=f"{member.name} Info",
                    icon_url=f"{member.avatar_url}")
    userinfo.set_thumbnail(
        url=f"{member.avatar_url}")
    userinfo.add_field(name="Joined At", value=f"`{member.joined_at}`", inline=True)
    userinfo.add_field(name="Role", value=f"`{member.top_role}`", inline=True)
    userinfo.add_field(name="Status", value=f"`{member.status}`", inline=True)

    await ctx.send(embed=userinfo)

@bot.command()
async def coinflip(ctx):
    coin = ["Heads", "Trails"]
    await ctx.send(f"I threw `{random.choice(coin)}` :banana:")

@bot.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ["As I see it, yes.",
                 "Ask again later.",
                 "Better not tell you now.",
                 "Cannot predict now.",
                 "Concentrate and ask again.",
                 "Don’t count on it.",
                 "It is certain.",
                 "It is decidedly so.",
                 "Most likely.",
                 "My reply is no.",
                 "My sources say no.",
                 "Outlook not so good.",
                 "Outlook good.",
                 "Reply hazy, try again.",
                 "Signs point to yes.",
                 "Very doubtful.",
                 "Without a doubt.",
                 "Yes.",
                 "Yes – definitely.",
                 "You may rely on it."]

    await ctx.send(f"`Question:` {question}\n`Answer:` {random.choice(responses)}")

@bot.command()
async def help(ctx, rank=None):
    if rank is None:
        help = discord.Embed(
            colour=discord.Colour.from_rgb(250, 250, 0)
        )

        help.set_footer(text="#Help Command")
        help.set_image(url="https://media.discordapp.net/attachments/619413581145833472/729693870396538910/ezgif-5-3c9c28b0609b.gif?width=622&height=350")
        help.set_author(name="Banathon Help", icon_url="https://cdn.discordapp.com/avatars/727967252657471550/1fcacc779f361241eb5505e4de99ed81.png?size=128")
        help.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/727967252657471550/1fcacc779f361241eb5505e4de99ed81.png?size=128")
        help.add_field(name="Administrator", value="`.help admin`", inline=True)
        help.add_field(name="Fun Commands", value="`.help fun`", inline=True)
        help.add_field(name="All Commands", value="`.help all`", inline=True)

        await ctx.send(embed=help)
    if rank == "admin":
        help_admin = discord.Embed(
            colour=discord.Colour.from_rgb(250, 250, 0)
        )

        help_admin.set_footer(text="#Help Admin Command")
        help_admin.set_author(name="Banathon Help", icon_url="https://cdn.discordapp.com/avatars/727967252657471550/1fcacc779f361241eb5505e4de99ed81.png?size=128")
        help_admin.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/727967252657471550/1fcacc779f361241eb5505e4de99ed81.png?size=128")
        help_admin.add_field(name="`.warn [user] [reason]`", value="Sends a warning to a member.", inline=False)
        help_admin.add_field(name="`.kick [user] [reason]`", value="Kicks a member from the server.", inline=False)
        help_admin.add_field(name="`.ban [user] [reason]`", value="Bans a member from the server.", inline=False)
        help_admin.add_field(name="`.unban [username and tag]`", value="Clears a ban of a member.", inline=False)
        help_admin.add_field(name="`.clear [amount/all]`", value="Clears the chat of a text channel.", inline=False)
        help_admin.add_field(name="`.reactrole [mesage_id] [emoji] [role]`", value="Adds a role to a member if they react.", inline=False)

        await ctx.send(embed=help_admin)
    if rank == "fun":
        help_fun = discord.Embed(
            colour=discord.Colour.from_rgb(250, 250, 0)
        )

        help_fun.set_footer(text="#Help Fun Command")
        help_fun.set_author(name="Banathon Help",
                              icon_url="https://cdn.discordapp.com/avatars/727967252657471550/1fcacc779f361241eb5505e4de99ed81.png?size=128")
        help_fun.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/727967252657471550/1fcacc779f361241eb5505e4de99ed81.png?size=128")
        help_fun.add_field(name="`.8ball [question]`", value="Gives you a random answer to a question.", inline=True)
        help_fun.add_field(name="`.coinflip`", value="Flips a coin, random answer heads or trails.", inline=True)
        help_fun.add_field(name="`.ping`", value="Sends the bots ping in milliseconds.", inline=True)
        help_fun.add_field(name="`.join`", value="Banathon joins your voice channel.", inline=True)
        help_fun.add_field(name="`.invite`", value="Sends a invite for the bot.", inline=True)
        help_fun.add_field(name="`.userinfo`", value="Replays the user info of a user.", inline=True)

        await ctx.send(embed=help_fun)

    if rank == "all":
        help_all = discord.Embed(
            colour=discord.Colour.from_rgb(250, 250, 0)
        )

        help_all.set_footer(text="#Help All Command")
        help_all.set_author(name="Banathon Help",
                              icon_url="https://cdn.discordapp.com/avatars/727967252657471550/1fcacc779f361241eb5505e4de99ed81.png?size=128")
        help_all.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/727967252657471550/1fcacc779f361241eb5505e4de99ed81.png?size=128")
        help_all.add_field(name="`.8ball [question]`", value="Gives you a random answer to a question.", inline=True)
        help_all.add_field(name="`.coinflip`", value="Flips a coin, random answer heads or trails.", inline=True)
        help_all.add_field(name="`.ping`", value="Sends the bots ping in milliseconds.", inline=True)
        help_all.add_field(name="`.join`", value="Banathon joins your voice channel.", inline=True)
        help_all.add_field(name="`.invite`", value="Sends a invite for the bot.", inline=True)
        help_all.add_field(name="`.warn [user] [reason]`", value="Sends a warning to a member.", inline=True)
        help_all.add_field(name="`.kick [user] [reason]`", value="Kicks a member from the server.", inline=True)
        help_all.add_field(name="`.ban [user] [reason]`", value="Bans a member from the server.", inline=True)
        help_all.add_field(name="`.unban [username and tag]`", value="Clears a ban of a member.", inline=True)
        help_all.add_field(name="`.clear [amount/all]`", value="Clears the chat of a text channel.", inline=True)
        help_all.add_field(name="`.reactrole [mesage_id] [emoji] [role]`", value="Adds a role to a member if they react.", inline=True)
        help_all.add_field(name="`.userinfo`", value="Replays the user info of a user.", inline=True)

        await ctx.send(embed=help_all)


# AdminCommands
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    kicked = discord.Embed(
        title="You're kicked",
        description=f"You're kicked from the {ctx.guild} server",
        colour=discord.Colour.from_rgb(250, 250, 0)
    )

    kicked.set_footer(text=f"#Kicked From {ctx.guild}.")
    kicked.set_image(url="https://media.discordapp.net/attachments/619413581145833472/729688446070816788/ezgif-5-945a4fd6a78c.gif?width=622&height=350")
    kicked.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/727967252657471550/1fcacc779f361241eb5505e4de99ed81.png?size=128")
    kicked.set_author(name="Banathon",
                     icon_url="https://cdn.discordapp.com/avatars/727967252657471550/1fcacc779f361241eb5505e4de99ed81.png?size=128")
    kicked.add_field(name="Reason", value=f"{reason}", inline=False)
    kicked.add_field(name="Info", value="If you want more info, please contact our staff.", inline=False)

    await member.send(embed=kicked)
    await member.kick(reason=reason)
    await ctx.send(f"Kicked: {member.mention}")
    print(f"{ctx.author} kicked {member} for {reason} > {ctx.guild}:{ctx.guild.id}")


@bot.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason):
    await ctx.send(f"{member} had been warned")
    warned = discord.Embed(
        title="You're warned",
        description=f"You're warned on the {ctx.guild} server.",
        colour=discord.Colour.from_rgb(250, 250, 0)
    )

    warned.set_footer(text=f"#Warned On {ctx.guild}")
    warned.set_image(url="https://media.discordapp.net/attachments/619413581145833472/729690305648918568/ezgif-5-8f75a4ba685b.gif?width=622&height=350")
    warned.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/727967252657471550/1fcacc779f361241eb5505e4de99ed81.png?size=128")
    warned.set_author(name="Banathon",
                     icon_url="https://cdn.discordapp.com/avatars/727967252657471550/1fcacc779f361241eb5505e4de99ed81.png?size=128")
    warned.add_field(name="Reason", value=f"{reason}", inline=False)
    warned.add_field(name="Info", value="If you want more information, please contact our staff.", inline=False)

    await member.send(embed=warned)
    print(f"{ctx.author} warned {member} for {reason}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    banned = discord.Embed(
        title="You're banned",
        description=f"You're banned from the {ctx.guild} server.",
        colour=discord.Colour.from_rgb(250, 250, 0)
    )

    banned.set_footer(text=f"#Banned From {ctx.guild}")
    banned.set_image(url="https://media.discordapp.net/attachments/619413581145833472/729689453240778882/ezgif-5-27034f09e27b.gif?width=622&height=350")
    banned.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/727967252657471550/1fcacc779f361241eb5505e4de99ed81.png?size=128")
    banned.set_author(name="Banathon",
                     icon_url="https://cdn.discordapp.com/avatars/727967252657471550/1fcacc779f361241eb5505e4de99ed81.png?size=128")
    banned.add_field(name="Reason", value=f"{reason}", inline=False)
    banned.add_field(name="Info", value="If you want more information, please contact our staff.", inline=False)

    await member.send(embed=banned)
    await member.ban(reason=reason)
    await ctx.send(f"Banned: {member.mention}")
    print(f"{ctx.author} banned {member} for {reason} > {ctx.guild}:{ctx.guild.id}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned: {user.mention}")
            print(f"Unbanned: {user} > {ctx.guild}:{ctx.guild.id}")
            try:
                unbanned = discord.Embed(
                    title="Your Unbanned",
                    description=f"Your unbanned from the {ctx.guild} server.",
                    colour=discord.Colour.from_rgb(250, 250, 0)
                )

                unbanned.set_footer(text=f"#Unbanned From {ctx.guild}")
                unbanned.set_thumbnail(
                    url="https://cdn.discordapp.com/avatars/727967252657471550/1fcacc779f361241eb5505e4de99ed81.png?size=128")
                unbanned.set_author(name="Banathon",
                                  icon_url="https://cdn.discordapp.com/avatars/727967252657471550/1fcacc779f361241eb5505e4de99ed81.png?size=128")
                unbanned.add_field(name="General Info", value="Feel free to join back in.\nIf you want more information, you can contact our staff.", inline=False)
                unbanned.add_field(name="Ban Info", value=f"{discord.Guild.bans(user)}", inline=True)

                await user.send(embed=unbanned)
            except TypeError:
                print(f"ERROR: failed sending message to {user}")
        else:
            await ctx.send(f"`{member}` is not banned :banana:")
            print(f"Unban Error: {member} not on banned entry")
            return

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, content):
    if content == "all":
        await ctx.channel.purge()
        await ctx.send("`I have cleared all your messages`:+1:")
        print(f"Cleared all messages in {ctx.channel} > {ctx.guild}:{ctx.guild.id}")
        time.sleep(5)
        await ctx.channel.purge(limit=1)
    else:
        amount = int(content)
        await ctx.channel.purge(limit=amount + 1)
        if amount == 1:
            await ctx.send("`I have cleared 1 message`:+1:")
        else:
            await ctx.send(f"`I have cleared {amount} messages`:+1:")
        print(f"Cleared {amount} messages in {ctx.channel} > {ctx.guild}:{ctx.guild.id}")
        time.sleep(5)
        await ctx.channel.purge(limit=1)


@bot.command()
@commands.has_permissions(manage_messages=True)
async def reactrole(ctx, message_id, emoji, role: discord.Role):
    global reaction_role_message_id
    global reaction_role_emoji
    global reaction_role_role
    reaction_role_role = role
    reaction_role_emoji = emoji
    reaction_role_message_id = message_id
    await ctx.send(f"Added reaction role {emoji}")
    print(f"Added reaction role emoji= '{emoji}' message= '{message_id}' role= '{role}'")

@bot.command()
@commands.has_permissions(administrator=True)
async def displayembed(ctx):
    embed = discord.Embed(
        title = "Title",
        description = "Description",
        colour = discord.Colour.from_rgb(250, 250, 0)
    )

    embed.set_footer(text="#Footer Text")
    embed.set_image(url="https://cdn.discordapp.com/avatars/727967252657471550/1fcacc779f361241eb5505e4de99ed81.png?size=128")
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/476413851525709835/c70e6d748f68d20e14e15959bd0dc0d2.png?size=128")
    embed.set_author(name="Banathon", icon_url="https://cdn.discordapp.com/avatars/727967252657471550/1fcacc779f361241eb5505e4de99ed81.png?size=128")
    embed.add_field(name="Name Field", value="Field Value", inline=False)
    embed.add_field(name="Name Field", value="Field Value", inline=True)
    embed.add_field(name="Name Field", value="Field Value", inline=True)

    await ctx.send(embed=embed)


@tasks.loop(seconds=60)
async def status_change():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(next(status)))


bot.run("NzI3OTY3MjUyNjU3NDcxNTUw.Xv3lgQ.pAbzJB1U9I96gAebehGSS2EEmus")