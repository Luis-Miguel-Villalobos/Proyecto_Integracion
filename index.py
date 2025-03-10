import asyncio, csv, json, account as a
import time
from random import randint
from twikit import Client, TooManyRequests
from datetime import datetime

#repo base:
# https://github.com/mehranshakarami/AI_Spectrum/blob/main/2024/Twikit/main.py#L52

# Constante
MINIMUM_TWEETS = 5000

class TwitterAccount:
    def __init__(self, username, email, password):
        """
        Inicializa una cuenta de Twitter.
        
        :param username: Nombre de usuario de la cuenta.
        :param email: Correo electrónico de la cuenta.
        :param password: Contraseña de la cuenta.
        """
        self.username = username
        self.email = email
        self.password = password


class TweetCollector:
    def __init__(self, client, account, query, save_to="csv"):
        """
        Inicializa el recolector de tweets.
        
        :param client: Cliente de la API de X.
        :param account: Objeto de tipo TwitterAccount con los datos de la cuenta.
        :param query: Consulta para buscar tweets.
        :param save_to: Formato en el que se guardarán los tweets (csv, json, txt).
        """
        self.client = client
        self.account = account  # Recibe un objeto TwitterAccount
        self.query = query
        self.save_to = save_to.lower()  # Asegura que el formato esté en minúsculas
        self.tweet_count = 0
        self.tweets = None

    async def login(self):
        """Inicia sesión en X."""
        await self.client.login(
            auth_info_1=self.account.username,
            auth_info_2=self.account.email,
            password=self.account.password
        )
        print(f"{datetime.now()} - Inicié sesión en X")

    async def collect_tweets(self):
        """Recolecta tweets."""
        if self.tweets is None:
            print(f'{datetime.now()} - Recolectando tweets...')
            self.tweets = await self.client.search_tweet(self.query, 'LATEST')
        else:
            wait_time = randint(5, 10)
            print(f'{datetime.now()} - Próxima recolección en {wait_time} segundos...')
            time.sleep(wait_time)
            self.tweets = await self.tweets.next()
        return self.tweets

    async def save_tweets(self, tweets):
        """
        Guarda los tweets en el formato especificado (csv, json, txt).
        
        :param tweets: Lista de tweets recolectados.
        """
        if self.save_to == "csv":
            await self.save_tweets_to_csv(tweets)
        elif self.save_to == "json":
            await self.save_tweets_to_json(tweets)
        elif self.save_to == "txt":
            await self.save_tweets_to_txt(tweets)
        else:
            print(f"{datetime.now()} - Formato no válido. No se guardaron los tweets.")

    async def save_tweets_to_csv(self, tweets):
        """Guarda los tweets en un archivo CSV."""
        with open('tweets.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter='|')

            # Escribe la cabecera del CSV solo si el archivo está vacío
            if file.tell() == 0:
                writer.writerow(['user_name', 'id_tweet', 'tweet_text', 'created_at'])

            count = 0
            for tweet in tweets:
                count += 1
                writer.writerow([tweet.user.name, tweet.id, tweet.text, tweet.created_at])

            print(f'{datetime.now()} - {count} tweets guardados en CSV')

    async def save_tweets_to_json(self, tweets):
        """Guarda los tweets en un archivo JSON."""
        tweets_data = []
        for tweet in tweets:
            tweets_data.append({
                'user_name': tweet.user.name,
                'id_tweet': tweet.id,
                'tweet_text': tweet.text,
                'created_at': tweet.created_at.isoformat()
            })

        with open('tweets.json', mode='a', encoding='utf-8') as file:
            if file.tell() != 0:  # Si el archivo no está vacío, añade una coma
                file.write(",\n")
            json.dump(tweets_data, file, indent=4, ensure_ascii=False)

        print(f'{datetime.now()} - {len(tweets_data)} tweets guardados en JSON')

    async def save_tweets_to_txt(self, tweets):
        """Guarda los tweets en un archivo TXT."""
        with open('tweets.txt', mode='a', encoding='utf-8') as file:
            for tweet in tweets:
                file.write(f"Usuario: {tweet.user.name}\n")
                file.write(f"ID del Tweet: {tweet.id}\n")
                file.write(f"Texto: {tweet.text}\n")
                file.write(f"Fecha: {tweet.created_at}\n")
                file.write("-" * 50 + "\n")

        print(f'{datetime.now()} - {len(tweets)} tweets guardados en TXT')

    async def run(self):
        """Ejecuta el proceso de recolección de tweets."""
        try:
            await self.login()
        except Exception as e:
            print(f"{datetime.now()} - No pude iniciar sesión. Error: {e}")
            return

        while self.tweet_count < MINIMUM_TWEETS:
            try:
                tweets = await self.collect_tweets()
                self.tweet_count += len(tweets)
                await self.save_tweets(tweets)
            except TooManyRequests as e:
                rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
                print(f'{datetime.now()} - Se alcanzó el límite de peticiones. Esperando hasta {rate_limit_reset}')
                wait_time = (rate_limit_reset - datetime.now()).total_seconds()
                time.sleep(wait_time)
                continue
            except Exception as e:
                print(f'{datetime.now()} - Error: {e}')
                break

            if not tweets:
                print(f'{datetime.now()} - No hay más tweets')
                break

        print(f'{datetime.now()} - {self.tweet_count} tweets recolectados con éxito')


# Aquí corro el recolector
if __name__ == "__main__":
    # Inicializa el cliente (asegúrate de importar y configurar el cliente correctamente)
    client = Client('en-US')

    # Crea una cuenta de Twitter
    account = TwitterAccount(
        username= a.USERNAME,
        email= a.EMAIL,
        password= a.PASSWORD
    )

    # Define la consulta (QUERY)
    query = '(from:SATMX (DIOT OR IEPS) until:2024-10-31 since:2023-01-01'

    # Define el formato de guardado (csv, json, txt)
    save_to = "json"  # Cambia a "csv", "json" o "txt" según lo que necesites

    # Crea una instancia del recolector de tweets
    collector = TweetCollector(client, account, query, save_to)

    # Ejecuta el recolector
    try:
        asyncio.run(collector.run())
    except Exception as e:
        print(f"{datetime.now()} - No arrancó el recolector. Error: {e}")