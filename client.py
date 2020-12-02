import discord
import json
import random
import time
import os
import aiohttp
import asyncio
from  discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix = ".")
status = cycle(["your commands", ".help to ask for help", "helpful commands"])

client.remove_command("help")

REDDIT_APP_ID = "k3jhvHbGJpQvRA"
REDDIT_APP_SECRET = "TDsbBQ2oHMDSJo7Rxao8MSoW2GM"

rock_paper_scissors = 0
rock_paper_scissors_channel = ""
rock_paper_scissors_play = 0
Embed_make_title = False
Embed_content = ""


#client events
@client.event
async def on_ready():
    status_change.start()
    print("client status= Ready")

@client.event
async def on_member_join(member):
    print(f"{member} has joined server {member.guild}:{member.guild.id}")

@client.event
async def on_member_remove(member):
    print(f"{member} has left server {member.guild}:{member.guild.id}")

@client.event
async def on_guild_join(guild):
    pass

@client.event
async def on_guild_remove(guild):
    pass

@client.event
async def on_command_error(ctx, error):
    print(f"client Command Error: {error}")
    if not isinstance(error, commands.CommandNotFound):
        await ctx.send(f"```java\n{error}\n```")

@client.event
async def on_message(message):
    global rock_paper_scissors, rock_paper_scissors_channel, rock_paper_scissors_play, Embed_make_title, Embed_content
    filter = ["fuck", "kut", "idioot", "godverdomme", "f*ck", "k*t", "idiot", "bitch", "b*tch", "asshole", "*sshole", "assh*le", "*ssh*le", "*diot", "id*ot", "idi*t", "*d*ot", "id**t", "*di*t", "*d**t", 
    "hoer", "homo", "h*mo", "hom*", "h*m*", "tering", "t*ring", "klootzak", "klootz*k", "fck", "btch", "gvd", "f**k", "dick", "d*ck", "cock", "c*ck", "penis", "p*nis", "pen*s", "p*n*s", 
    "sex", "s*x", "porn", "prick", "bastard", "bellend", "gobdaw", "fecker", "ráicleach", "cúl tóna", "aiteann", "salope", "Slut"
    ]

    for word in filter:
        if message.content.count(word) > 0 :
            print("%s has cursed" % (message.author))
            await message.channel.purge(limit=1)
    await client.process_commands(message)

    if Embed_make_title == True:
        content = message.content
        if not content == "What title `do you prefer?`" and content.startswith(".embed") == False:
            await message.channel.purge(limit=3)
            Embed = discord.Embed(
            title=f"{message.content}",
            description=f"{Embed_content}",
            colour=discord.Colour.from_rgb(255, 255, 0),
            )
            Embed.set_footer(text= f"#From {message.author}")
            
            Embed_make_title = False
            await message.channel.send(embed=Embed)
            
    
    if rock_paper_scissors == 1:
        if message.channel == rock_paper_scissors_channel:
            content = message.content
            responses_lose = ["You win! good game.",
            "You win! I can't defeat you.",
            "You got the win, Guess I'm gonna spectate.",
            "You're the winner, congrats!",
            "You won! you're good.",
            "You win! Nice, I knew I lost.",
            "You win! Guess I need to practice more.",
            "You win! I can't beat your skill.",
            "Well, I thick you won.",
            "You won! How is that possible?"]
            responses_draw = ["Draw, good choice",
            "Draw. I bet win I next time!",
            "Draw. your amazing!",
            "Draw. I've never played against anyone this good before!",
            "Draw! Whew, that was close.",
            "Draw! I didn't count on this."]
            responses_win = ["Wow, how did I win!",
            "I win! I really thought you had won.",
            "I win? That's weird you're better than me.",
            "I'm the winner, that was close!",
            "I won, good game!",
            "Seriously, you should have won.",
            "Thats amazing I won!"]

            if "rock" in content or "Rock" in content:
                rock_paper_scissors += 1
                if rock_paper_scissors == 2:
                    rock_paper_scissors = 0
                rock_rock = discord.Embed(
                title=":mountain: vs :mountain:",
                description=f"{random.choice(responses_draw)}",
                colour=discord.Colour.from_rgb(250, 250, 0)
                )
                rock_rock.set_footer(text="#Rock, paper, scissors: Game")
                
                rock_scissors = discord.Embed(
                title=":mountain: vs :scissors:",
                description=f"{random.choice(responses_lose)}",
                colour=discord.Colour.from_rgb(250, 250, 0)
                )
                rock_scissors.set_footer(text="#Rock, paper, scissors: Game")

                rock_paper = discord.Embed(
                title=":mountain: vs :scissors:",
                description=f"{random.choice(responses_win)}",
                colour=discord.Colour.from_rgb(250, 250, 0)
                )
                rock_paper.set_footer(text="#Rock, paper, scissors: Game")
                
                responses_rock_embed = [rock_rock, rock_scissors, rock_paper]
                await message.channel.send(embed=random.choice(responses_rock_embed))
                return
            
            if "paper" in content or "Paper" in content:
                rock_paper_scissors += 1
                if rock_paper_scissors == 2:
                    rock_paper_scissors = 0
                paper_paper = discord.Embed(
                title=":page_facing_up: vs :page_facing_up:",
                description=f"{random.choice(responses_draw)}",
                colour=discord.Colour.from_rgb(250, 250, 0)
                )
                paper_paper.set_footer(text="#Rock, paper, scissors: Game")
                
                paper_rock = discord.Embed(
                title=":page_facing_up: vs :mountain:",
                description=f"{random.choice(responses_lose)}",
                colour=discord.Colour.from_rgb(250, 250, 0)
                )
                paper_rock.set_footer(text="#Rock, paper, scissors: Game")

                paper_scissors = discord.Embed(
                title=":page_facing_up: vs :mountain:",
                description=f"{random.choice(responses_win)}",
                colour=discord.Colour.from_rgb(250, 250, 0)
                )
                paper_scissors.set_footer(text="#Rock, paper, scissors: Game")
                
                responses_rock_embed = [paper_paper, paper_rock, paper_scissors]
                await message.channel.send(embed=random.choice(responses_rock_embed))
                return
            
            if "scissors" in content or "Scissors" in content:
                rock_paper_scissors += 1
                if rock_paper_scissors == 2:
                    rock_paper_scissors = 0
                scissors_scissors = discord.Embed(
                title=":scissors: vs :scissors:",
                description=f"{random.choice(responses_draw)}",
                colour=discord.Colour.from_rgb(250, 250, 0)
                )
                scissors_scissors.set_footer(text="#Rock, paper, scissors: Game")
                
                scissors_paper = discord.Embed(
                title=":scissors: vs :page_facing_up:",
                description=f"{random.choice(responses_lose)}",
                colour=discord.Colour.from_rgb(250, 250, 0)
                )
                scissors_paper.set_footer(text="#Rock, paper, scissors: Game")
                
                scissors_rock = discord.Embed(
                title=":scissors: vs :page_facing_up:",
                description=f"{random.choice(responses_win)}",
                colour=discord.Colour.from_rgb(250, 250, 0)
                )
                scissors_rock.set_footer(text="#Rock, paper, scissors: Game")
                
                responses_rock_embed = [scissors_scissors, scissors_paper, scissors_rock]
                await message.channel.send(embed=random.choice(responses_rock_embed))
                return
                
@client.event
async def convert(ctx, reason):
    reason = await commands.MemberConverter().convert(ctx, reason)

@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    emoji = "🍌"
    reaction_role_message_id = "731938596608540692"

    if reaction_role_message_id == None:
        if emoji == payload.emoji.name:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

            role = discord.utils.get(guild.roles, name="Member")

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



    if f"{message_id}" == reaction_role_message_id:
        if emoji == payload.emoji.name:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

            role = discord.utils.get(guild.roles, name="Member")

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

@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    emoji = "🍌"
    reaction_role_message_id = "731938596608540692"
    if f"{message_id}" == reaction_role_message_id:
        if emoji == payload.emoji.name:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

            role = discord.utils.get(guild.roles, name="Member")

            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await discord.Member.remove_roles(member, role)
                print(f"Removed {role} from {member}")

    if reaction_role_message_id == None:
        if emoji == payload.emoji.name:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

            role = discord.utils.get(guild.roles, name="Member")

            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await discord.Member.remove_roles(member, role)
                print(f"Removed {role} from {member}")


# clientCommands
@client.command()
async def invite(ctx):
    invite = discord.Embed(description="`Invite link` has been send :banana:", colour=discord.Colour.from_rgb(250, 255, 0))
    await ctx.send(embed=invite)
    invite = discord.Embed(
        title="Invite Link:",
        description="https://discord.com/api/oauth2/authorize?client_id=727967252657471550&permissions=8&scope=bot",
        colour=discord.Colour.from_rgb(250, 250, 0)
    )

    invite.set_footer(text="#Banathon Invite Link")
    invite.set_image(url="https://media.discordapp.net/attachments/731575466313384047/733704616579170324/ezgif-5-c742e4b59516.gif?width=640&height=360")
    invite.set_author(name="Banathon Invite", icon_url="https://cdn.discordapp.com/avatars/727967252657471550/ed55927886ccf4368b8f364ead00280c.png?size=128")
    invite.set_thumbnail(url="https://cdn.discordapp.com/avatars/727967252657471550/ed55927886ccf4368b8f364ead00280c.png?size=128")

    await ctx.author.send(embed=invite)
    print(f"An invite link has been send to {ctx.author}")
    
@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! :banana:'s ping is around: `{round(client.latency * 1000)}ms`")
    print(f"{ctx.author} has checked the client ping: {round(client.latency * 1000)}ms")

@client.command()
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

@client.command()
async def coinflip(ctx):
    coin = ["Heads", "Trails"]
    await ctx.send(f"I threw `{random.choice(coin)}` :banana:")

@client.command()
async def rps(ctx, choice=None):
    global rock_paper_scissors, rock_paper_scissors_channel, rock_paper_scissors_play
    if choice is None:
        rps = discord.Embed(
        title="Rock, Paper, Scissors:",
        description="Type rock, paper or scissors to play a fair game!",
        colour=discord.Colour.from_rgb(250, 250, 0)
        )
        rps.set_footer(text="#Rock, paper, scissors")

        await ctx.send(embed=rps)
    
    rock_paper_scissors = 1
    rock_paper_scissors_channel = ctx.channel

@client.command()
async def fox(ctx):
    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://randomfox.ca/floof/") as r:
                data = await r.json()
                embed = discord.Embed(
                    title="A fox for you! Floof!",
                    colour=discord.Colour.from_rgb(255, 255, 0)
                )
                embed.set_image(url=data['image'])
                
                await ctx.send(embed=embed)

@client.command()
async def dog(ctx):
    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://random.dog/woof.json") as r:
                data = await r.json()
                embed = discord.Embed(
                    title="Here is a dog! Woof!",
                    colour=discord.Colour.from_rgb(255, 255, 0)
                )
                embed.set_image(url=data['url'])
                
                await ctx.send(embed=embed)

@client.command(aliases=['8ball'])
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

@client.command()
async def help(ctx, rank=None):
    if rank is None:
        help = discord.Embed(
            colour=discord.Colour.from_rgb(250, 250, 0)
        )

        help.set_footer(text="#Help Command")
        help.set_image(url="https://media.discordapp.net/attachments/731575466313384047/731575678922915840/ezgif-5-3c9c28b0609b.gif?width=770&height=433")
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
        help_admin.add_field(name="`.warn [user] [reason]`", value="Sends a warning to a member.", inline=True)
        help_admin.add_field(name="`.kick [user] [reason]`", value="Kicks a member from the server.", inline=True)
        help_admin.add_field(name="`.ban [user] [reason]`", value="Bans a member from the server.", inline=True)
        help_admin.add_field(name="`.unban [username and tag]`", value="Clears a ban of a member.", inline=True)
        help_admin.add_field(name="`.softban [user]`", value="Bans and unbans a user quickly.", inline=True)
        help_admin.add_field(name="`.clear [amount/all]`", value="Clears the chat of a text channel.", inline=True)
        help_admin.add_field(name="`.embed [message]`", value="Send a embed using the bot.", inline=True)
        help_admin.add_field(name="`.say [message]`", value="Let the bot send a message for you.", inline=True)        
        help_admin.add_field(name="`.mute [user] (channel)`", value="Mutes a user in one/all channel(s)", inline=True)
        help_admin.add_field(name="`.unmute [user] (channel)`", value="Unmutes a user in one/all channel(s)", inline=True)
        help_admin.add_field(name="`.channelmute [channel]`", value="Mutes a channel", inline=True) 
        help_admin.add_field(name="`.channelunmute [channel]`", value="Unmutes a channel", inline=True) 

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
        help_fun.add_field(name="`.invite`", value="Sends a invite for the bot.", inline=True)
        help_fun.add_field(name="`.userinfo`", value="Sends the information of a user.", inline=True)
        help_fun.add_field(name="`.rps`", value="Plays a game of rock, paper, scissors with you.", inline=True)
        help_fun.add_field(name="`.dog`", value="Displays a random image of a dog.", inline=True)
        help_fun.add_field(name="`.fox`", value="Reveals a arbitrary image of a fox.", inline=True)

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
        help_all.add_field(name="`.ban [user] [reason]`", value="Bans a member from the server.", inline=True)
        help_all.add_field(name="`.unban [username and tag]`", value="Clears a ban of a member.", inline=True)
        help_all.add_field(name="`.softban [user]`", value="Bans and unbans a user quickly.", inline=True)
        help_all.add_field(name="`.kick [user] [reason]`", value="Kicks a member from the server.", inline=True)
        help_all.add_field(name="`.mute [user] (channel)`", value="Mutes a user in one/all channel(s)", inline=True)
        help_all.add_field(name="`.unmute [user] (channel)`", value="Unmutes a user in one/all channel(s)", inline=True)
        help_all.add_field(name="`.channelmute [channel]`", value="Mutes a channel", inline=True) 
        help_all.add_field(name="`.channelunmute [channel]`", value="Unmutes a channel", inline=True) 
        help_all.add_field(name="`.warn [user] [reason]`", value="Sends a warning to a member.", inline=True)
        help_all.add_field(name="`.clear [amount/all]`", value="Clears the chat of a text channel.", inline=True)
        help_all.add_field(name="`.8ball [question]`", value="Gives you a random answer to a question.", inline=True)
        help_all.add_field(name="`.coinflip`", value="Flips a coin, random answer heads or trails.", inline=True)
        help_all.add_field(name="`.ping`", value="Sends the bots ping in milliseconds.", inline=True)
        help_all.add_field(name="`.rps`", value="Plays a game of rock, paper, scissors with you.", inline=True)
        help_all.add_field(name="`.invite`", value="Sends a invite for the bot.", inline=True)
        help_all.add_field(name="`.userinfo`", value="Sends the information of a user.", inline=True)
        help_all.add_field(name="`.embed [message]`", value="Send a embed using the bot.", inline=True)
        help_all.add_field(name="`.say [message]`", value="Let the bot send a message for you.", inline=True)
        help_all.add_field(name="`.dog`", value="Displays a random image of a dog.", inline=True)
        help_all.add_field(name="`.fox`", value="Reveals a arbitrary image of a fox.", inline=True)

        await ctx.send(embed=help_all)

# AdminCommands
@client.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, channel: discord.TextChannel=None):
    async with ctx.channel.typing():
        if channel == None:
            for allChannels in ctx.guild.channels:
                await discord.TextChannel.set_permissions(allChannels, member, overwrite=discord.PermissionOverwrite(send_messages=False))
            await ctx.send(f"Muted `{member}`")
        else:
            await discord.TextChannel.set_permissions(channel, member, overwrite=discord.PermissionOverwrite(send_messages=False))
            await ctx.send(f"Muted `{member}` in `{channel}`")

@client.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member, channel: discord.TextChannel=None):
    async with ctx.channel.typing():
        if channel == None:
            for allChannels in ctx.guild.channels:
                await discord.TextChannel.set_permissions(allChannels, member, overwrite=None)
            await ctx.send(f"Unmuted `{member}`")
        else:
            await discord.TextChannel.set_permissions(channel, member, overwrite=None)
            await ctx.send(f"Unmuted `{member}` in `{channel}`")

@client.command()
@commands.has_permissions(manage_messages=True)
async def channelmute(ctx, channel: discord.TextChannel=None):
    async with ctx.channel.typing():
        if channel == None:
            for allMembers in ctx.guild.members:
                await discord.TextChannel.set_permissions(ctx.channel, allMembers, overwrite=discord.PermissionOverwrite(send_messages=False))
                
            await ctx.send(f"Muted `{ctx.channel}`")
        else:
            for allMembers in ctx.guild.members:
                await discord.TextChannel.set_permissions(channel, allMembers, overwrite=discord.PermissionOverwrite(send_messages=False))

            await ctx.send(f"Muted `{ctx.channel}`")

@client.command()
@commands.has_permissions(manage_messages=True)
async def channelunmute(ctx, channel: discord.TextChannel=None):
    async with ctx.channel.typing():
        if channel == None:
            for allMembers in ctx.guild.members:
                await discord.TextChannel.set_permissions(ctx.channel, allMembers, overwrite=None)

            await ctx.send(f"Unmuted `{ctx.channel}`")
        else:
            for allMembers in ctx.guild.members:
                await discord.TextChannel.set_permissions(channel, allMembers, overwrite=None)

            await ctx.send(f"Unmuted `{ctx.channel}`")

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    kicked = discord.Embed(
        title="You're kicked",
        description=f"You're kicked from the {ctx.guild} server",
        colour=discord.Colour.from_rgb(250, 250, 0)
    )

    kicked.set_footer(text=f"#Kicked From {ctx.guild}.")
    kicked.set_image(url="https://media.discordapp.net/attachments/731575466313384047/731575546458406922/ezgif-5-945a4fd6a78c.gif?width=770&height=433")
    kicked.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/727967252657471550/ed55927886ccf4368b8f364ead00280c.png?size=128")
    kicked.set_author(name="Banathon",
                     icon_url="https://cdn.discordapp.com/avatars/727967252657471550/ed55927886ccf4368b8f364ead00280c.png?size=128")
    kicked.add_field(name="Reason", value=f"{reason}", inline=False)
    kicked.add_field(name="Info", value="If you want more info, please contact our staff. You can join back in if you want.", inline=False)

    await member.send(embed=kicked)
    await member.kick(reason=reason)
    await ctx.send(f"Kicked: {member.mention}")
    print(f"{ctx.author} kicked {member} for {reason} > {ctx.guild}:{ctx.guild.id}")

@client.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason):
    await ctx.send(f"{member} had been warned")
    warned = discord.Embed(
        title="You're warned",
        description=f"You're warned on the {ctx.guild} server.",
        colour=discord.Colour.from_rgb(250, 250, 0)
    )

    warned.set_footer(text=f"#Warned On {ctx.guild}")
    warned.set_image(url="https://media.discordapp.net/attachments/731575466313384047/731575588132880424/ezgif-5-8f75a4ba685b.gif?width=770&height=433")
    warned.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/727967252657471550/ed55927886ccf4368b8f364ead00280c.png?size=128")
    warned.set_author(name="Banathon",
                     icon_url="https://cdn.discordapp.com/avatars/727967252657471550/ed55927886ccf4368b8f364ead00280c.png?size=128")
    warned.add_field(name="Reason", value=f"{reason}", inline=False)
    warned.add_field(name="Info", value="If you want more information, please contact our staff.", inline=False)

    await member.send(embed=warned)
    print(f"{ctx.author} warned {member} for {reason}")

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    banned = discord.Embed(
        title="You're banned",
        description=f"You're banned from the {ctx.guild} server.",
        colour=discord.Colour.from_rgb(250, 250, 0)
    )

    banned.set_footer(text=f"#Banned From {ctx.guild}")
    banned.set_image(url="https://media.discordapp.net/attachments/731575466313384047/731575511456940042/ezgif-5-27034f09e27b.gif?width=770&height=433")
    banned.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/727967252657471550/ed55927886ccf4368b8f364ead00280c.png?size=128")
    banned.set_author(name="Banathon",
                     icon_url="https://cdn.discordapp.com/avatars/727967252657471550/ed55927886ccf4368b8f364ead00280c.png?size=128")
    banned.add_field(name="Reason", value=f"{reason}", inline=False)
    banned.add_field(name="Info", value="If you want more information, please contact our staff.", inline=False)

    await member.send(embed=banned)
    await member.ban(reason=reason)
    await ctx.send(f"Banned: {member.mention}")
    print(f"{ctx.author} banned {member} for {reason} > {ctx.guild}:{ctx.guild.id}")

@client.command()
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
                unbanned.set_image(url="https://media.discordapp.net/attachments/731575466313384047/731582587541258340/ezgif-5-2c051b9beafd.gif?width=770&height=433")
                unbanned.set_thumbnail(
                    url="https://cdn.discordapp.com/avatars/727967252657471550/ed55927886ccf4368b8f364ead00280c.png?size=128")
                unbanned.set_author(name="Banathon",
                                  icon_url="https://cdn.discordapp.com/avatars/727967252657471550/ed55927886ccf4368b8f364ead00280c.png?size=128")
                unbanned.add_field(name="General Info", value="Feel free to join back in.\nIf you want more information, you can contact our staff.", inline=False)
                unbanned.add_field(name="Ban Info", value=f"{discord.Guild.bans(user)}", inline=True)

                await user.send(embed=unbanned)
            except TypeError:
                print(f"ERROR: failed sending message to {user}")
        else:
            errors = discord.Embed(dsicription=f"`{member}` is not banned :banana:", colour=discord.Colour.from_rgb(255, 0, 0))
            await ctx.send(embed=errors)
            print(f"Unban Error: {member} not on banned entry")
            return

@client.command()
@commands.has_permissions(ban_members=True)
async def softban(ctx, member: discord.Member, reason=None):
    softbanned = discord.Embed(
    title="You're softbanned",
    description=f"You're softbanned from the {ctx.guild} server.",
    colour=discord.Colour.from_rgb(250, 250, 0)
    )

    softbanned.set_footer(text=f"#Softbanned From {ctx.guild}")
    softbanned.set_image(url="https://media.discordapp.net/attachments/731575466313384047/731581048030363708/ezgif-5-c6f62afa8eae.gif?width=770&height=433")
    softbanned.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/727967252657471550/ed55927886ccf4368b8f364ead00280c.png?size=128")
    softbanned.set_author(name="Banathon",
                     icon_url="https://cdn.discordapp.com/avatars/727967252657471550/ed55927886ccf4368b8f364ead00280c.png?size=128")
    softbanned.add_field(name="Reason", value=f"{reason}", inline=False)
    softbanned.add_field(name="Info", value="If you want more information, please contact our staff. You can join back in if you want.", inline=False)

    await member.send(embed=softbanned)
    await member.ban(reason=reason)
    await ctx.guild.unban(member)
    await ctx.send(f"Softbanned: {member}")
    print(f"{ctx.author} softbanned {member} for {reason} > {ctx.guild}:{ctx.guild.id}")

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, content=None, user: discord.Member = None):
    if content == None:
        await ctx.channel.purge()
        msg = await ctx.send("I have cleared `all your messages`:+1:")
        print(f"Cleared all messages in {ctx.channel} > {ctx.guild}:{ctx.guild.id}")
        time.sleep(3)
        await msg.delete()

    else:
        amount_clear = int(content)
        await ctx.channel.purge(limit=amount_clear + 1)
        if amount_clear == 1:
            msg = await ctx.send("`I have cleared 1 message`:+1:")
            time.sleep(3)
            await msg.delete()
        else:
            msg = await ctx.send(f"`I have cleared {amount_clear} messages`:+1:")
            print(f"Cleared {amount_clear} messages in {ctx.channel} > {ctx.guild}:{ctx.guild.id}")
            time.sleep(3)
            await msg.delete()

@client.command()
@commands.has_permissions(manage_messages=True)
async def embed(ctx, *, message):
    global Embed_make_title, Embed_content
    Embed_make_title = True
    Embed_content = message
    await ctx.send("What title `do you prefer?`")

@client.command()
@commands.has_permissions(manage_messages=True)
async def say(ctx, *, message):
    await ctx.channel.purge(limit=1)
    await ctx.send(f"{message}")

@client.command()
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
    await client.change_presence(status=discord.Status.online, activity=discord.Game("your commands"))

client.run("NzI3OTY3MjUyNjU3NDcxNTUw.XvziVg.fpVN9tbHHOmXWezIEl9usZKycb4")