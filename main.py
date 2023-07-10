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

drem = 201866951683735552

profiles = {}
# options = Options()
# options.add_argument('--headless')
# driver = webdriver.Edge(options=options)

@client.event
async def on_ready():
    global vcTimes, textTimes, constants, textlog_message, voicelog_message, userTimes, nicevoice_message, textlog_messageID, logs_channelID
    global logs_channelID, logsbackup_channelID, textlog_messageID, nicetextlog_messageID, voicelog_messageID, nicevoicelog_messageID
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
    except KeyError as e:
        print(e)
        sys.exit()

    try:
        voicelog_message = await(client.get_channel(logs_channelID).fetch_message(voicelog_messageID))
        #vcTimes = ast.literal_eval(voicelog_message.content)
        vcTimes = {}
        textlog_message = await(client.get_channel(logs_channelID).fetch_message(textlog_messageID))
        textTimes = ast.literal_eval(textlog_message.content)
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
    return
    #updateMessage.start()


# @tasks.loop(seconds=15)
async def updateMessage():
    return
    global textlog_message, voicelog_message, vcTimes
    if client.is_ready():
        textlog_message = await(client.get_channel(logs_channelID).fetch_message(textlog_messageID))
        try:
            if ast.literal_eval(textlog_message.content) != textTimes:
                #print('Updating Text')
                await(textlog_message.edit(content=textTimes))
                await(makeSorted())
            # else:
            #     print(f'nochanges')
        except discord.HTTPException as e:
            print(e.text)

        voicelog_message = await(client.get_channel(logs_channelID).fetch_message(voicelog_messageID))
        for guild in client.guilds:
            for channel in guild.voice_channels:
                for cons in channel.voice_states:
                    #print(f'{getFull(guild.get_member(cons))} total time updated to {vcTimes[getFull(guild.get_member(cons))]} seconds')
                    vcTimes[getFull(guild.get_member(cons))] = round(vcTimes[getFull(guild.get_member(cons))] + time.time() - userTimes[getFull(guild.get_member(cons))], 2)
                    userTimes[getFull(guild.get_member(cons))] = round(time.time(), 2)

        if ast.literal_eval(voicelog_message.content) != vcTimes:
            #print('updating Voice')
            await(voicelog_message.edit(content=vcTimes))
            await(sortVoice())
        # else:
        #     print('No changes to update')



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



def fixList():
    testList = textTimes
    testVoice = vcTimes
    rafes = []
    r = []
    for x in testList.keys():
        if '#2947' in x:
            rafes.append(testList[x])
    print('text')
    print(rafes)

    tt = 0
    tv = 0

    for x in rafes:
        tt = tt + x[0]
    print(f'text {tt}')

    for x in testVoice.keys():
        if '#2947' in x:
            r.append(testVoice[x])
    print('voice')
    print(r)
    tv = sum(r)
    print(tv)




@client.event
async def on_voice_state_update(member, before, after):
    global profiles
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


def getTime():
    current = datetime.datetime.time()
    return f'{current.hour}-{current.minute}'


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
        await(embedTiktok(message))

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
            words = re.findall("[\S]+", message.content)

            for i in range(len(words)):#turns IDs into ints
                if i > 1:
                    words[i] = int(words[i])

            try:
                if len(words) == 3:
                    confirmMessage = await(message.channel.fetch_message(words[2]))
                elif len(words == 4):
                    confirmMessage = await(client.get_channel(words[2]).fetch_message(words[3]))
                if confirmMessage is None:
                    raise discord.HTTPException("Couldnt get message ig")
                replyString = f"The Message?\n{confirmMessage.content}"
                if len(replyString) > 2000:
                    replyEmbed = discord.Embed(title=f"Message {confirmMessage.id}", description=replyString, colour=discord.Colour.darker_grey())
                    await(message.reply(embed=replyEmbed))
                else:
                    await(message.reply(content=replyString))
            except discord.HTTPException as e:
                await(message.reply(content=f"{client.get_user(drem)} come fix your AWFUL bot bro"))
                print(e.text)
        elif message.content == '%usamin hotfix':
            await(hotfix())
        elif message.content == '%usamin backup':
            await(backupLogs())

    if message.content == '%usamin report text':
        textReport = await(client.get_channel(logs_channelID).fetch_message(nicetextlog_messageID))
        await(message.channel.reply(content=textReport.content))
    elif message.content == '%usamin report voice':
        voiceReport = await(client.get_channel(logs_channelID).fetch_message(nicevoicelog_messageID))
        await(message.channel.reply(content=voiceReport.content))

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

async def hotfix():

    await(backupLogs())


    return
    recordTime = datetime.datetime.now()
    message = await(client.get_channel(logs_channelID).fetch_message(1061766911966314536))
    tempDict = ast.literal_eval(message.content)

    sortedTextString = f'```VOICE LOG - 09-Jul 01:40:10\n'
    sortedText = dict(collections.OrderedDict(sorted(tempDict.items(), key=lambda kv: kv[1], reverse=True)))

    for x in sortedText:
        sortedTextString += f'{x}, {sortedText[x]}\n'
    sortedTextString += '```'

    try:
        await(client.get_channel(logsbackup_channelID).send(content=sortedTextString))
    except discord.HTTPException as e:
        print(e.text)

oldText = {'Desti d(๑´ڡ`๑ )b#7588': (4603, '06:01'), 'Dwr3k#0424': (3287, '21:19'), 'Vsel#5099': (3030, '11:54'), 'alan#5202': (2570, '20:14'), 'morstain#6565': (2414, '18:53'), 'Kuro#8574': (1995, '21:09'), 'Fuyubro#4649': (1888, '20:35'), 'hoshi#1892': (1597, '19:58'), 'Framework#8725': (1448, '18:38'), 'レン#2947': (1359, '23:33'), 'レンジ#2947': (1296, '07:10'), 'Moyashi#1187': (1082, '17:53'), 'キョウヤ#2947': (963, '12:19'), 'Olive#4040': (929, '18:40'), 'J12od99#7443': (840, '14:53'), 'W0ps#5810': (735, '03:54'), 'Sweeber#7517': (728, '03:37'), 'Zeroes|Producer-San#8327': (473, '23:34'), 'purin#0011': (465, '12:16'), 'carrot#9332': (320, '20:04'), 'Vsel#4242': (289, '09:06'), 'LolicoreP#0911': (278, '14:03'), 'Autan#3622': (254, '13:12'), 'ramon#7873': (218, '15:11'), 'K1#9503': (206, '01:51'), 'Ushino#1986': (205, '08:38'), 'Amnitoki#1001': (179, '04:08'), 'genm#0790': (161, '13:14'), 'rain#9416': (148, '21:17'), 'nareso#4378': (91, '13:16'), 'kaneda#3677': (71, '18:14'), 'DaMaryP#7517': (69, '18:52'), 'ジャンヌ#2681': (57, '08:04'), 'Yureizan#5692': (43, '05:43'), 'nala9#0': (33, '22:55'), 'sui#8624': (30, '07:48'), 'NotSoBot#9555': (25, '10:40'), 'Gold#5402': (24, '21:17'), 'dwr3k#0': (23, '20:23'), 'morstain#0': (16, '13:38'), 'yori#9776': (13, '17:32'), 'Wesley#5714': (13, '12:26'), 'vsel#0': (12, '21:24'), 'Hibm#6969': (12, '03:46'), 'moyashi45#0': (11, '21:46'), 'm.matsushima#3888': (9, '21:28'), 'destinationmystery#0': (7, '05:03'), 'mayuzumifuyuko#0': (6, '03:23'), '.framework#0': (4, '21:49'), 'kuro765#0': (4, '21:42'), 'mistrcarrot#0': (3, '20:23'), 'koharukoga#0': (2, '20:58'), 'xalan9#0': (2, '16:56'), 'ViciousHarbinger#9618': (2, '00:01'), 'Dooki6#7320': (1, '21:28'), 'yukimisajo#0': (1, '19:54'), '._._._._._._._._._._._._._._._._#0': (1, '17:25'), 'Wanko#6192': (1, '17:11'), 'PiggyTerry#6018': (1, '08:51'), 'huehuehuehuehuehuehuehuehuehue#0': (1, '07:37'), 'z.buki#9910': (1, '07:24'), 'thefuckingvvvvvvv#3226': (1, '06:49'), 'ushino#0': (1, '03:09')}
oldVoice = {'Kuro#8574': 2346555.16, 'Moyashi#1187': 2294539.94, 'Dwr3k#0424': 2195576.78, 'carrot#9332': 1469258.47, 'Desti d(๑´ڡ`๑ )b#7588': 1288278.37, 'J12od99#7443': 1190770.37, 'alan#5202': 823627.82, 'W0ps#5810': 666446.75, 'Framework#8725': 574610.12, 'Vsel#5099': 464618.95, 'Fuyubro#4649': 411770.95, 'レンジ#2947': 297567.93, 'レン#2947': 249108.72, 'キョウヤ#2947': 190655.13, 'yori#9776': 105339.7, 'Amnitoki#1001': 103989.55, 'K1#9503': 94748.64, 'moyashi45#0': 62815.07, 'Ushino#1986': 59667.69, 'weeaboo.trash#0': 54884.96, 'morstain#6565': 52398.54, 'dwr3k#0': 48336.44, 'mistrcarrot#0': 40975.54, 'Vsel#4242': 30603.7, 'hoshi#1892': 19780.53, 'purin#0011': 15878.49, 'j12od99#0': 15179.39, 'ViciousHarbinger#9618': 13552.72, 'Sweeber#7517': 13267.44, 'Wesley#5714': 13025.41, 'nala9#0': 11193.93, 'sierra_sweatshirt#0': 8682.24, 'destinationmystery#0': 8025.77, 'Dooki6#7320': 7732.56, 'm.matsushima#3888': 6533.81, 'Hibm#6969': 5475.8, 'misonoo#0': 5374.48, 'Zeroes|Producer-San#8327': 4355.06, 'LolicoreP#0911': 3544.88, '.framework#0': 3357.13, 'Mysterious Alter Ego Λ#4223': 3312.65, 'genm#0790': 2794.21, 'Autan#3622': 2760.54, 'Yureizan#5692': 1002.42, 'ushino#0': 449.98, 'dooki.3#0': 91.95}
# @tasks.loop(seconds=15)
async def backupLogs():

    recordTime = datetime.datetime.now()
    textEmbed = discord.Embed(title=f'```TEXT LOG - {recordTime.strftime("%d-%b %H:%M")}```', description=f"```{textTimes}```")
    backupChannel = client.get_channel(logsbackup_channelID)

    oldTextEmbed = discord.Embed(title=f'```TEXT LOG - 04-Jul 20:23```', description=f"```{oldText}```")

    try:
        await(backupChannel.send(embed=oldTextEmbed))
    except discord.HTTPException as e:
        print(e.text)

    sortedTextString = '```'
    sortedText = dict(collections.OrderedDict(sorted(oldText.items(), key=lambda kv: kv[1], reverse=True)))
    for x in sortedText:
        sortedTextString += f'{x}, {sortedText[x]}\n'
    sortedTextString += '```'
    sortedTextEmbed = discord.Embed(title=f'```SORTED TEXT LOG - 04-Jul 20:23```', description=sortedTextString)

    try:
        await(backupChannel.send(embed=sortedTextEmbed))
    except discord.HTTPException as e:
        print(e.text)

    sortedOldVoice = dict(collections.OrderedDict(sorted(oldVoice.items(), key=lambda kv: kv[1], reverse=True)))
    deltaedVoice = {k: str(datetime.timedelta(seconds=v))[:len(str(datetime.timedelta(seconds=v)))-4] for k, v in sortedOldVoice.items()}
    niceString = ""
    for x,v in deltaedVoice.items():
        niceString += f"{x}, {v}\n"
    oldVoiceEmbed = discord.Embed(title=f'```VOICE LOG - 09-Jul 01:40```', description=f"```{oldVoice}```")
    sortedOldVoiceEmbed = discord.Embed(title=f'```SORTED VOICE LOG - 09-Jul 01:40```', description=f"```{niceString}```")

    try:
        await(backupChannel.send(embed=oldVoiceEmbed))
        await(backupChannel.send(embed=sortedOldVoiceEmbed))
    except discord.HTTPException as e:
        print(e.text)




    return

    sentText = False
    sentVoice = False
    try:
        textLog = await(client.get_channel(logs_channelID).fetch_message(nicetextlog_messageID))
    except discord.HTTPException as e:
        print(f'Text - {e.text}')
        return



    try:
        await(client.get_channel(logsbackup_channelID).send(content=textTimes))
        await(client.get_channel(logsbackup_channelID).send(content=sortedTextString))
        sentText = True
    except discord.HTTPException as e:
        print(f"Voice - {e.text}")

    sortedVoice = dict(collections.OrderedDict(sorted(vcTimes.items(), key=lambda kv: kv[1], reverse=True)))
    sortedVoiceString = f'```VOICE LOG - {recordTime.strftime("%d-%b %H:%M")}\n'
    for x in sortedVoice:
        sortedVoiceString += f'{x}, {datetime.timedelta(seconds=sortedVoice[x])}\n'
    sortedVoiceString += '```'

    try:
        await(client.get_channel(logsbackup_channelID.send(content=vcTimes)))
        await(client.get_channel(logsbackup_channelID).send(content=sortedVoiceString))
        sentVoice = True
    except discord.HTTPException as e:
        print(e.text)

    try:
        if not sentText:
            raise AssertionError('Text Log backup failed')
        if not sentVoice:
            raise AssertionError('Voice Log backup failed')
    except AssertionError as e:
        print(e)





async def updateConstantPlace():
    m = await(client.get_channel(logs_channelID).fetch_message(1061736393086345296))
    await(m.edit(content=constants))

async def embedInstagram(message):
    instaURL = ''
    for phrase in message.content.split():
        if phrase.__contains__('https://www.instagram.com'):
            instaURL = phrase

    if instaURL == '':
        print('something went wrong with finding the link')
        return
    # print('Detected instagram reel')

    r = requests.get(instaURL)
    response = r.content
    response = response.decode(r.encoding)

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

    try:
        await(message.reply(files=sendFiles))
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
        await(message.reply(file=discord.File(fp=mediaPath)))
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

    ydl_opts = {'paths': {'home': "/TestVideo/"}, 'restrictfilenames': True}
    recordTime = datetime.datetime.now()
    path = f"{recordTime.second}{recordTime.microsecond}"
    ydl_opts['outtmpl'] = f"{path}%(title)s.%(ext)s"

    YoutubeDL(ydl_opts).download(word)
    try:
        for file in os.listdir('Media'):
            if file.__contains__(path):
                await(message.reply(content=discord.File(fp=f"/Media/{path}")))
                return
    except discord.HTTPException as e:
        print(e)
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
    if len(message.content) < 2000:
        await(channel.send(content=message))
    else:
        await(channel.send(content=f"Message too big! ({len(message.content)})"))

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

handler = logging.FileHandler(filename='times.txt', encoding='utf-8', mode='w')
client.run(token=token, log_handler=handler, log_level=logging.DEBUG)
#client.run(token=token)
