import pandas as pd
from difflib import get_close_matches
from cleaner import DataCleaner

class Chatbot:
    def __init__(self):
        # Cargar el archivo CSV con las respuestas
        self.df = pd.read_csv('tweets2.csv', delimiter='|', on_bad_lines='skip')
        
        # Verificar que la columna 'tweet_text' existe
        if 'tweet_text' not in self.df.columns:
            raise ValueError("El archivo CSV debe contener una columna llamada 'tweet_text'.")
 
        # Inicializar el DataCleaner
        self.data_cleaner = DataCleaner()
               
       # Crear una lista de tuplas (tweet_original, tweet_limpio)
        self.tweets = [
            (tweet, self.data_cleaner.limpiar_tweet(tweet))  # (original, limpio)
            for tweet in self.df['tweet_text']
        ]


    def obtener_respuesta_similar(self, entrada_usuario):
        """
        Busca la respuesta más similar en la lista de respuestas.
        
        Parámetros:
        - entrada_usuario: texto que el usuario escribió.
        
        Retorna:
        - La respuesta más similar o un mensaje predeterminado si no se encuentra.
        """

        # Limpiar el tweet del usuario
        tweet_limpio_usuario = self.data_cleaner.limpiar_tweet(entrada_usuario)
        print(tweet_limpio_usuario)

        # Buscar la respuesta más similar usando difflib
        # - n=1: devuelve solo la mejor coincidencia
        # - cutoff=0.1: umbral de similitud (ajústalo según sea necesario)

         # Extraer solo los tweets limpios para la comparación
        tweets_limpios = [tweet_limpio for _, tweet_limpio in self.tweets]

        # Buscar la respuesta más similar usando difflib (en los tweets limpios)
        coincidencias = get_close_matches(tweet_limpio_usuario, tweets_limpios, n=1, cutoff=0.3)
        print(coincidencias)
        
        # Si se encontró una coincidencia, devolverla
        if coincidencias:
            indice = tweets_limpios.index(coincidencias[0])
            respuesta_original = self.tweets[indice][0]  # Tweet original
            return respuesta_original
        else:
            # Si no se encuentra una respuesta similar, devolver un mensaje predeterminado
            return "Lo siento, no tengo una respuesta para eso."

    def get_response(self, message):
        """
        Método para obtener la respuesta del chatbot.
        
        Parámetros:
        - message: mensaje del usuario.
        
        Retorna:
        - La respuesta del chatbot.
        """
        return self.obtener_respuesta_similar(message)