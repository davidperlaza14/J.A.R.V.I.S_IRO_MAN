import pyttsx3
from decouple import config
from datetime import datetime
import speech_recognition as sr
from random import choice
from utils import opening_text
import requests
from funciones.online_ops import find_my_ip, get_latest_news, get_random_advice, get_random_joke, get_trending_movies, get_weather_report, play_on_youtube, search_on_google, search_on_wikipedia, send_email, send_whatsapp_message
from funciones.os_ops import open_calculator, open_camera, open_cmd, open_notepad, open_discord
from pprint import pprint





USERNAME = config('USER')
BOTNAME = config('BOTNAME')


engine = pyttsx3.init('sapi5')

# Set Rate
engine.setProperty('rate', 190)

# Set Volume
engine.setProperty('volume', 1.0)

# Set Voice (Female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Conversión Texto a Voz
def speak(text):
    """Usado para decir cualquier texto que le sea entregado"""
    engine.say(text)
    engine.runAndWait()

def greet_user():
    """Saluda al usuario de acuerdo al horario"""
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Buenos dias {USERNAME}")
    elif (hour >= 12) and (hour < 18):
        speak(f"Buenas Tardes {USERNAME}")
    elif (hour >= 19):
        speak(f"Buenas noches {USERNAME}")
    speak(f"Yo soy {BOTNAME}. Como puedo asistirle?")


def take_user_input():
    """Toma las entradas del usuario, las reconoce utilizando el módulo de reconocimiento de voz y lo transforma a texto"""
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Escuchando...')
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print('Reconociendo...')
        query = r.recognize_google(audio, language='es-es')
        if not 'Salir' in query or 'Alto' in query:
            speak(choice(opening_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak("Buenas noches señor, !cuídese!")
            else:
                speak('¡Tenga un buen día señor!')
            exit()
    except Exception:
        speak('Disculpe, no he podido entender. ¿Podría decirlo de nuevo?')
        query = 'None'
    return query


if __name__ == '__main__':
    greet_user()
    while True:
        query = take_user_input().lower()

        if 'open notepad' in query:
            open_notepad()

        elif 'open discord' in query:
            open_discord()

        elif 'open command prompt' in query or 'open cmd' in query:
            open_cmd()

        elif 'open camera' in query:
            open_camera()

        elif 'open calculator' in query:
            open_calculator()

        elif 'ip address' in query:
            ip_address = find_my_ip()
            speak(f'Su Dirección IP es {ip_address}.\n Para su comodidad la estoy mostrado en la pantalla señor.')
            print(f'Tu direccion IP es {ip_address}')

        elif 'wikipedia' in query:
            speak('¿Qué quiere buscar en Wikipedia, señor?')
            search_query = take_user_input().lower()
            results = search_on_wikipedia(search_query)
            speak(f"De acuerdo con Wikipedia, {results}")
            speak("Para su comodidad, mostraré en pantalla los resultados, señor.")
            print(results)

        elif 'youtube' in query:
            speak('¿Que desea ver en YouTube, señor?')
            video = take_user_input().lower()
            play_on_youtube(video)

        elif 'search on google' in query:
            speak('¿Qué desea buscar en Google, señor?')
            query = take_user_input().lower()
            search_on_google(query)

        elif "send whatsapp message" in query:
            speak('¿A qué número debería enviar el mensaje señor?, por favor, digítelo en la consola: ')
            number = input("Ingrese el número: ")
            speak("¿Cúal es el mensaje, señor?")
            message = take_user_input().lower()
            send_whatsapp_message(number, message)
            speak("El mensaje ha sido enviado, señor.")

        elif "send an email" in query:
            speak("¿A qué dirección de correo la envío, señor? Por favor, ingresela en la consola: ")
            receiver_address = input("Ingrese la dirección de correo electrónico: ")
            speak("¿Cuál es el asunto, señor?")
            subject = take_user_input().capitalize()
            speak("¿Cuál es el mensaje, señor?")
            message = take_user_input().capitalize()
            if send_email(receiver_address, subject, message):
                speak("El correo ha sido enviado, señor.")
            else:
                speak("Algo ha salido mal mientras estaba enviando el correo, por favor revise el registro de errores, señor.")

        elif 'joke' in query:
            speak(f"Espero le guste este, señor.")
            joke = get_random_joke()
            speak(joke)
            speak("Para su goce, se lo mostraré en la pantalla, señor.")
            pprint(joke)

        elif "advice" in query:
            speak(f"Acá hay un consejo para usted, señor.")
            advice = get_random_advice()
            speak(advice)
            speak("Para su disfrute, lo estoy mostrando en la pantalla, señor.")
            pprint(advice)

        elif "trending movies" in query:
            speak(f"Algunas de las películas en tendencia son: {get_trending_movies()}")
            speak("Para su mejor comprensión, están en la pantalla, señor.")
            print(*get_trending_movies(), sep='\n')

        elif 'news' in query:
            speak(f"Estoy leyendo los útimos titulares de las noticias, señor.")
            speak(get_latest_news())
            speak("Para su comodidad, las mostraré en la pantalla, señor.")
            print(*get_latest_news(), sep='\n')

        elif 'weather' in query:
            ip_address = find_my_ip()
            city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
            speak(f"Obteniendo el reporte del clima en su ciudad {city}")
            weather, temperature, feels_like = get_weather_report(city)
            speak(f"La temperatura actual es {temperature}, pero se siente más como {feels_like}")
            speak(f"Además, el reporte menciona acerca de {weather}")
            speak("Para vuestra información, se la mostraré en la pantalla, señor.")
            print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")