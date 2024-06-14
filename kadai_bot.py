import discord
import asyncio
import sqlite3

client = discord.Client(intents=discord.Intents.all())

TOKEN = 'DISCORD_BOT_TOKEN'

connection = sqlite3.connect("kadai.db")
cursor = connection.cursor()


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
        title, deadline, note = msg[1:]
        cursor.execute('INSERT INTO kadai_list (title, deadline, note) VALUES (?, ?, ?)', (title, deadline, note))
        connection.commit()
        
        await message.channel.send("課題を追加しました")
    except Exception as e:
        await message.channel.send(f"送信エラー：{str(e)}")

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
    "kadaihelp":{
        "description": "このヘルプリストの表示",
        "use": "!kadaihelp",
        "alias": "!kh",
        "func": kadaihelp
        },
    "addkadai":{
        "description": "課題リストへ追加",
        "use": "!addkadai \{タイトル\} \{締め切り\} \{備考\}",
        "alias": "!ak",
        "func": addkadai
        },
    "deletekadai":{
        "description": "指定課題の削除",
        "use": "!deletekadai",
        "alias": "!dk",
        "func": deletekadai
        },
    "kadailist":{
        "description": "課題一覧の表示",
        "use": "!kadailist",
        "alias": "!kl",
        "func": listkadai
        },
    "kadaiexit":{
        "description": "ボット機能の終了",
        "use": "!kadaiexit",
        "alias": "!kexit",
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