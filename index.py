import asyncio, csv, json, account as a
import time
from random import randint
from twikit import Client, TooManyRequests
from datetime import datetime

#repo base:
# https://github.com/mehranshakarami/AI_Spectrum/blob/main/2024/Twikit/main.py#L52

MINIMUM_TWEETS = 300
QUERY = '(from:SATMX (IVA OR ISR) until:2024-10-01 since:2023-01-01'

# Initialize client
client = Client('en-US')

async def login():
    await client.login(
        auth_info_1=a.USERNAME ,
        auth_info_2=a.EMAIL,
        password=a.PASSWORD
    )
    print("Inicie sesion en X")

async def recolectar_tweets(tweets):
    if tweets is None:
        #recolectar tweets
        print(f'{datetime.now()} - Recolectando tweets...')
        tweets = await client.search_tweet(QUERY, 'TOP')
    else:
        wait_time= randint(5, 10)
        print(f'{datetime.now()} - Proxima recoleccion en {wait_time} segundos...')
        time.sleep(wait_time)
        tweets = await tweets.next()
    
    return tweets

async def main():
    try:
        await login()
    except Exception as e:
        print(f"No pude iniciar sesion, Error: {e}")
        return

    tweet_count = 0
    tweets= None
    while tweet_count < MINIMUM_TWEETS:

        try:
            tweets= await recolectar_tweets(tweets)
            tweet_count += len(tweets)
        except TooManyRequests as e:
            rate_limit_reset= datetime.fromtimestamp(e.rate_limit_reset)
            print(f'{datetime.now()} - Se alcanzo el limite de peticiones, esperando hasta {rate_limit_reset}')
            wait_time= rate_limit_reset - datetime.now()
            time.sleep(wait_time.total_seconds())
            continue

        if not tweets:
            print(f'{datetime.now()} - No hay mas tweets')
            break

        # Abre el archivo CSV en modo escritura
        with open('tweets.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter='||')

            # Escribe la cabecera del CSV solo si el archivo esta vacio+
            if file.tell() == 0:
                writer.writerow(['user_name', 'tweet_text', 'created_at'])

            count= 0
            for tweet in tweets:
                count += 1
                # Convierte el tweet a formato JSON
                tweet_json = json.dumps({
                    'user_name': tweet.user.name,
                    'tweet_text': tweet.text,
                    'created_at': tweet.created_at
                })
                # Escribe el tweet en el archivo CSV
                writer.writerow([tweet.user.name, tweet.text, tweet.created_at])
            
            print(f'{datetime.now()} - {count} tweets recolectados')
    
    print(f'{datetime.now()} - {tweet_count} tweets recolectados con exito')
       
#Aqui corro el main
try:
    asyncio.run(main())
except Exception as e:
    print(f"No arranco el recolector, Error: {e}")    
