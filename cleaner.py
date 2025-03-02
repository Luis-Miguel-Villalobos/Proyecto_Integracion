import re, string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class DataCleaner:
    def __init__(self):
        # Descargar las stopwords en español (solo es necesario hacerlo una vez)
        import nltk
        nltk.download('stopwords')
        nltk.download('punkt')
        self.stopwords_es = set(stopwords.words('spanish'))
        
    def eliminar_menciones(self, tweet):
        """
        Elimina las menciones (palabras que comienzan con '@') de un tweet.

        :param tweet: Cadena de texto que representa el tweet.
        :return: El tweet sin menciones.
        """
        # Usamos una expresión regular para encontrar y eliminar las menciones
        tweet_limpio = re.sub(r'@\w+', '', tweet)
        # Eliminamos espacios adicionales que puedan quedar después de eliminar las menciones
        tweet_limpio = ' '.join(tweet_limpio.split())
        return tweet_limpio
    
    def eliminar_ligas(self, tweet):
        """
        Elimina las URLs (ligas) de un tweet.

        :param tweet: Cadena de texto que representa el tweet.
        :return: El tweet sin URLs.
        """
        # Usamos una expresión regular para encontrar y eliminar las URLs
        tweet_limpio = re.sub(r'http\S+|www\.\S+', '', tweet)
        # Eliminamos espacios adicionales que puedan quedar después de eliminar las URLs
        tweet_limpio = ' '.join(tweet_limpio.split())
        return tweet_limpio
    
    def eliminar_stopwords(self, tweet):
        """
        Elimina las stopwords (palabras vacías) de un tweet.

        :param tweet: Cadena de texto que representa el tweet.
        :return: El tweet sin stopwords.
        """
        # Tokenizar el tweet en palabras individuales
        palabras = word_tokenize(tweet, language='spanish')
        # Filtrar las stopwords
        palabras_limpias = [palabra for palabra in palabras if palabra.lower() not in self.stopwords_es]
        # Unir las palabras limpias en una sola cadena
        tweet_limpio = ' '.join(palabras_limpias)
        return tweet_limpio
    
    def eliminar_signos_puntuacion(self, tweet):
        """
        Elimina los signos de puntuación de un tweet.

        :param tweet: Cadena de texto que representa el tweet.
        :return: El tweet sin signos de puntuación.
        """
        # Usamos una expresión regular para eliminar los signos de puntuación
        tweet_limpio = re.sub(f'[{re.escape(string.punctuation)}]', '', tweet)
        return tweet_limpio
    
    def eliminar_caracteres_especiales(self, tweet):
        """
        Elimina caracteres especiales (que no son letras, números ni espacios) de un tweet.

        :param tweet: Cadena de texto que representa el tweet.
        :return: El tweet sin caracteres especiales.
        """
        # Usamos una expresión regular para eliminar caracteres que no sean letras, números o espacios
        tweet_limpio = re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s]', '', tweet)
        return tweet_limpio