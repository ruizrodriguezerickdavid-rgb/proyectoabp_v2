import flet as ft
import requests
import json
import pyttsx3
import platform
import os
import threading

SO = platform.system()

PERSONAJE = "Guía Virtual del Museo de la Informática"
EMOJI_PERSONAJE = "🤖"
VOZ = "Sabina" if SO == "Windows" else "Juan"

EMOJI_USUARIO = "🧑"
OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL = "phi3:mini"

OLLAMA_OPTIONS = {
    "num_ctx": 2048,
    "num_predict": 200,
    "temperature": 0.7,
    "top_p": 0.85,
    "repeat_penalty": 1.1,
}
KEEP_ALIVE = "30m"

COLOR_GUINDA = "#800000"
COLOR_BLANCO = "#FFFFFF"
COLOR_CHAT_USUARIO = "#A93226"
COLOR_CHAT_BOT = "#F8F8F8"

BANNER_URL = "https://raw.githubusercontent.com/Prof-Luis1986/recursos-cetis50/refs/heads/main/BANNER_CETIS.png"

SALAS = [
    "0: 'Bienvenida y Pasaporte'",
    "1: 'Pioneros: Abaco y Babbage'",
    "2: 'Criptografía y Bombe (Enigma)'",
    "3: 'Transistores y Miniaturización'",
    "4: 'Evolución de los Medios de Almacenamiento'",
    "5: 'Microprocesadores: Línea del Tiempo de CPUs'",
    "6: 'Microprocesadores: Rompecabezas CPU'",
    "7: 'La Energía Digital y La Huella Tecnológica'",
    "8: 'interfaces hapticas y sensoriales (evolucion de perifericos'",
    "9: 'redes e internet'",
    "10: 'red neuronal fisica'",
    "11: 'chatbot del museo y futuro etico de la IA'",
]

SALAS_INFO = {
    0: "¡Bienvenido al Museo de la Informática del CETIS 50! En esta sala recibirás tu pasaporte digital para recorrer todas las exposiciones. Aquí comienza tu viaje por la historia de la computación, desde los primeros dispositivos de cálculo hasta la inteligencia artificial moderna.",

    1: "En la Sala 1 conocemos a los pioneros de la computación. El ábaco fue un sistema mecánico para calcular usado durante milenios en diversas culturas. Charles Babbage diseñó la máquina analítica en el siglo XIX, sentando las bases de la informática moderna con conceptos como memoria, procesamiento programable y tarjetas perforadas.",

    2: "La Sala 2 presenta la criptografía y la máquina Bombe. Durante la Segunda Guerra Mundial, Alan Turing y su equipo en Bletchley Park desarrollaron la Bombe para descifrar los códigos de la máquina Enigma nazi. Este trabajo no solo ayudó a ganar la guerra, sino que marcó un hito fundamental en la historia de la computación y la seguridad informática.",

    3: "En la Sala 3 exploramos los transistores y la miniaturización. Inventados en 1947 en Bell Labs, los transistores reemplazaron las válvulas de vacío, permitiendo computadoras más pequeñas, rápidas, eficientes y confiables. La miniaturización continua llevó a los circuitos integrados y microchips que revolucionaron la tecnología.",

    4: "La Sala 4 presenta la evolución de los medios de almacenamiento: desde tarjetas perforadas y cintas magnéticas, pasando por disquetes, discos duros, CDs, DVDs y memorias USB, hasta el almacenamiento en la nube actual. Cada generación multiplicó la capacidad, velocidad y portabilidad de los datos.",

    5: "En la Sala 5 recorremos la línea del tiempo de los microprocesadores. Desde el Intel 4004 en 1971 (primer microprocesador comercial con 2,300 transistores) hasta los procesadores multinúcleo actuales con miles de millones de transistores que impulsan smartphones, computadoras, servidores y dispositivos IoT.",

    6: "La Sala 6 presenta un rompecabezas interactivo de CPU donde puedes armar y entender los componentes de un procesador moderno: ALU (Unidad Aritmético-Lógica), registros, unidad de control, memoria caché, buses de datos y cómo trabajan juntos para ejecutar instrucciones a velocidades increíbles.",

    7: "En la Sala 7 reflexionamos sobre la energía digital y la huella tecnológica. Exploramos el consumo energético de centros de datos, minería de criptomonedas, dispositivos electrónicos y cómo la tecnología impacta el medio ambiente. También vemos soluciones sostenibles como energías renovables, eficiencia energética y reciclaje electrónico.",

    8: "La Sala 8 muestra la evolución de interfaces hombre-máquina y sensores gestuales: desde teclados mecánicos y ratones, pasando por pantallas táctiles y trackpads, hasta controladores de movimiento, realidad virtual, guantes hápticos, reconocimiento de gestos y tecnologías que permiten interactuar con computadoras de formas cada vez más naturales e intuitivas.",

    9: "En la Sala 9 descubrimos la historia de redes e Internet. Desde ARPANET en 1969 (precursor de Internet) hasta las redes modernas con protocolos TCP/IP, fibra óptica, WiFi, 5G y la conectividad global que permite comunicación instantánea, comercio electrónico, streaming y servicios en la nube que transformaron nuestra sociedad.",

    10: "La Sala 10 presenta una red neuronal física interactiva. Mediante una maqueta tangible y una aplicación Flet, puedes ver cómo funcionan las neuronas artificiales, capas de entrada y salida, capas ocultas, pesos sinápticos, funciones de activación y el proceso de aprendizaje automático de forma visual, práctica y comprensible.",

    11: "La Sala 11 es donde estás ahora: el Chatbot del Museo y el Futuro Ético de la IA. Aquí exploramos cómo funcionan los asistentes virtuales, procesamiento de lenguaje natural, y reflexionamos sobre dilemas éticos de la inteligencia artificial: sesgos algorítmicos, privacidad de datos, transparencia, responsabilidad, impacto laboral y el futuro de la convivencia humano-IA."
}

session = requests.Session()

_tts_engine = None
_tts_lock = threading.Lock()

def hablar(texto, voz=False):
    global _tts_engine
    texto_limpio = texto.replace("*","").replace("_","").replace("#","")
    if SO == "Darwin":
        os.system(f"say -v 'Yuna' \"{texto_limpio}\"")
    elif SO == "Windows":
        try:
            with _tts_lock:
                if _tts_engine is None:
                    _tts_engine = pyttsx3.init()
                    if voz:
                        for v in _tts_engine.getProperty('voices'):
                            if voz.lower() in v.name.lower():
                                _tts_engine.setProperty('voice', v.id)
                                break
                    _tts_engine.setProperty('rate', 160)
                    _tts_engine.setProperty('volume', 0.9)
                _tts_engine.say(texto_limpio)
                _tts_engine.runAndWait()
        except Exception as e:
            print(f"Error en TTS: {e}")

def main(page: ft.Page):
    page.title = f"Chat con {PERSONAJE} – CETis 50"
    page.bgcolor = COLOR_BLANCO

    mensajes = ft.ListView(expand=True, spacing=10, padding=20, auto_scroll=True)

    mensaje_bienvenida = (
        "¡Hola! 👋 Soy tu Guía Virtual del Museo de la Informática del CETis 50.\n"
        "Selecciona una sala del menú para conocer su contenido, o escribe tu pregunta directamente."
    )

    mensajes.controls.append(
        ft.Row([
            ft.Container(
                content=ft.Text(
                    mensaje_bienvenida,
                    color=COLOR_GUINDA,
                    size=15,
                    selectable=True,
                ),
                bgcolor=COLOR_CHAT_BOT,
                padding=12,
                border_radius=30,
                width=350,
            ),
            ft.Text(EMOJI_PERSONAJE, size=24),
        ],alignment=ft.MainAxisAlignment.START)
    )

    page.update()

    if VOZ:
        threading.Thread(target=hablar, args=("¡Hola! Soy tu Guía Virtual del Museo de la Informática del CETis 50. Selecciona una sala del menú o escribe tu pregunta.", VOZ)).start()

    def burbuja(texto, es_usuario):
        return ft.Row(
            [
                ft.Text(EMOJI_USUARIO if es_usuario else EMOJI_PERSONAJE, size=24),
                ft.Container(
                    content=ft.Text(
                        texto,
                        color=COLOR_BLANCO if es_usuario else COLOR_GUINDA,
                        size=15,
                        selectable=True,
                    ),
                    bgcolor=COLOR_CHAT_USUARIO if es_usuario else COLOR_CHAT_BOT,
                    padding=12,
                    border_radius=30,
                    shadow=ft.BoxShadow(blur_radius=8, color="#B0B0B2", offset=ft.Offset(2, 2)),
                    margin=ft.margin.only(left=10) if es_usuario else ft.margin.only(right=10),
                    alignment=ft.alignment.center_right if es_usuario else ft.alignment.center_left,
                    width=350,
                )
            ] if es_usuario else [
                ft.Container(
                    content=ft.Text(
                        texto,
                        color=COLOR_GUINDA,
                        size=15,
                        selectable=True,
                    ),
                    bgcolor=COLOR_CHAT_BOT,
                    padding=12,
                    border_radius=30,
                    shadow=ft.BoxShadow(blur_radius=8, color="#B0B0B2", offset=ft.Offset(2, 2)),
                    margin=ft.margin.only(right=10),
                    alignment=ft.alignment.center_left,
                    width=350,
                ),
                ft.Text(EMOJI_PERSONAJE, size=24),
            ],
            alignment=ft.MainAxisAlignment.END if es_usuario else ft.MainAxisAlignment.START,
        )

    def mostrar_info_sala(num_sala):
            """Muestra información de una sala específica"""
            mensajes.controls.append(burbuja(f"Sala {num_sala}: {SALAS[num_sala]}", es_usuario=True))
            page.update()

            info = SALAS_INFO[num_sala]
            invitacion = "\n\n¿Tienes alguna pregunta sobre esta sala? Escríbela abajo."
            texto_completo = info + invitacion

            mensajes.controls.append(burbuja(texto_completo, es_usuario=False))
            page.update()

            if voz_activada.value and VOZ:
                def leer_sala():
                    try:
                        global _tts_engine
                        if _tts_engine is None:
                            _tts_engine = pyttsx3.init()
                        hablar(info, voz="female")
                    except Exception as e:
                        print(f"Error al leer sala: {e}")
                threading.Thread(target=leer_sala,).start()

    prompt = ft.TextField(
        label=" Escribe tu pregunta...",
        border_radius=20,
        filled=True,
        bgcolor=COLOR_BLANCO,
        multiline=True,
        min_lines=1,
        max_lines=4,
    )

    voz_activada = ft.Checkbox(label="🔊 Leer en voz alta", value=True)


    def enviar_click(e):
        user_input = prompt.value.strip()
        if not user_input:
            return

        mensajes.controls.append(burbuja(user_input, es_usuario=True))
        page.update()
        prompt.value = ""
        page.update()

    # Detectar si pregunta por una sala específica
        texto_final = None
        user_lower = user_input.lower()

    # Buscar referencias a salas (0–11)
        for num in range(12):
            if f"sala {num}" in user_lower or f"sala{num}" in user_lower:
                texto_final = SALAS_INFO[num] + "\n\n💡 ¿Tienes alguna pregunta adicional sobre esta sala?"
                sala_detectada = num
                break

        respuesta_live = ft.Text("", color=COLOR_GUINDA, size=15, selectable=True)
        contenedor_bot = ft.Row([
            ft.Container(
                content=respuesta_live,
                bgcolor=COLOR_CHAT_BOT,
                padding=12,
                border_radius=30,
                width=350,
            ),
            ft.Text(EMOJI_PERSONAJE, size=24),
        ],alignment=ft.MainAxisAlignment.START,)

        mensajes.controls.append(contenedor_bot)
        page.update()

    # Si encontró una sala específica, mostrar respuesta predefinida
        if texto_final:
            respuesta_live.value = texto_final
            page.update()

            if voz_activada.value and VOZ:
                def leer_respuesta():
                    try:
                        global _tts_engine
                        if _tts_engine:
                            _tts_engine.stop()
                        hablar(SALAS_INFO[sala_detectada], VOZ)
                    except Exception as e:
                        print(f"Error al leer respuesta: {e}")
                threading.Thread(target=leer_respuesta).start()
            return
        
        salas_texto = "\n".join([f"Sala {num}: {nombre}" for num, nombre in SALAS.items()])
        prompt_personaje = (
            f"Eres el Guía Virtual del Museo de la Informática del CETis 50. "
            f"Responde en español, de manera clara y didáctica en máximo 4 frases. "
            f"Si te preguntan por una sala específica, describe SOLO esa sala. "
            f"Las salas del museo son:\n{salas_texto}\n\n"
            f"Pregunta: {user_input}\n"
            f"Respuesta:"
        )

        try:
            resp = session.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "prompt": prompt_personaje,
                    "stream": True,
                    "keep_alive": KEEP_ALIVE,
                    "options": OLLAMA_OPTIONS,
                },
                stream=True,
                timeout=300,
            )
            resp.raise_for_status()

            texto_final = ""
            for line in resp.iter_lines():
                if not line:
                    continue
                data = json.loads(line)
                if "response" in data:
                    chunk = data["response"]
                    texto_final += chunk
                    respuesta_live.value = texto_final
                    page.update()
                elif "error" in data:
                    texto_final = f"Error de Ollama: {data['error']}"
                    break

            if not texto_final:
                texto_final = "No se recibió respuesta del modelo."

            respuesta_live.value = texto_final
            page.update()

        # TTS al final
            if voz_activada.value and VOZ:
                def leer_respuesta():
                    try:
                        global _tts_engine
                        if _tts_engine:
                            _tts_engine.stop()
                        hablar(texto_final, VOZ)
                    except Exception as e:
                        print(f"Error al leer respuesta: {e}")
                threading.Thread(target=leer_respuesta).start()

        except Exception as ex:
            respuesta_live.value = f"Error de conexión o inesperado: {ex}"
            page.update()

    prompt.on_submit = enviar_click

    def probar_voz(e):
        if VOZ:
            threading.Thread(target=hablar, args=(f"Hola, soy {PERSONAJE}. Estoy aquí para guiarte por el Museo de la Informática del CETis 50.", VOZ)).start()

    def limpiar_chat(e):
        mensajes.controls.clear()

    # Agregar mensaje de bienvenida
        mensajes.controls.append(
            ft.Row([
                ft.Container(
                    content=ft.Text(
                        mensaje_bienvenida,
                        color=COLOR_GUINDA,
                        size=15,
                        selectable=True,
                    ),
                    bgcolor=COLOR_CHAT_BOT,
                    padding=12,
                    border_radius=30,
                    width=350,
                ),
                ft.Text(EMOJI_PERSONAJE, size=24),
            ],alignment=ft.MainAxisAlignment.START,)
        )

        page.update()

    # Vuelve a decir el saludo por voz al limpiar
        if VOZ:
            threading.Thread(target=hablar, args=("¡Hola! Soy tu Guía Virtual del Museo de la Informática del CETis 50. Selecciona una sala del menú o escribe tu pregunta.", VOZ)).start()

    header = ft.Container(
        content=ft.Row([
            ft.Text(EMOJI_PERSONAJE, size=32),
            ft.Text(PERSONAJE, size=22, weight="bold", color=COLOR_GUINDA),
        ],alignment=ft.MainAxisAlignment.START,spacing=15),
        padding=ft.padding.symmetric(vertical=16, horizontal=10),
        bgcolor=COLOR_BLANCO,
        border_radius=ft.border_radius.only(top_left=20, top_right=20),
        shadow=ft.BoxShadow(blur_radius=12, color="#7D8DE2", offset=ft.Offset(0, 2))
    )

    banner = ft.Image(
        src=BANNER_URL,
        width=600,
        height=90,
        fit=ft.ImageFit.CONTAIN
    )

# Menú de salas (botones compactos - 12 salas: 0 a 11)
    def crear_boton_sala(num):
        return ft.ElevatedButton(
            text=f"{num}",
            on_click=lambda _: mostrar_info_sala(num),
            bgcolor=COLOR_GUINDA,
            color=COLOR_BLANCO,
            width=50,
            height=40,
            tooltip=SALAS[num]
        )

    menu_salas = ft.Container(
        content=ft.Column([
            ft.Text("🏛️ Selecciona una sala:", size=14, weight="bold", color=COLOR_GUINDA),
            ft.Row([
                crear_boton_sala(0),
                crear_boton_sala(1),
                crear_boton_sala(2),
                crear_boton_sala(3),
                crear_boton_sala(4),
                crear_boton_sala(5),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
            ft.Row([
                crear_boton_sala(6),
                crear_boton_sala(7),
                crear_boton_sala(8),
                crear_boton_sala(9),
                crear_boton_sala(10),
                crear_boton_sala(11),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
        ], spacing=8),
        padding=10,
        bgcolor="#FFFFF5",
        border_radius=10,
    )

    page.add(
        ft.Container(
            content=ft.Column([
                banner,
                header,
                menu_salas,
                mensajes,
                ft.Row([
                    voz_activada,
                    ft.ElevatedButton("🔈 Probar voz", on_click=probar_voz, bgcolor=COLOR_GUINDA, color=COLOR_BLANCO),
                    ft.TextButton("🧹 Limpiar chat", on_click=limpiar_chat, style=ft.ButtonStyle(color=COLOR_GUINDA)),
                ], alignment=ft.MainAxisAlignment.START, spacing=10),
                ft.Row([
                    prompt,
                    ft.ElevatedButton("Enviar", on_click=enviar_click, bgcolor=COLOR_GUINDA, color=COLOR_BLANCO),
                ], vertical_alignment=ft.CrossAxisAlignment.END),
            ], expand=True, spacing=10),
            exand=True,
            padding=0,
            border_radius=0,
            bgcolor=COLOR_BLANCO,
        )   
    )   

ft.app(target=main)