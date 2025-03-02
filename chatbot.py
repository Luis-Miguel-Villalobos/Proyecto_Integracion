import pandas as pd
from difflib import get_close_matches

class Chatbot:
    def __init__(self):
        # Cargar el archivo CSV con las respuestas
        self.df = pd.read_csv('tweets2.csv', delimiter='|', on_bad_lines='skip')
        
        # Verificar que la columna 'tweet_text' existe
        if 'tweet_text' not in self.df.columns:
            raise ValueError("El archivo CSV debe contener una columna llamada 'tweet_text'.")
        
        # Convertir las respuestas a una lista
        self.respuestas = self.df['tweet_text'].tolist()

    def obtener_respuesta_similar(self, entrada_usuario):
        """
        Busca la respuesta más similar en la lista de respuestas.
        
        Parámetros:
        - entrada_usuario: texto que el usuario escribió.
        
        Retorna:
        - La respuesta más similar o un mensaje predeterminado si no se encuentra.
        """
        # Buscar la respuesta más similar usando difflib
        # - n=1: devuelve solo la mejor coincidencia
        # - cutoff=0.1: umbral de similitud (ajústalo según sea necesario)
        coincidencias = get_close_matches(entrada_usuario, self.respuestas, n=1, cutoff=0.1)
        
        # Si se encontró una coincidencia, devolverla
        if coincidencias:
            return coincidencias[0]
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