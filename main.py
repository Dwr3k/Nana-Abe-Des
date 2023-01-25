import discord
import datetime
import time
import ast
import collections
import logging
import logging.handlers
from discord.ext import tasks

id = 636289011215761461
secret = 'QVO-pFuorq4lfhzumtALs505MGrajikQ'
pub_key = '7c9bfa08c1ed0c3945774d19aefab2a457d50ade636c32ce3421867d978f1189'
token = 'NjM2Mjg5MDExMjE1NzYxNDYx.G5BL9_.cHqoXpl-nmggJBYJ0unDqYjHr_iC2pGJXf9yII'
clientSecret = 'BvKmvZlHPT1jNWAzIJG8a06olXs-4SVR'
perm_num = 8
ouath2_url = 'https://discord.com/api/oauth2/authorize?client_id=636289011215761461&permissions=8&scope=bot'

ignoreNames = ['Nana Abe des', 'SaucyBot', 'Mudae']
ignoreChannels = ['logs', 'modlog', 'shh', 'bot-time', 'mmmm-i-love-manga']
jokercarThumb = 'https://cdn.discordapp.com/icons/636290342156500993/14b3a9b21d1be1e0a92a8cf7f4d58063.webp'

jokercarID = 636290342156500993
jokercar2ID = 679154749349560320
wildWestID = 686339689598156843

modChannelID = 710004202293690389
botTimeID = 791781737448472627

botTimeVC = 1061164714958266418

intents = discord.Intents.all()
client = discord.Client(intents=intents)

userTimes = {}
vcTimes = {}
textTimes = {}

constantsID = 1061435230214438932  #id of constants message in #botchannel
constants = {}

logsID = 1061735975899893850
textID = 1061738499159638186
voiceID = 1061766911966314536
niceTextID = 1065534601558249573
niceVoiceID = 1066245140894732288

global textMessage, voiceMessage, niceTextMessage, niceVoiceMessage


@client.event
async def on_ready():
    global vcTimes, textTimes, constants, textMessage, voiceMessage, userTimes, niceTextMessage, niceVoiceMessage
    runTime = time.time()
    print('Connected to Discord')
    print(f'found channels:')
    print(f'-----------------------------------------------------')
    for guild in client.guilds:
        print(f'{guild.name.upper()}')
        for channel in guild.channels:
            print(f'{channel.name}: {channel.id}')
        print(f'-----------------------------------------------------')

    constantsMessage = await(client.get_channel(botTimeID).fetch_message(constantsID))
    constants = ast.literal_eval(constantsMessage.content)
    voiceMessage = await(client.get_channel(logsID).fetch_message(voiceID))
    vcTimes = ast.literal_eval(voiceMessage.content)
    textMessage = await(client.get_channel(logsID).fetch_message(textID))
    textTimes = ast.literal_eval(textMessage.content)
    niceTextMessage = await(client.get_channel(logsID).fetch_message(niceTextID))
    niceVoiceMessage = await(client.get_channel(logsID).fetch_message(niceVoiceID))

    print('Checking voice connections:')
    print(f'-----------------------------------------------------')
    for guild in client.guilds:
        print(f'{guild.name.upper()} {guild.id}:')
        for channel in guild.voice_channels:
            for cons in channel.voice_states:
                #print(getFull(guild.get_member(cons)))
                if getFull(guild.get_member(cons)) in vcTimes:
                    print(f'Found {getFull(guild.get_member(cons))} already in VC, starting timer')
                    userTimes[getFull(guild.get_member(cons))] = round(time.time(), 2)
                else:
                    print(f'Found {getFull(guild.get_member(cons))} already in VC and is (somehow) not in the list, starting timer')
                    userTimes[getFull(guild.get_member(cons))] = round(time.time(), 2)
                    vcTimes[getFull(guild.get_member(cons))] = 0
        print(f'-----------------------------------------------------')


@client.event
async def setup_hook():
    updateMessage.start()


@tasks.loop(minutes=1)
async def updateMessage():
    global textMessage, voiceMessage, vcTimes
    if client.is_ready():
        textMessage = await(client.get_channel(logsID).fetch_message(textID))
        if ast.literal_eval(textMessage.content) != textTimes:
            #print('Updating Text')
            await(textMessage.edit(content=textTimes))
            await(makeSorted())
        # else:
        #     print(f'nochanges')

        voiceMessage = await(client.get_channel(logsID).fetch_message(voiceID))
        for guild in client.guilds:
            for channel in guild.voice_channels:
                for cons in channel.voice_states:
                    #print(f'{getFull(guild.get_member(cons))} total time updated to {vcTimes[getFull(guild.get_member(cons))]} seconds')
                    vcTimes[getFull(guild.get_member(cons))] = round(vcTimes[getFull(guild.get_member(cons))] + time.time() - userTimes[getFull(guild.get_member(cons))], 2)
                    userTimes[getFull(guild.get_member(cons))] = round(time.time(), 2)

        if ast.literal_eval(voiceMessage.content) != vcTimes:
            #print('updating Voice')
            await(voiceMessage.edit(content=vcTimes))
            await(sortVoice())
        # else:
        #     print('No changes to update')


@client.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        if getFull(member) not in vcTimes:
            vcTimes[getFull(member)] = 0
        userTimes[getFull(member)] = round(time.time(), 2)

        print(f'{member.name}#{member.discriminator} went from {before.channel} to {after.channel} in {after.channel.guild.name}')

    if after.channel is None and before.channel is not None:
        print(f'{member.name}#{member.discriminator} went from {before.channel} to {after.channel} in {before.channel.guild.name}')
        print(f'{member.name}#{member.discriminator} was in {before.channel} for {round(time.time() - userTimes[getFull(member)], 2)} seconds')

        if getFull(member) in vcTimes:
            vcTimes[getFull(member)] = round(vcTimes[getFull(member)] + time.time()-userTimes[getFull(member)], 2)
            print(f'{getFull(member)} total time updated to {vcTimes[getFull(member)]} seconds')
        else:
            vcTimes[getFull(member)] = round(time.time()-userTimes[getFull(member)], 2)
            print(f'{getFull(member)} added to list with time {vcTimes[getFull(member)]}')


def getFull(member):
    return f'{member.name}#{member.discriminator}'


def getTime():
    current = datetime.datetime.time()
    return f'{current.hour}-{current.minute}'


@client.event
async def on_message(message):
    global vcTimes, textTimes, voiceMessage, textMessage, niceTextMessage, userTimes

    current = datetime.datetime.now()
    currentTime = current.strftime("%H:%M")

    if message.author.name in ['Dwr3k', 'Nana Abe des', 'Dooki6']:
        if message.content == '%usamin textclear':
            textTimes = {}
            await(message.channel.last_message.delete())
            await(message.channel.send(content='Change da world, goodbye forever~'))
            await(message.channel.last_message.delete(delay=3))
            await(textMessage.edit(content=textTimes))
        elif message.content == '%usamin voiceclear':
            vcTimes = {}
            await(message.channel.last_message.delete())
            await(message.channel.send(content='Change da world, goodbye forever~'))
            await(message.channel.last_message.delete(delay=3))
            await(voiceMessage.edit(content=vcTimes))
        elif message.content.__contains__('%usamin mimic'):
            await(mimic(message.channel, message.content[13:]))
            await(message.delete())
        elif message.content == '%usamin record':
            for guild in client.guilds:
                #print(f'{guild.name} {guild.id}\n')
                for channel in guild.voice_channels:
                    for cons in channel.voice_states:
                        #print(getFull(guild.get_member(cons)))
                        if getFull(guild.get_member(cons)) in vcTimes:
                            print(f'{getFull(guild.get_member(cons))} total time updated to {vcTimes[getFull(guild.get_member(cons))]} seconds')
                            vcTimes[getFull(guild.get_member(cons))] = round(vcTimes[getFull(guild.get_member(cons))] + time.time() - userTimes[getFull(guild.get_member(cons))], 2)
                        else:
                            vcTimes[getFull(guild.get_member(cons))] = round(time.time() - userTimes[getFull(guild.get_member(cons))], 2)
                            print(f'{getFull(guild.get_member(cons))} added to list with time {vcTimes[getFull(guild.get_member(cons))]}')
                        userTimes[getFull(guild.get_member(cons))] = round(time.time(), 2)
            await(voiceMessage.edit(content=vcTimes))
            await(message.delete())
        elif message.content == '%usamin ora':
            resetMessage = await(client.get_channel(709263987379798097).fetch_message(1065855899886944256))
            vcTimes = ast.literal_eval(resetMessage.content)
            await(voiceMessage.edit(content=vcTimes))
        elif message.content == '%usamin report voice':
            await(message.channel.send(content=niceVoiceMessage.content))
        elif message.content == '%usamin report text':
            await(message.channel.send(content=niceTextMessage.content))

    if message.channel.name not in ignoreChannels and (message.author.name not in ignoreNames):
        if getFull(message.author) not in textTimes:
            textTimes[getFull(message.author)] = 1, f'{currentTime}'
            print(f'added {getFull(message.author)} to textTimes [{textTimes[getFull(message.author)]}]')

        else:
            if textTimes[getFull(message.author)][1] != f'{currentTime}':
                textTimes[getFull(message.author)] = textTimes[getFull(message.author)][0]+1, f'{currentTime}'
                print(f'+1 {getFull(message.author)} at {currentTime} in {message.channel.name} [{textTimes[getFull(message.author)]}]')


async def makeSorted():
    currentTime = datetime.datetime.now()
    sortedText = dict(collections.OrderedDict(sorted(textTimes.items(), key=lambda kv: kv[1], reverse=True)))
    sortedTextString = f'```LAST UPDATED AT {currentTime.strftime("%H:%M:%S")}\n'
    for x in sortedText:
        sortedTextString += f'{x}, {sortedText[x]}\n'
    sortedTextString += '```'
    await(niceTextMessage.edit(content=sortedTextString))


async def sortVoice():
    currentTime = datetime.datetime.now()
    sortedVoice = dict(collections.OrderedDict(sorted(vcTimes.items(), key=lambda kv: kv[1], reverse=True)))
    sortedVoiceString = f'```LAST UPDATED AT {currentTime.strftime("%H:%M:%S")}\n'
    for x in sortedVoice:
        sortedVoiceString += f'{x}, {datetime.timedelta(seconds=sortedVoice[x])}\n'
    sortedVoiceString += '```'
    await(niceVoiceMessage.edit(content=sortedVoiceString))


async def mimic(channel, message):
    await(channel.send(content=message))


async def updateConstants():
    channel = client.get_channel(constants['bottimeID'])
    message = await(channel.fetch_message(constantsID))
    await(message.edit(content=constants))


@client.event
async def on_member_join(member):
    if member.guild.id == jokercarID:
        currentTime = datetime.datetime.now()
        timestamp = f'{currentTime.month}/{currentTime.day}/{currentTime.year} {currentTime.hour}:{currentTime.minute}'
        channel = client.get_channel(modChannelID)  # currently id for bot-time

        joinEmbed = discord.Embed(title=f'Member {member.name}#{member.discriminator} joined', colour=discord.Colour.purple())
        joinEmbed.set_thumbnail(url=member.display_avatar)
        joinEmbed.add_field(name='Message Author', value=f'{member.mention}', inline=False)
        joinEmbed.set_footer(text=f'{member.name}#{member.discriminator} • {timestamp}')
        await channel.send(embed=joinEmbed)


@client.event
async def on_member_remove(member):
    if member.guild.id == jokercarID:
        currentTime = datetime.datetime.now()
        timestamp = f'{currentTime.month}/{currentTime.day}/{currentTime.year} {currentTime.hour}:{currentTime.minute}'
        channel = client.get_channel(modChannelID)  # currently id for bot-time

        leaveEmbed = discord.Embed(title=f'Member {member.name}#{member.discriminator} removed', colour=discord.Colour.red())
        leaveEmbed.set_thumbnail(url=member.display_avatar)
        leaveEmbed.add_field(name='Message Author', value=f'{member.mention}', inline=False)
        leaveEmbed.set_footer(text=f'{member.name}#{member.discriminator} • {timestamp}')
        await channel.send(embed=leaveEmbed)


@client.event
async def on_message_delete(message):
    if message.guild.id == jokercarID:
        currentTime = datetime.datetime.now()
        timestamp = f'{currentTime.month}/{currentTime.day}/{currentTime.year} {currentTime.hour}:{currentTime.minute}'
        channel = client.get_channel(modChannelID)  # currently id for bot-time

        if message.author.name not in ignoreNames and message.channel.name not in ignoreChannels:
            deleteEmbed = discord.Embed(title=f'Message Deleted in #{message.channel.name}', colour=discord.Colour.gold())
            deleteEmbed.set_thumbnail(url=message.author.display_avatar)
            deleteEmbed.add_field(name='Message Content', value=f'```{message.content}```', inline=False)
            deleteEmbed.add_field(name='Message Author', value=f'{message.author.mention}', inline=False)
            deleteEmbed.set_footer(text=f'{message.author.name}#{message.author.discriminator} • {timestamp}')
            await channel.send(embed=deleteEmbed)


@client.event
async def on_message_edit(before, after):
    if before.guild.id == jokercarID:
        currentTime = datetime.datetime.now()
        timestamp = f'{currentTime.month}/{currentTime.day}/{currentTime.year} {currentTime.hour}:{currentTime.minute}'
        channel = client.get_channel(modChannelID)

        if before.content != after.content and before.author.name not in ignoreNames:
            editEmbed = discord.Embed(title=f'Message Updated in #{before.channel.name}', colour=discord.Colour.brand_green())
            editEmbed.set_thumbnail(url=before.author.display_avatar)
            editEmbed.add_field(name='Old Message', value=f'```{before.content}```', inline=False)
            editEmbed.add_field(name='New message', value=f'```{after.content}```', inline=False)
            editEmbed.add_field(name='Message Author', value=f'{before.author.mention}', inline=False)
            editEmbed.set_footer(text=f'{before.author.name}#{before.author.discriminator} • {timestamp}')
            await channel.send(embed=editEmbed)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

#handler = logging.FileHandler(filename='times.txt', encoding='utf-8', mode='w')
client.run(token=token, log_handler=handler, log_level=logging.DEBUG)



