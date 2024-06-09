import discord
import asyncio
import sqlite3
# from flask import Flask, request,jsonify

client = discord.Client()

TOKEN = ''

connection = sqlite3.connect("kadai.db")
cursor = connection.cursor()

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
        
        cursor.execute('INSERT INTO kadai_list (title, deadline, memo) VALUES (?, ?, ?)', (title, deadline, memo))
        connection.commit()
        
        await message.channel.send("課題を追加しました")
    except:
        await message.channel.send("形式が違います")

async def deletekadai(message):
    try:
        msg = message.content.split(" ")
        title = msg[1]

        cursor.execute('DELETE FROM kadai_list WHERE title = ?',(title,))
        connection.commit()

        if cursor.rowcount > 0:
            await message.channel.send(f"課題 '{title}' を削除しました")
        else:
            await message.channel.send(f"課題 '{title}' が見つかりませんでした")
    except Exception as e:
        await message.channel.send(f"エラーが発生しました: {e}")

async def listkadai(message):
    cursor.execute('SELECT * FROM kadai_list')
    rows = cursor.fetchall()
    
    if rows:
        res = "現在の課題: \n"
        for row in rows:
            res += f"<{row[1]}>({row[2]}まで): {row[3]}\n"
    else:
        res = "課題はありません"
 
    await message.channel.send(res)

async def exit(message):
    await client.close()

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