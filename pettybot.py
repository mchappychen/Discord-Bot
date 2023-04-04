
import discord, random, asyncio,requests, aiohttp, io, calendar, json, time
from datetime import datetime

CLIENT_TOKEN = "Put your bot client-token here"

#Create client variable
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents,max_messages=None,heartbeat_timeout=180,)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    #Puts 'Watching !help' as custom status
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="!help"))

#this activates whenever it sees a message
@client.event
async def on_message(message):

    #ignore our own bot messages
    if message.author == client.user:
        return

    if message.content == '!help':
        await message.channel.send('!guess - guess a number from 1 to 10\n!weather - get Middletown weather\n!yomomma - get a yomomma joke\n!ask - ask a question for chatgpt')

    elif message.content.startswith('!guess'):
        await message.channel.send('Guess the number between 1 and 10 within 5 seconds')

        def is_correct(m):
            return m.author == message.author and m.content.isdigit()

        answer = random.randint(1, 10)

        try:
            #wait for a response message
            guess = await client.wait_for('message', check=is_correct, timeout=5)
        except asyncio.TimeoutError:
            return await message.channel.send(f'Sorry, you took too long it was {answer}.')

        if int(guess.content) == answer:
            await message.channel.send('You are right!')
        else:
            await message.channel.send(f'Wrong. It is actually {answer}.')

    elif message.content.startswith('!weather'):

        #call weather api using my key
        response = requests.get(f'http://api.weatherapi.com/v1/forecast.json?key=d4d293be3d9a46c4961163605220812&days=3&aqi=no&alerts=no&q={message.content[9:]}') if len(message.content) > 8 else requests.get('http://api.weatherapi.com/v1/forecast.json?key=d4d293be3d9a46c4961163605220812&days=3&aqi=no&alerts=no&q=Middletown,NY')
        try:
            data = response.json()
        except Exception as e:
            await message.channel.send(f'Error: {e}\nWait a bit then try again')
            return

        try:
            embedVar = discord.Embed(
                title=f"{data['current']['condition']['text']} {int(float(data['current']['temp_f']))}°F",
                description=f"{int(float(data['current']['wind_mph']))} mph winds",
                color = 0x00ffff)
            embedVar.set_author(name=f"{data['location']['name']}, {data['location']['region']}")
            embedVar.set_thumbnail(url=f"https:{data['current']['condition']['icon']}")
        
            embedVar.add_field(name='Today',
                value=f"High {round(data['forecast']['forecastday'][0]['day']['maxtemp_f'])}°F\nLow {round(data['forecast']['forecastday'][0]['day']['mintemp_f'])}°F\n{data['forecast']['forecastday'][0]['day']['condition']['text']}",inline=True)
            embedVar.add_field(name='Tomorrow',
                value=f"High {round(data['forecast']['forecastday'][1]['day']['maxtemp_f'])}°F\nLow {round(data['forecast']['forecastday'][1]['day']['mintemp_f'])}°F\n{data['forecast']['forecastday'][1]['day']['condition']['text']}",inline=True)
            embedVar.add_field(name=calendar.day_name[datetime.strptime(data['forecast']['forecastday'][2]['date'],'%Y-%m-%d').weekday()],
                value=f"High {round(data['forecast']['forecastday'][2]['day']['maxtemp_f'])}°F\nLow {round(data['forecast']['forecastday'][2]['day']['mintemp_f'])}°F\n{data['forecast']['forecastday'][2]['day']['condition']['text']}",inline=True)
            await message.channel.send(embed=embedVar)
        except Exception as e:
            await message.channel.send(f'Error: {e}\ndata:{data}\nWait a bit then try again')

    elif message.content.startswith('!ask '):
        msg = message.content[5:]
        #make sure they typed something
        if len(message.content) == 5:
            await message.channel.send('Write down what you wanna ask after !ask')
            return

        msg_to_edit = await message.channel.send(f'Getting response...')
        #make sure http server is running
        try:
            response = requests.post('http://localhost:8080', json = {'from':'discord','msg':msg})
        except Exception as e:
            await message.channel.send(f'Command is currently down. (Server not up)')
            return
        try:
            #{'msg':'message'}
            data = response.content.decode('utf-8')
        except Exception as e:
            await message.channel.send(f'Error: {e}')
            print('Error',e,response.content.decode('utf-8'))
            return
        try:
            await msg_to_edit.edit(content=data)
        except Exception as e:
            await msg_to_edit.edit(content='Response too long, splitting into 2 messages:')
            await message.channel.send(data[:data[:2000].rfind('.')+1])
            await message.channel.send(data[data[:2000].rfind('.')+1:])

    elif message.content == '!test embed':
        embedVar = discord.Embed(title='Title',description='Description')
        embedVar.add_field(name="Field1", value="hi", inline=True)
        embedVar.add_field(name="Field2", value="hi2", inline=True)
        embedVar.set_thumbnail(url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1385481861i/7159203._SX540_.jpg')
        embedVar.set_author(name='Author')

        await message.channel.send(embed=embedVar)

    elif message.content == '!test':
        test = await message.channel.send('Editing this message in 2 seconds...')
        time.sleep(2)
        await test.edit(content='Successfully Edited')



#discord bot login token
client.run(CLIENT_TOKEN)

