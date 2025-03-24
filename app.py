from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from chatbot import Chatbot
from test import TwitterAccount, TweetCollector  # Importamos las clases de test.py
import asyncio, account as a
from twikit import Client

# Inicializar Flask
app = Flask(__name__)
luca = Chatbot()
# Variable para controlar si la búsqueda está activa
is_search_active = True

# Inicializar cliente de Twitter
client = Client('en-US')

@app.route('/')
def home():
    return 'Home page'

@app.route('/form-inf')
def form_inf():
    return render_template('formulario2.html')

@app.route('/infinite-search', methods=['GET'])
def infinite_search():
    # Obtener parámetros del formulario (enviados como parámetros en la URL)
    query = request.args.get('query')
    from_date = request.args.get('from')
    to_date = request.args.get('to')
    language = request.args.get('language')
    user = request.args.get('user')
    hashtag = request.args.get('hashtag')
    advanced_query = request.args.get('advanced-query')
    formato = request.args.get('formato')

    # Debug: Imprimir los parámetros recibidos
    print(f"query: {query}")
    print(f"from_date: {from_date}")
    print(f"to_date: {to_date}")
    print(f"language: {language}")
    print(f"user: {user}")
    print(f"hashtag: {hashtag}")
    print(f"advanced_query: {advanced_query}")
    print(f"formato: {formato}")

    # Construir la consulta avanzada
    if advanced_query and advanced_query != "undefined":
        QUERY = advanced_query
    else:
        query_parts = []
        if user:
            query_parts.append(f"from:{user}")
        if query:
            keywords = query.split()
            if len(keywords) > 1:
                query_parts.append(f"({' OR '.join(keywords)})")
            else:
                query_parts.append(query)
        if hashtag:
            query_parts.append(f"#{hashtag}")
        if from_date:
            query_parts.append(f"since:{from_date}")
        if to_date:
            query_parts.append(f"until:{to_date}")
        if language:
            query_parts.append(f"lang:{language}")
        QUERY = " ".join(query_parts)

    # Debug: Imprimir la consulta construida
    print(f"La query es: {QUERY}")

    # Crear una cuenta de Twitter
    account = TwitterAccount(
        username=a.USERNAME,
        email=a.EMAIL,
        password=a.PASSWORD
    )

    # Crear una instancia del recolector de tweets
    collector = TweetCollector(client, account, QUERY, save_to=formato)

    def generate():
        #nonlocal is_search_active
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        async_gen = collector.run()
        global is_search_active
        
        try:
            while is_search_active:
                message = loop.run_until_complete(async_gen.__anext__())
                yield f"data: {message}\n\n"
        except StopAsyncIteration:
            yield "data: No hay más tweets para recolectar.\n\n"
        except Exception as e:
            yield f"data: Error: {e}\n\n"
        finally:
            loop.close()
            is_search_active = False

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

# Ruta para detener la búsqueda infinita
@app.route('/stop-infinite-search', methods=['POST'])
def stop_infinite_search():
    global is_search_active
    is_search_active = False
    return jsonify({"status": "success", "message": "Búsqueda detenida."})

@app.route('/form')
def form():
    return render_template('formulario.html')

# Ruta para manejar la búsqueda de tweets
@app.route('/search', methods=['GET'])
def search():
    # Obtener parámetros del formulario (enviados como parámetros en la URL)
    query = request.args.get('query')
    from_date = request.args.get('from')
    to_date = request.args.get('to')
    language = request.args.get('language')
    user = request.args.get('user')
    hashtag = request.args.get('hashtag')
    advanced_query = request.args.get('advanced-query')
    formato = request.args.get('formato')

     # Debug: Imprimir los parámetros recibidos
    print(f"query: {query}")
    print(f"from_date: {from_date}")
    print(f"to_date: {to_date}")
    print(f"language: {language}")
    print(f"user: {user}")
    print(f"hashtag: {hashtag}")
    print(f"advanced_query: {advanced_query}")
    print(f"formato: {formato}")

    # Construir la consulta avanzada
    if advanced_query and advanced_query != "undefined":
        QUERY = advanced_query
    else:
        query_parts = []
        if user:
            query_parts.append(f"from:{user}")
        if query:
            keywords = query.split()
            if len(keywords) > 1:
                query_parts.append(f"({' OR '.join(keywords)})")
            else:
                query_parts.append(query)
        if hashtag:
            query_parts.append(f"#{hashtag}")
        if from_date:
            query_parts.append(f"since:{from_date}")
        if to_date:
            query_parts.append(f"until:{to_date}")
        if language:
            query_parts.append(f"lang:{language}")
        QUERY = " ".join(query_parts)

    # Debug: Imprimir la consulta construida
    print(f"La query es: {QUERY}")

    # Crear una cuenta de Twitter
    account = TwitterAccount(
        username=a.USERNAME,
        email=a.EMAIL,
        password=a.PASSWORD
    )

    # Crear una instancia del recolector de tweets
    collector = TweetCollector(client, account, QUERY, save_to=formato)

    def generate():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        async_gen = collector.run()

        try:
            while True:
                message = loop.run_until_complete(async_gen.__anext__())
                yield f"data: {message}\n\n"
        except StopAsyncIteration:
            pass
        except Exception as e:
            yield f"data: Error: {e}\n\n"
        finally:
            loop.close()

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json['message']
    bot_response = luca.get_response(user_message)  # Obtén la respuesta del chatbot
    return jsonify({'response': bot_response})

@app.route('/cube')
def cubeR():
    return render_template('cube.html')

try:
    if __name__ == '__main__':
        app.run(host='127.0.0.1', port=5000, debug=True)
except Exception as e:
    print(f'Error: {e}')