import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
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

        # Extraer solo los tweets limpios para la comparación
        self.tweets_limpios = [tweet_limpio for _, tweet_limpio in self.tweets]

        # Inicializar y entrenar el vectorizador TF-IDF
        self.vectorizer = TfidfVectorizer(
            tokenizer=None,  # No usar tokenizador interno
            preprocessor=None,  # No hacer limpieza automática
            analyzer="word"  # Usar las palabras tal como están tras limpiar
        )
        self.matriz_vectores = self.vectorizer.fit_transform(self.tweets_limpios)


    def obtener_respuesta_similar(self, entrada_usuario):
        """
         Busca la respuesta más similar en la lista de respuestas usando TF-IDF y similitud de coseno.
        """

        # Limpiar el tweet del usuario
        tweet_limpio_usuario = self.data_cleaner.limpiar_tweet(entrada_usuario)
        print(tweet_limpio_usuario)

        # Convertir la pregunta del usuario en un vector TF-IDF
        vector_usuario = self.vectorizer.transform([tweet_limpio_usuario])

        # Calcular la similitud con todos los tweets
        similitudes = cosine_similarity(vector_usuario, self.matriz_vectores)

        # Obtener el índice de la mejor coincidencia
        indice_mas_similar = similitudes.argmax()
        puntaje_similitud = similitudes[0, indice_mas_similar]

        # Definir un umbral de similitud mínima (ajústalo según necesidad)
        UMBRAL_SIMILITUD = 0.5  # Ajusta este valor según los resultados

        if puntaje_similitud >= UMBRAL_SIMILITUD:
            respuesta_original = self.tweets[indice_mas_similar][0]  # Tweet original
            print(self.tweets[indice_mas_similar][1])
            return respuesta_original
        else:
            return "Lo siento, no tengo una respuesta para eso."

    def get_response(self, message):
        """
        Método para obtener la respuesta del chatbot.
        """
        return self.obtener_respuesta_similar(message)