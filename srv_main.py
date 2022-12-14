import discord 
import os 
import random
from discord.utils import get 
from discord.ext import commands
from dotenv import load_dotenv
import wavelink
load_dotenv()

client = commands.Bot(intents=discord.Intents.all(),command_prefix='/') 

# todo depression

depresssed_env = ["death","suicide","depression","sad","anxious","miserable"]

encourged_resp = [
    "Cheer up !! , you have a day to live ",
    "Dont be sad :sed: sending you hugs !!",
    " 'Just be happy , dont be sad ' - Shade ~ 15/10/22 ",
    "Just be happy atleast you are not a bihari"
]

race = ["bihari","chapri","marwari","gujrati","mulla","muslim","katwa","bihar","bihari","bikhari"]

class Scripting_x_player(wavelink.Player):
    
    def __init__(self):
        super().__init__()
        self.queue = wavelink.Queue()



@client.event 
async def on_ready():
    # print('login succeded in as {}'.format(client))
    client.loop.create_task(connect_nodes())

async def connect_nodes():
    await client.wait_until_ready()
    await wavelink.NodePool.create_node(
        bot=client,host='127.0.0.1',port=2333,password='youshallnotpass'
    )
    

@client.event
async def on_wavelink_node_ready(node: wavelink.Node):
    # print(f'Node: <{node.id}> is ready !')
    print('Node is ready for connection')
    
@client.event
async def on_wavelink_track_end(player: Scripting_x_player, track:wavelink.Track, reason):
    if not player.queue.is_empty:
        next_track = player.queue.get()
        await player.play(next_track)
        
@client.command()
async def disconnect(ctx):
    voice = ctx.voice_client
    if voice:
        await voice.disconnect()
    else:
        await ctx.send("Moron I am not even connected !!")
        
# join the user's channel
@client.command()
async def connect(ctx):
    voice = ctx.voice_client
    try:
        channel = ctx.author.voice.channel
    except AttributeError:
        return await ctx.send("Join a channel first ")
    if not voice:
        await ctx.author.voice.channel.connect(cls=Scripting_x_player())
    else:
        await ctx.send("Idiot I am already in channel ---> {}".format(channel))
        
# play func
@client.command()
async def play(ctx, *, search: wavelink.YouTubeTrack):
    voice = ctx.voice_client
    if not voice :
        script_player = Scripting_x_player()
        voice: Scripting_x_player =  await ctx.author.voice.channel.connect(cls=script_player)
    
    if voice.is_playing():
        voice.queue.put(item=search)
        
        await ctx.send(embed=discord.Embed(
            title=search.title,
            url=search.uri,
            # author=ctx.author,
            description=f"{search.title} has been queued in {voice.channel}"
        ))
        
    else:
        await voice.play(search)
        
        await ctx.send(embed=discord.Embed(
            title=voice.source.title,
            url=voice.source.uri,
            # author=ctx.author,
            description=f"{voice.source.title} is playing in {voice.channel}"
        ))
    

    
@client.command()
async def resume(ctx):
    voice = ctx.voice_client
    if voice:
        if voice.is_paused():
            await voice.resume()
        else:
            await ctx.send("Idiot nothing is paused ")
    else:
        await ctx.send("Moron I am not even connected to a channel")
    
    
    
@client.command()
async def pause(ctx):
    voice = ctx.voice_client
    if voice :
        if voice.is_playing() and not voice.is_paused():
            await voice.pause()
        else:
            await ctx.send("Nothing is playing now idiot !! ")
    else:
        await ctx.send('Moron I am not even connected to a channel')
     
    
@client.command()
async def stop(ctx):
    voice = ctx.voice_client
    if voice:
        if voice.is_playing():
            await voice.stop()
            await ctx.send('Stopping..... the music Bruhh  !!! ')
        
@client.command()
async def skip(ctx):
    voice = ctx.voice_client
    if voice:
        if not voice.is_playing():
            return await ctx.send("Nothing is playing moron!!")
        if voice.queue.is_empty:
            return await voice.stop()
        
        await voice.seek(voice.track.length * 1000)
        if voice.is_paused():
            await voice.resume()
    else:
        await ctx.send("moron connect me to a channel first")
                    
        
client.run('your token')
