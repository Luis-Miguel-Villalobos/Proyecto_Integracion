import pandas as pd
from difflib import get_close_matches

# Cargar el archivo CSV con las respuestas
# Asegúrate de que el archivo CSV tenga una columna llamada "respuesta"
df = pd.read_csv('tweets2.csv', delimiter='|', on_bad_lines='skip')

print(df.columns)

# Convertir las respuestas a una lista
respuestas = df['tweet_text'].tolist()

# Función para encontrar la respuesta más similar
def obtener_respuesta_similar(entrada_usuario):
    # Buscar la respuesta más similar usando difflib
    # Parámetros:
    # - entrada_usuario: texto que el usuario escribió
    # - respuestas: lista de respuestas disponibles
    # - n=1: devuelve solo la mejor coincidencia
    # - cutoff=0.1: umbral de similitud (ajústalo según sea necesario)
    coincidencias = get_close_matches(entrada_usuario, respuestas, n=1, cutoff=0.1)
    
    # Si se encontró una coincidencia, devolverla
    if coincidencias:
        return coincidencias[0]
    else:
        # Si no se encuentra una respuesta similar, devolver un mensaje predeterminado
        return "Lo siento, no tengo una respuesta para eso."

# Función para interactuar con el chatbot
def interactuar_con_chatbot():
    print("¡Hola! Soy tu chatbot. Puedes empezar a hablar conmigo.")
    while True:
        try:
            # Obtener la entrada del usuario
            user_input = input("Tú: ")
            
            # Obtener la respuesta más similar
            response = obtener_respuesta_similar(user_input)
            
            # Mostrar la respuesta del chatbot
            print(f"ChatBot: {response}")
        except (KeyboardInterrupt, EOFError, SystemExit):
            # Manejar la salida del programa
            print("\n¡Adiós! Fue un placer ayudarte.")
            break

# Iniciar la interacción
interactuar_con_chatbot()