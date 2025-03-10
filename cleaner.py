import re, string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer  # Stemmer para español

class DataCleaner:
    def __init__(self):
        # Descargar las stopwords en español (solo es necesario hacerlo una vez)
        import nltk
        nltk.download('stopwords')
        nltk.download('punkt_tab')
        self.stopwords_es = set(stopwords.words('spanish'))

        # Inicializar el stemmer para español
        self.stemmer = SnowballStemmer('spanish')
        
    def eliminar_menciones(self, tweet):
        """
        Elimina las menciones (palabras que comienzan con '@') de un tweet.
        """
        # Usamos una expresión regular para encontrar y eliminar las menciones
        tweet_limpio = re.sub(r'@\w+', '', tweet)
        # Eliminamos espacios adicionales que puedan quedar después de eliminar las menciones
        tweet_limpio = ' '.join(tweet_limpio.split())
        return tweet_limpio
    
    def eliminar_ligas(self, tweet):
        """
        Elimina las URLs (ligas) de un tweet.
        """
        # Usamos una expresión regular para encontrar y eliminar las URLs
        tweet_limpio = re.sub(r'http\S+|www\.\S+', '', tweet)
        # Eliminamos espacios adicionales que puedan quedar después de eliminar las URLs
        tweet_limpio = ' '.join(tweet_limpio.split())
        return tweet_limpio
    
    def eliminar_stopwords(self, tweet):
        """
        Elimina las stopwords (palabras vacías) de un tweet.
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
        """
        # Usamos una expresión regular para eliminar los signos de puntuación
        tweet_limpio = re.sub(f'[{re.escape(string.punctuation)}]', '', tweet)
        return tweet_limpio
    
    def eliminar_caracteres_especiales(self, tweet):
        """
        Elimina caracteres especiales (que no son letras, números ni espacios) de un tweet.
        """
        # Usamos una expresión regular para eliminar caracteres que no sean letras, números o espacios
        tweet_limpio = re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s$%]|[\n\t\r]', '', tweet)
        return tweet_limpio
    
    def derivar_texto(self, texto):
        """
        Aplica stemming a un texto en español.

        :param texto: Cadena de texto a derivar.
        :return: Texto derivado (stemmed).
        """
        palabras = word_tokenize(texto, language='spanish')
        palabras_stemmed = [self.stemmer.stem(palabra) for palabra in palabras]
        return ' '.join(palabras_stemmed) if palabras_stemmed else ''
    
    def limpiar_tweet(self, tweet):
        """
        Aplica todas las funciones de limpieza a un tweet.
        """
        tweet_limpio = self.eliminar_menciones(tweet)
        tweet_limpio = self.eliminar_ligas(tweet_limpio)
        tweet_limpio = self.eliminar_stopwords(tweet_limpio)
        tweet_limpio = self.eliminar_signos_puntuacion(tweet_limpio)
        tweet_limpio = self.eliminar_caracteres_especiales(tweet_limpio)
        tweet_limpio = self.derivar_texto(tweet_limpio)

        return tweet_limpio