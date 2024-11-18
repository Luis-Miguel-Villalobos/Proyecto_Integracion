import asyncio, csv, json, account as a
from twikit import Client

# Initialize client
client = Client('en-US')

async def main():
    await client.login(
        auth_info_1=a.USERNAME ,
        auth_info_2=a.EMAIL,
        password=a.PASSWORD
    )
    print("Inicie sesion en X")

    try:
        tweets = await client.search_tweet('from:SATMX', 'top')

        # Abre el archivo CSV en modo escritura
        with open('tweets.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Escribe la cabecera del CSV solo si el archivo esta vacio+
            if file.tell() == 0:
                writer.writerow(['user_name', 'tweet_text', 'created_at'])

            for tweet in tweets:
                # Convierte el tweet a formato JSON
                tweet_json = json.dumps({
                    'user_name': tweet.user.name,
                    'tweet_text': tweet.text,
                    'created_at': tweet.created_at
                })
                # Escribe el tweet en el archivo CSV
                writer.writerow([tweet.user.name, tweet.text, tweet.created_at])
                #await client.logout()

    except Exception as e:
        print(f"No pude recolectar tweets: {e}")
    else:
        print("Tweets recolectados con exito")

try:
    asyncio.run(main())
except Exception as e:
    print(f"No pude iniciar sesion, Error: {e}")