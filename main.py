import sys

import discord
import datetime
import time
import ast
import collections
import logging
import logging.handlers
from discord.ext import tasks
import random
import requests
import os
import json
import re
from yt_dlp import YoutubeDL

id = 636289011215761461
secret = 'QVO-pFuorq4lfhzumtALs505MGrajikQ'
pub_key = '7c9bfa08c1ed0c3945774d19aefab2a457d50ade636c32ce3421867d978f1189'
token = 'NjM2Mjg5MDExMjE1NzYxNDYx.G5BL9_.cHqoXpl-nmggJBYJ0unDqYjHr_iC2pGJXf9yII'
clientSecret = 'BvKmvZlHPT1jNWAzIJG8a06olXs-4SVR'
perm_num = 8
ouath2_url = 'https://discord.com/api/oauth2/authorize?client_id=636289011215761461&permissions=8&scope=bot'

ignoreNames = ['Nana Abe des', 'SaucyBot', 'Mudae']
ignoreChannels = ['logs', 'modlog', 'shh', 'bot-time', 'mmmm-i-love-manga', 'logs-backup']
jokercarThumb = 'https://cdn.discordapp.com/icons/636290342156500993/14b3a9b21d1be1e0a92a8cf7f4d58063.webp'

jokercarID = 636290342156500993
jokercar2ID = 679154749349560320
wildWestID = 686339689598156843

WWlogs = 1071962029579042887
modChannelID = 710004202293690389
botTimeID = 791781737448472627

botTimeVC = 1061164714958266418

intents = discord.Intents.all()
client = discord.Client(intents=intents)

userTimes = {}
vcTimes = {}
textTimes = {}

constantsID = 1061736393086345296  #id of constants message in #logs
constants = {}


logs_channelID = 1061735975899893850
logsbackup_channelID = -1
textlog_messageID = -1
nicetextlog_messageID = -1
voicelog_messageID = -1
nicevoicelog_messageID = -1
textbackup_channelID = -1
voicebackup_channelID = -1

drem = 201866951683735552

current_nicetextlog_messageID = -1
current_nicevoicelog_messageID = -1

profiles = {}
# options = Options()
# options.add_argument('--headless')
# driver = webdriver.Edge(options=options)

@client.event
async def on_ready():
    global vcTimes, textTimes, constants, textlog_message, voicelog_message, userTimes, nicevoice_message, textlog_messageID, logs_channelID
    global logs_channelID, logsbackup_channelID, textlog_messageID, nicetextlog_messageID, voicelog_messageID, nicevoicelog_messageID, textbackup_channelID, voicebackup_channelID

    runTime = time.time()
    print('Connected to Discord')
    print(f'found channels:')
    print(f'-----------------------------------------------------')
    for guild in client.guilds:
        print(f'{guild.name.upper()}')
        for channel in guild.channels:
            print(f'{channel.name}: {channel.id}')
        print(f'-----------------------------------------------------')

    constantsMessage = await(client.get_channel(logs_channelID).fetch_message(constantsID))
    constants = ast.literal_eval(constantsMessage.content)

    try:
        textlog_messageID = constants['textlog_message_id']
        nicetextlog_messageID = constants['nicetextlog_message_id']
        voicelog_messageID = constants['voicelog_message_id']
        nicevoicelog_messageID = constants['voicelog_message_id']
        logsbackup_channelID = constants['logsbackup_channel_id']
        logs_channelID = constants['logs_channel_id']
        textbackup_channelID = constants['textbackup_channel_id']
        voicebackup_channelID = constants['voicebackup_channel_id']
    except KeyError as e:
        print(e)
        sys.exit()

    try:
        voicelog_message = await(client.get_channel(logs_channelID).fetch_message(voicelog_messageID))
        textlog_message = await(client.get_channel(logs_channelID).fetch_message(textlog_messageID))
        textbackup_channel = client.get_channel(textbackup_channelID)
        voicebackup_channel = client.get_channel(voicebackup_channelID)

        textbackups = [message async for message in textbackup_channel.history(limit=6)]
        voicebackups = [message async for message in voicebackup_channel.history(limit=6)]

        for message in textbackups:
            if message.embeds[0].title.__contains__("```TEXT LOG"):
                textTimes = ast.literal_eval(message.embeds[0].description[3:len(message.embeds[0].description)-3])
                print(f"Using {message.embeds[0].title}")

                # print(message.embeds[0].title)
                # print(message.embeds[0].description[3:len(message.embeds[0].description)-3])
                break
        #print(textTimes)

        for message in voicebackups:
            if message.embeds[0].title.__contains__("```VOICE LOG"):
                vcTimes = ast.literal_eval(message.embeds[0].description[3:len(message.embeds[0].description)-3])
                print(f"Using {message.embeds[0].title}")
                # print(message.embeds[0].title)
                # print(message.embeds[0].description[3:len(message.embeds[0].description)-3])
                break
        #print(vcTimes)
        if textTimes == {} or vcTimes == {}:
            print("Something is wrong so we dont even get starting privileges")
            sys.exit()



        nicetextlog_messageID = await(client.get_channel(logs_channelID).fetch_message(nicetextlog_messageID))
        nicevoice_message = await(client.get_channel(logs_channelID).fetch_message(nicevoicelog_messageID))
    except discord.HTTPException as e:
        print(e.text)
        print('error in setting voice/text things, ending')
        sys.exit()

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
    backupLogs.start()


async def initStats():
    global profiles
    if client.is_ready():
        profileMessage = await(client.get_channel(botTimeID).fetch_message(constants['stats']))
        profiles = ast.literal_eval(profileMessage.content)

        allServersAndMembers = []

        for g in client.guilds:
            if g.id != jokercar2ID:
                tempList = []
                for m in g.members:
                    tempList.append(m.id)
                allServersAndMembers.append(tempList)

        crossovers = set(allServersAndMembers[0]).intersection(*allServersAndMembers[1:])
        #print(crossovers)
        for x in crossovers:
            if x not in profiles:#setup as in name, [serverID], numMessages, voiceTime
                profiles[x] = {'name': discord.Guild.get_member(client.get_guild(wildWestID), x).display_name, jokercarID: (0,0), wildWestID:(0,0)}
        #print(profiles)

        await(profileMessage.edit(content=profiles))


@client.event
async def on_voice_state_update(member, before, after):
    global profiles, userTimes
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

            if member.id in profiles:
                tempDict = profiles[member.id]
                profileMessage = await(client.get_channel(botTimeID).fetch_message(constants['stats']))

                if member.guild.id == wildWestID:
                    tempDict.update(wildWestID = ((tempDict[wildWestID])[0], (tempDict[wildWestID])[1] + round(time.time() - userTimes[getFull(member)], 2)))
                elif member.guild.id == jokercarID:
                    tempDict.update(jokercarID = ((tempDict[jokercarID])[0], (tempDict[jokercarID])[1]+ round(time.time() - userTimes[getFull(member)], 2)))
                await(profileMessage.edit(content=profiles))

        else:
            vcTimes[getFull(member)] = round(time.time()-userTimes[getFull(member)], 2)
            print(f'{getFull(member)} added to list with time {vcTimes[getFull(member)]}')


def getFull(member):
    return f'{member.name}#{member.discriminator}'


@client.event
async def on_message(message):
    global vcTimes, textTimes, voicelog_message, textlog_message, nicetextlog_messageID, userTimes, driver, options, constants, profiles
    global logBackupChannel

    current = datetime.datetime.now()
    currentTime = current.strftime("%H:%M")

    if message.content.__contains__('https://www.instagram.com'):
        await(embedInstagram(message))
    elif message.content.__contains__('https://ifunny.co'):
        await(embedIfunny(message))
    elif message.content.__contains__('https://www.tiktok.com'):
        pass
        #await(embedTiktok(message))

    if message.author.name in ['dwr3k', 'Nana Abe des', 'dooki6']:
        if message.content.__contains__('%usamin mimic'):
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
            await(voicelog_message.edit(content=vcTimes))
            await(message.delete())
        elif message.content.__contains__('%usamin list constant'):
            constantMessage = await(client.get_channel(logs_channelID).fetch_message(constantsID))
            await(message.reply(content=constantMessage.content))
        elif message.content.__contains__('%usamin add constant'):
            words = re.findall("[\S]+", message.content)

            if len(words) != 5 or words[4] not in re.findall("[\d]+", message.content):
                return
            newConstant = int(words[4])
            constants[words[3]] = newConstant#what the hell does this line do (it was very obvious)

            try:
                await(message.reply(content=f'Constant {words[3]}: {constants[words[3]]} added!'))
                await(updateConstants())
                await(message.channel.send(content=constants))
            except discord.HTTPException as e:
                print(e.text)

        elif message.content.__contains__('%usamin add string'):
            words = re.findall("[\S]+", message.content)
            print(len(words))
            if len(words) != 5:
                return

            constants[words[3]] = words[4]
            try:
                await(message.reply(content=f"Constant {words[3]}: {constants[words[3]]} added!"))
                await(updateConstants())
                await(message.channel.send(content=constants))
            except discord.HTTPException as e:
                print(e.text)
        elif message.content.__contains__('%usamin remove'):
            words = re.findall("[\S]+", message.content)

            if words[2] not in constants.keys():
                await(message.reply(content=f'Key {words[2]} doesnt exist!'))
                return

            await(message.reply(content=f'Removed {words[2]}: {constants.pop(words[2])} from constants'))
            await(updateConstants())
            await(message.channel.send(content=constants))
        elif message.content == '%ucn':
            await(updateConstantPlace())
        elif message.content == '%debug':
            await(initStats())
        elif message.content.__contains__('%usamin edit'):
            try:
                words = re.findall("[\S]+", message.content)
                editMessage = await(message.channel.fetch_message(words[2]))
                sentence = ''
                for x in words[3:]:
                    sentence += x + ' '

                await(editMessage.edit(content=sentence.strip()))
                await(message.delete())
            except discord.HTTPException as e:
                await(message.reply(content=e.text))
        elif message.content.__contains__('%usamin confirm'):
            await(confirm(message))
        elif message.content == '%usamin hotfix':
            await(hotfix())
        elif message.content == '%usamin backup':
            await(backupLogs())

    if '%usamin report text' in message.content:
        await(makeReport(type='text', og_message=message, show=message.content))
    elif '%usamin report voice' in message.content:
        await(makeReport(type='voice', og_message=message, show=message.content))


    if message.channel.name not in ignoreChannels and (message.author.name not in ignoreNames):
        if getFull(message.author) not in textTimes:
            textTimes[getFull(message.author)] = 1, f'{currentTime}'
            print(f'added {getFull(message.author)} to textTimes [{textTimes[getFull(message.author)]}]')
        else:
            if textTimes[getFull(message.author)][1] != f'{currentTime}':
                textTimes[getFull(message.author)] = textTimes[getFull(message.author)][0]+1, f'{currentTime}'
                print(f'+1 {getFull(message.author)} at {currentTime} in {message.channel.name} [{textTimes[getFull(message.author)]}]')

                if message.author.id in profiles:
                    print(f'{message.author.id} entering')
                    tempDict = profiles[message.author.id]

                    if message.guild.id == wildWestID:
                        tempDict.update(wildWestID=((tempDict[wildWestID])[0]+1, (tempDict[wildWestID])[1]))
                    elif message.guild.id == jokercarID:
                        tempDict.update(jokercarID=((tempDict[jokercarID])[0]+1, (tempDict[jokercarID])[1]))

async def makeReport(type, og_message, show):
    returnMessage = None
    if type == 'text':
        textbackup_channel = await(client.fetch_channel(textbackup_channelID))
        async for message in textbackup_channel.history(limit=4):
            if 'SORTED TEXT LOG' in message.embeds[0].title:
                returnMessage = message
                break
    elif type == 'voice':
        voicebackup_channel = await(client.fetch_channel(voicebackup_channelID))
        async for message in voicebackup_channel.history(limit=4):
            if 'SORTED VOICE LOG' in message.embeds[0].title:
                returnMessage = message
                break

    if returnMessage is None:
        returnMessage = discord.Message(content='Couldnt find a valid message to report')
        await(og_message.channel.send(returnMessage))
        return

    entries = returnMessage.embeds[0].description.split('\n')
    if 'new' in show:
        entries = list(filter(lambda x: '#0,' in x, entries))
    elif 'old' in show:
        entries = list(filter(lambda x: '#0,' not in x, entries))

    if '```' in entries[0]:
        entries[0] = entries[0][:3]
        entries[len(entries)] = entries[len(entries)][:len(len(entries))]

    descriptionString = '```'
    for x in entries:
        descriptionString += f'{x}\n'
    descriptionString += '```'


    embedTitle = returnMessage.embeds[0].title
    reportEmbed = discord.Embed(title=embedTitle, description=descriptionString)
    await(og_message.channel.send(embed=reportEmbed))











async def confirm(message):
    words = re.findall("[\S]+", message.content)

    for i in range(len(words)):  # turns IDs into ints
        if i > 1:
            words[i] = int(words[i])

    try:
        if len(words) == 3:
            confirmMessage = await(message.channel.fetch_message(words[2]))
            embedTitle = f"Message {confirmMessage.id}"
        elif len(words) == 4:
            confirmMessage = await(client.get_channel(words[2]).fetch_message(words[3]))
            embedTitle = f"Message {words[2]} {words[3]}"
        if confirmMessage is None:
            raise discord.HTTPException("Couldnt get message ig")

        replyEmbed = discord.Embed(title=embedTitle, description=f"```{confirmMessage.content}```", colour=discord.Colour.darker_grey())
        await(message.channel.send(embed=replyEmbed))

        if len(message.embeds) > 0:
            print("saw embeds")
            for embed in message.embeds:
                await(message.channel.send(embed=embed))
    except discord.HTTPException as e:
        await(message.reply(f"{e.text}"))

async def hotfix():
    pass


@tasks.loop(minutes=1)
async def backupLogs():
    if client.is_ready():
        recordTime = datetime.datetime.now()
        textEmbed = discord.Embed(title=f'```TEXT LOG - {recordTime.strftime("%d-%b %H:%M")}```', description=f"```{textTimes}```")

        textBackupChannel = client.get_channel(textbackup_channelID)
        voiceBackupChannel = client.get_channel(voicebackup_channelID)

        textLogs = [message async for message in textBackupChannel.history(limit=6)]
        for message in textLogs:
            if message.embeds[0].title.__contains__("```TEXT LOG"):
                oldTextTime = ast.literal_eval(message.embeds[0].description[3:len(message.embeds[0].description)-3])

        voiceLogs = [message async for message in voiceBackupChannel.history(limit=6)]
        for message in voiceLogs:
            if message.embeds[0].title.__contains__("```VOICE LOG"):
                oldVcTime = ast.literal_eval(message.embeds[0].description[3:len(message.embeds[0].description)-3])


        if textTimes != oldTextTime:
            try:
                await(textBackupChannel.send(embed=textEmbed))
            except discord.HTTPException as e:
                print(e.text)

            sortedTextString = '```'
            sortedText = dict(collections.OrderedDict(sorted(textTimes.items(), key=lambda kv: kv[1], reverse=True)))
            for x in sortedText:
                sortedTextString += f'{x}, {sortedText[x]}\n'
            sortedTextString += '```'
            sortedTextEmbed = discord.Embed(title=f'```SORTED TEXT LOG - {recordTime.strftime("%d-%b %H:%M")}```', description=sortedTextString)

            try:
                await(textBackupChannel.send(embed=sortedTextEmbed))
            except discord.HTTPException as e:
                print(e.text)

        for guild in client.guilds:
            for channel in guild.voice_channels:
                for cons in channel.voice_states:
                    vcTimes[getFull(guild.get_member(cons))] = round(vcTimes[getFull(guild.get_member(cons))] + time.time() - userTimes[getFull(guild.get_member(cons))], 2)
                    userTimes[getFull(guild.get_member(cons))] = round(time.time(), 2)

        deltaedVoice = {k: str(datetime.timedelta(seconds=v))[:len(str(datetime.timedelta(seconds=v)))-4] for k, v in vcTimes.items()}
        niceString = ""
        for x,v in deltaedVoice.items():
            niceString += f"{x}, {v}\n"
        voiceEmbed = discord.Embed(title=f'```VOICE LOG - {recordTime.strftime("%d-%b %H:%M")}```', description=f"```{vcTimes}```")
        sortedVoiceEmbed = discord.Embed(title=f'```SORTED VOICE LOG - {recordTime.strftime("%d-%b %H:%M")}```', description=f"```{niceString}```")


        if vcTimes != oldVcTime:
            try:
                await(voiceBackupChannel.send(embed=voiceEmbed))
                await(voiceBackupChannel.send(embed=sortedVoiceEmbed))
            except discord.HTTPException as e:
                print(e.text)
        return

        try:
            txtlog_message = await(client.get_channel(logs_channelID).fetch_message(textlog_messageID))
            await(txtlog_message.edit(embed=textEmbed))
        except discord.HTTPException as e:
            print(textlog_messageID)
            print(f"txtlog_message:\n{e.text}")
            sys.exit()

        try:
            nicetxtlog_message = await(client.get_channel(logs_channelID).fetch_message(nicetextlog_messageID))
            await(nicetxtlog_message.edit(embed=sortedTextEmbed))
        except discord.HTTPException as e:
            print(nicetxtlog_message)
            print(f"nicetxtlog_message:\n{e.text}")
            sys.exit()
        try:
            vclog_message = await(client.get_channel(logs_channelID).fetch_message(voicelog_messageID))
            await(vclog_message.edit(embed=voiceEmbed))
        except discord.HTTPException as e:
            print(voicelog_messageID)
            print(f"vclog_message:\n{e.text}")
            sys.exit()

        try:
            nicevclog_message = await(client.get_channel(logs_channelID).fetch_message(nicevoicelog_messageID))
            await(nicevclog_message.edit(embed=sortedVoiceEmbed))
        except discord.HTTPException as e:
            print(nicevclog_message)
            print(f"nicevclog_message:\n{e.text}")
            sys.exit()

        if None in [txtlog_message, nicetxtlog_message, vclog_message, nicevclog_message]:
            print('couldnt')
            await(client.get_channel(logsbackup_channelID).send(message=f"@dwr3k#0 something has gone wrong"))
            return
        else:
            print('yatta')
    else:
        print("Client isnt ready")




async def updateConstantPlace():
    m = await(client.get_channel(logs_channelID).fetch_message(1061736393086345296))
    await(m.edit(content=constants))

async def embedInstagram(message):
    instaURL = ''
    for phrase in message.content.split():
        if phrase.__contains__('https://www.instagram.com'):
            instaURL = phrase

    print(instaURL)
    if instaURL == '':
        print('something went wrong with finding the link')
        return
    # print('Detected instagram reel')

    r = requests.get(instaURL)
    #print(r)
    response = r.content
    response = response.decode(r.encoding)
    #print(response)


    urls = re.findall(r'("url":"https:\\\/\\\/scontent.+?})|("contentUrl":"https:\\\/\\\/scontent.+?")', response)
    for i in range(len(urls)):
        if urls[i][0] != '':  # url match == picture
            temp = urls[i][0]
            temp = temp[7:len(temp) - 2]
            temp = temp.replace("\\", "")
            urls[i] = temp
        elif urls[i][1] != '':  # contentUrl match == video
            temp = urls[i][1]
            temp = temp[14:len(temp) - 1]
            temp = temp.replace("u0025", "%")
            temp = temp.replace("\\", "")
            urls[i] = temp
        else:
            print('this sure was unexpected')

    if len(urls) == 1 and '.jpg' in urls[0]:  # Only a single picture so avoid duplicate embed
        return

    sendFiles = []
    for url in urls:
        mediaPath = f'Media/{random.randint(1, 123456789)}'
        if '.jpg' in url:
            r = requests.get(url, stream=True)
            with open(f"{mediaPath}.jpg", 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            sendFiles.append(discord.File(fp=f'{mediaPath}.jpg'))
        else:
            r = requests.get(url, stream=True)
            with open(f"{mediaPath}.mp4", 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            sendFiles.append(discord.File(fp=f'{mediaPath}.mp4'))

    if len(sendFiles) == 0:
        drem_member = client.get_guild(jokercarID).get_member(drem)

        #await(message.reply(content="Broke bum tf you tryna make me post"))
        await(message.reply(content=f"Instagram changed their api and broke this feature and {drem_member.mention} hasnt bothered to fix this yet"))
        await(message.channel.send(content="<a:uzuSpin:727951359428657303> <a:uzuSpin:727951359428657303> <a:uzuSpin:727951359428657303>"))
        print(instaURL)
        print(urls)
        print(r)
        print(response)
    else:
        try:
            await(message.reply(files=sendFiles, mention_author=False))
            for file in os.listdir('Media'):
                os.remove(f'Media\\{file}')
        except discord.HTTPException as funny:
            print('something hilarious happened')
            print(funny.status)
            print(funny.code)
            print(funny.text)
            print(instaURL)
            print(urls)
            for x in sendFiles:
                print(x.filename)

            await(message.reply(content=f'Can\'t embed, {funny.text} (yikes!)'))


async def embedIfunny(message):

    ifunnyURL = ''
    for phrase in message.content.split():
        if phrase.__contains__('https://ifunny.co/video/'):
            ifunnyURL = phrase

    if ifunnyURL == '':
        print('Cant find ifunny link')
        return

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'}

    r = requests.get(url=ifunnyURL, headers=headers)
    response = r.content.decode(r.encoding)

    urls = re.findall(r'(content="https://img\.ifunny\.co/videos/.+?\.mp4")', response)
    cleaned = urls[0]
    cleaned = (cleaned[9:len(cleaned) - 1]).strip()

    mediaPath = f'Media/{random.randint(1, 1234567)}.mp4'
    r = requests.get(cleaned, stream=True)
    with open(mediaPath, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    try:
        await(message.reply(file=discord.File(fp=mediaPath), mention_author=False))
        for file in os.listdir('Media'):
            os.remove(f'Media\\{file}')
    except discord.HTTPException as funny:
        print('something hilarious happened')
        print(funny.status)
        print(funny.code)
        print(funny.text)
        print(ifunnyURL)
        print(urls)

        await(message.reply(content=f'Can\'t embed, {funny.text} (yikes!)'))

async def embedTiktok(message):
    words = re.findall("[\S]+", message.content)
    url = ""

    for word in words:
        if word.__contains__("https://www.tiktok.com"):
            url = word
            pass

    ydl_opts = {'paths': {'home': "Media/"}, 'restrictfilenames': True}
    recordTime = datetime.datetime.now()
    path = f"{recordTime.second}{recordTime.microsecond}"
    ydl_opts['outtmpl'] = f"{path}%(title)s.%(ext)s"

    YoutubeDL(ydl_opts).download(url)
    try:
        for file in os.listdir('Media'):
            if file.__contains__(path):
                await(message.reply(file=discord.File(fp=f"Media/{file}")))

    except discord.HTTPException as e:
        print(e)
        if e.status == 413:
            await(message.reply(content="File is too big!"))
        else:
            await(message.reply(content="Something went wrong and its probably not my fault"))

async def makeSorted():
    currentTime = datetime.datetime.now()
    sortedText = dict(collections.OrderedDict(sorted(textTimes.items(), key=lambda kv: kv[1], reverse=True)))
    sortedTextString = f'```LAST UPDATED {currentTime.strftime("%H:%M:%S")}\n'
    for x in sortedText:
        sortedTextString += f'{x}, {sortedText[x]}\n'
    sortedTextString += '```'
    await(nicetextlog_messageID.edit(content=sortedTextString))


async def sortVoice():
    currentTime = datetime.datetime.now()
    sortedVoice = dict(collections.OrderedDict(sorted(vcTimes.items(), key=lambda kv: kv[1], reverse=True)))
    sortedVoiceString = f'```LAST UPDATED {currentTime.strftime("%H:%M:%S")}\n'
    for x in sortedVoice:
        sortedVoiceString += f'{x}, {datetime.timedelta(seconds=sortedVoice[x])}\n'
    sortedVoiceString += '```'
    await(nicevoice_message.edit(content=sortedVoiceString))


async def mimic(channel, message):

    try:
        if len(message) < 2000:
            await(channel.send(content=message))
        else:
            await(channel.send(content=f"Message too big! ({len(message)})"))
    except discord.HTTPException as e:
        print(e.text)

async def updateConstants():
    global constants
    constants = dict(collections.OrderedDict(sorted(constants.items(), key=lambda kv: kv[0])))
    message = await(client.get_channel(logs_channelID).fetch_message(constantsID))
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
async def on_presence_update(before, after):
    if before.id == drem and after.status == 'offline':
        print("This man went offline")
        await(client.get_channel(botTimeID).send(content=f"Ain't no waaaaaaaaaaaaaaaaaay this mf {client.get_user(drem).mention} is offline rn"))



@client.event
async def on_message_delete(message):

    currentTime = datetime.datetime.now()
    timestamp = f'{currentTime.month}/{currentTime.day}/{currentTime.year} {currentTime.hour}:{currentTime.minute}'

    if message.channel.guild.id == wildWestID: #wildwest
        channel = client.get_channel(WWlogs)
    elif message.channel.guild.id == jokercarID:
        channel = client.get_channel(modChannelID)  # currently id for bot-time

    if message.author.name not in ignoreNames and message.channel.name not in ignoreChannels:
        deleteEmbed = discord.Embed(title=f'Message Deleted in #{message.channel.name}', colour=discord.Colour.gold())
        deleteEmbed.set_thumbnail(url=message.author.display_avatar)
        if message.content != '':
            deleteEmbed.add_field(name='Message Content', value=f'```{message.content}```', inline=False)
        pics = ''
        for i in message.attachments:
            pics += f'{i.proxy_url}\n'
        deleteEmbed.add_field(name='Attachments', value=pics.strip(), inline=False)
        deleteEmbed.add_field(name='Message Author', value=f'{message.author.mention}', inline=False)
        deleteEmbed.set_footer(text=f'{message.author.name}#{message.author.discriminator} • {timestamp}')
        await channel.send(embed=deleteEmbed)


@client.event
async def on_message_edit(before, after):
    currentTime = datetime.datetime.now()
    timestamp = f'{currentTime.month}/{currentTime.day}/{currentTime.year} {currentTime.hour}:{currentTime.minute}'

    if before.channel.guild.id == wildWestID:  # wildwest
        channel = client.get_channel(WWlogs)
    elif before.channel.guild.id == jokercarID:
        channel = client.get_channel(modChannelID)  # currently id for bot-time

    oldAttach = ''
    newAttach = ''
    for i in before.attachments:
        oldAttach += f'{i.proxy_url}\n'
    for i in after.attachments:
        newAttach += f'{i.proxy_url}\n'
    oldAttach = oldAttach.strip()
    newAttach = newAttach.strip()

    if before.content != after.content and before.author.name not in ignoreNames:
        editEmbed = discord.Embed(title=f'Message Updated in #{before.channel.name}', colour=discord.Colour.brand_green())
        editEmbed.set_thumbnail(url=before.author.display_avatar)
        editEmbed.add_field(name='Old Message', value=f'```{before.content}```', inline=False)
        if oldAttach != newAttach:
            editEmbed.add_field(name='Old Attachments', value=oldAttach, inline=False)
        editEmbed.add_field(name='New message', value=f'```{after.content}```', inline=False)
        if oldAttach != newAttach:
            editEmbed.add_field(name='New Attachments', value=newAttach, inline=False)
        else:
            editEmbed.add_field(name="Attachments", value=oldAttach, inline=False)
        editEmbed.add_field(name='Message Author', value=f'{before.author.mention}', inline=False)
        editEmbed.set_footer(text=f'{before.author.name}#{before.author.discriminator} • {timestamp}')
        await channel.send(embed=editEmbed)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='newLog.log',
    encoding='utf-8',
    maxBytes=3 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

handler = logging.FileHandler(filename='discordLogs.log', encoding='utf-8', mode='w')
client.run(token=token, log_handler=handler, log_level=logging.DEBUG)
#client.run(token=token)
