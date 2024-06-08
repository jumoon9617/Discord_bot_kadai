import discord
import asyncio

client = discord.Client()

kadai_list = []

TOKEN = ''

async def kadaihelp(message):
    str = "command list\n"
    for command in COMMANDS:
        str += "-" * 10 + "\n"
        str += '{}: {}\n'.format("!" + command, COMMANDS[command]["description"])
        str += "使い方: {}\n".format(COMMANDS[command]["use"])
        str += "省略形: {}\n".format(COMMANDS[command]["alias"])
        str += "-" * 10
    await message.channel.send(str)

async def addkadai(message):
    msg = message.content.split(" ")
    try:
        title, deadline, memo = msg[1:]
        
        kadai_list.append({
            "title": title,
            "deadline": deadline,
            "memo": memo
        })
        
        await message.channel.send("課題を追加しました")
    except:
        await message.channel.send("形式が違います")

async def deletekadai(message):
    await print("delete")

async def listkadai(message):
    await print("list")

async def exit(message):
    await print("exit")

COMMANDS = {
    "help":{
        "description": "このヘルプリストの表示",
        "use": "!kadaihelp",
        "alias": "!kh",
        "func": kadaihelp
        },
    "add":{"description": "課題リストへ追加",
        "use": "!addkadai \{タイトル\} \{締め切り\} \{備考\}",
        "alias": "!kh",
        "func": addkadai
        },
    "delete":{"description": "指定課題の削除",
        "use": "!kadaihelp",
        "alias": "!kh",
        "func": deletekadai
        },
    "list":{"description": "このヘルプリストの表示",
        "use": "!kadaihelp",
        "alias": "!kh",
        "func": listkadai
        },
    "exit":{"description": "このヘルプリストの表示",
        "use": "!kadaihelp",
        "alias": "!kh",
        "func": exit
        }
}

@client.event
async def on_ready():
    await print('bot login!')
    
@client.event
async def on_message(message):
    msg = message.contet.split(" ")
    
    if message.author.bot:
        return

    for command in COMMANDS:
        if msg[0] in ["!" + command, COMMANDS[command]["alias"]]:
            await COMMANDS[command]["func"](message)

client.run(TOKEN)
