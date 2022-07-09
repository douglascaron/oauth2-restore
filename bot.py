import discord, sqlite3, config
from module import opendb, refresh_token, add_user

client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='with new members'))
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')


@client.event
async def on_message(msg):
    if msg.guild == None:
        return

    if msg.author.id == msg.guild.owner_id:
        if msg.content == f"*restore {config.recover_key}":
            await msg.channel.send("restoring...")
            con,cur = opendb()
            cur.execute("SELECT * FROM users;")
            users = cur.fetchall()
            
            for user in list(set(users)):
                try:
                    new_token = await refresh_token(user[1])
                    if new_token != False:
                        cur.execute("UPDATE users SET refresh_token = ? WHERE  id == ?;", (new_token["refresh_token"], user[0]))
                        con.commit()
                        await add_user(new_token["access_token"], msg.guild.id, user[0])
                except:
                    pass
            
            await msg.channel.send("Recovery success")

        if msg.content == "*verifypanel":
            try:
                await msg.delete()
            except:
                pass
            await msg.channel.send(embed=discord.Embed(color=0x32cd32, title="Verify yourself", description=f"To [verify]({config.oauth2_url}) your account please click on the blue verify button and you will instantly recieve your roles."))

    

client.run(config.token)
