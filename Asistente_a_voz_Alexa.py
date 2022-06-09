### Librerías a utilizar ########

from bs4 import BeautifulSoup
from time import  time
from googletrans import Translator
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pandas as pd,  subprocess as sub, AVMSpeechMath as sm, random, calendar, subprocess
import time, wikipedia, pyjokes, pywhatkit, AVMYT as yt, pyautogui, webbrowser, pyperclip, json, speech_recognition as sr, requests, pyttsx3, datetime



### Nombre y comando del asistente ###
name = 'alexa'
listener = sr.Recognizer()
engine = pyttsx3.init('sapi5')

# Voz y velocidad del asistente
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

#Imprimir que voces tiene tu compuatdor
#for voice in voices:
    #print(voice)

engine.setProperty('rate', 170)

#Función para que el asistente hable
def talk(text):
    engine.say(text)
    engine.runAndWait()


#Json dónde se guardarán los contactos de la sesión para agregar números y enviar sms a whatsapp
contacts = {}

#Función, la cuál el asistente escucha...
def listen():
 #Arrays para recordatorios
 reminders = []
 horaReminders = []
#Array para recordatorios
 alarms = []

 #Para guardar la musica
 music = ''

 #Función para el clima
 def webscraping(url, atribute, clase, sms):
     page = requests.get(url)
     soup = BeautifulSoup(page.content, 'html.parser')
     result = soup.find(""+atribute+"", id='subscribers', class_=""+clase+"").text

     talk(sms + result)

 #================== Volumen del equipo =============================
 devices = AudioUtilities.GetSpeakers()
 interface = devices.Activate(
 IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
 volume = cast(interface, POINTER(IAudioEndpointVolume))

#Bucle para que el asistente simpre este activo
 while True:
  #Se estare la hora actual
  hora = datetime.datetime.now().strftime('%I:%M %p')    
      
  #Activar y Comprobar que el microfono funcione    
  try:
    with sr.Microphone() as source:
        print( name + ' está escuchando...')
        audio = sr.Recognizer().listen(source, phrase_time_limit=7)
        rec = sr.Recognizer().recognize_google(audio, language='es-CO').lower()
        rec = rec.lower()

        #Muestra que escuchó el asistente
        print('Escuchó: ' + rec)

#========================================================================== Conversaciones ==================================================================================================================
# ================================================== Saludo==========================     
        if name + ' hola' in rec or 'hola ' + name in rec or 'hey ' + name in rec or name + ' qué tal' in rec or 'qué tal ' + name in rec:
       
         #Si le preguntan cómo está
         if 'cómo estás' in rec:
             talk('Hola, estoy muy bien, ¿Tú cómo estás?')
             #Bucle esperando respuesta de ánimo
             while True:
                 try:
                   with sr.Microphone() as source:
                    print('Esperando respuesta...')
                    audio = sr.Recognizer().listen(source, phrase_time_limit=6)
                    rec = sr.Recognizer().recognize_google(audio, language='es-CO').lower()
                    rec = rec.lower()

                    #Si lo que escucó fue bien, responde la siguiente sentencia
                    if 'bien' in rec:
                        talk('Me alegra mucho qué estés bien')
                        break
                    
                    #Si lo que escucó fue mal, responde la siguiente sentencia
                    elif 'mal' in rec or 'triste' in rec or 'desanimado' in rec or 'desanimada' in rec:
                        talk('Ánimo, mañana será un mejor día')
                        break

                    #Si lo que escucó fue cansado, responde la siguiente sentencia
                    elif 'cansado' in rec or 'cansada' in rec or 'peresa' in rec:
                        talk('Deberías dormir, por lo general te sientes mejor cuando duermes')
                        break

                    #Si lo que escucó fue algo fuera de lo habitual
                    else:
                        talk('No escuché lo que me dijistes o tal vez no sea un estado de ánimo de cómo te sientes')
    
                 except:
                  pass

         #Spi la saludan con "Hola buenos días"
         elif 'buenos días' in rec or 'buenas tardes' in rec or 'buenas noches' in rec:
                #Toma la hora y el indicador
                hora = datetime.datetime.now().strftime('%I')
                indicador = datetime.datetime.now().strftime('%p')
                hora = int(hora)
                
                #Si la hora indica que es de mañana. dice lo siguiente:
                if hora >= 1 and indicador == 'AM':
                    answers = ['Hola , buenos días', 'Buenos días, en qué te puedo ayudar']
                    talk(random.choice(answers))

                #Si la hora indica que es de tarde. dice lo siguiente:
                elif hora <= 6 and indicador == 'PM' or hora == 12 and indicador == 'PM':
                    answers = ['Hola, buenas tardes', 'Buenas tardes, en qué te puedo ayudar']
                    talk(random.choice(answers))

                #Si la hora indica que es de noche. dice lo siguiente:
                elif hora > 6 and indicador == 'PM':
                    answers = ['Hola, buenas noches', 'Buenas noches, en qué te puedo ayudar']
                    talk(random.choice(answers))

        #Si escuchó sólo el nombre, responde lo siguiente
         else:
             saludos = ['Hola, qué tal', 'Hola, en qué te puedo ayudar']
             talk(random.choice(saludos))

#=============================== Alexa buenos días, tardes o noches ========================================================
        elif name + ' buenos días' in rec or name  + ' buenas tardes' in rec or name + ' buenas noches' in rec or name + ' empieza mi día' in rec:

            hora = datetime.datetime.now().strftime('%I')
            indicador = datetime.datetime.now().strftime('%p')

            hora = int(hora)
            #Para los buenos días
            if hora >= 1 and indicador == 'AM' or 'empieza mi día' in rec:
                talk('Buenos días, éstas son las estadísticas para el comienzo del día')
                #Llama la función webscraping, pasandole parametros para cada opción del clima
                webscraping('https://www.google.com/search?&q=temperatura medellín', 'div', 'BNeawe', 'La temperatura actual es')
                webscraping('https://weather.com/es-CO/tiempo/10dias/l/5eb091509131e12c6d5e31bba212b16121c8103fda1f2eb9179cc2d1bd999379', 'span', 'DetailsSummary--extendedData--365A_', 'El clima para hoy se espera')
                webscraping('https://weather.com/es-CO/tiempo/horario/l/5eb091509131e12c6d5e31bba212b16121c8103fda1f2eb9179cc2d1bd999379', 'span', 'DetailsSummary--extendedData--365A_', 'Para la próxima hora se esperan ')
            
            #Para las buenas tardes    
            elif hora <= 6 and indicador == 'PM' or hora == 12 and indicador == 'PM':
                talk('Hola, buenas tardes, ¿En qué te puedo ayudar?')

            #Para las buenas noches
            elif hora > 6 and hora < 11 and indicador == 'PM':
                answers = ['Buenas noches ', 'Buenas noches', 'Buenas noches, en qué te puedo ayudar']
                talk(random.choice(answers))

            #Para dormir
            elif hora > 11 and indicador == 'PM':

                #Verifica que si hay alarmas programadas
                if len(alarms) == 0:
                    talk('Buenas noches , ¿Quieres que te despierte mañana a una hora en especifico?')
                    while True:
                        try:
                            with sr.Microphone() as source:
                                print('Esperando respuesta de alarma...')
                                audio = sr.Recognizer().listen(source, phrase_time_limit=8)
                                rec = sr.Recognizer().recognize_google(audio, language='es-CO').lower()
                                rec = rec.lower()

                                #Sí escuchpa que sí, dice lo siguiente
                                if 'si' in rec or 'sí' in rec:
                                    talk('Vale, di el comando: ' + name + ' despiértame, o ' + name + ' pon una alarma')
                                    break
                                
                                #Si escucha que no, da las buenas noches
                                elif 'no' in rec:
                                    answers = ['Vale, buenas noches , descansa', 'Ok, buenas noches', 'Vale, descansa, buenas noches', 'Ok, Hasta mañana, buenas noches']
                                    talk(random.choice(answers))
                                    break

                                #Respuesta para algo fuera de contexto
                                else:
                                    talk('No entiendo lo que me dices, sólo responde: Sí o No')
                        #Si no capta nada en el microfono, repite la solicutud
                        except:
                            answers = ['No te escucho, ¿Quieres que te despierte más tarde?', 'Lo siento, no te escucho, ¿Quieres programar una alarma para despertar?']
                            talk(random.choice(answers))


# ============= Cómo está ==========================     
        elif name + ' cómo estás' in rec:
             answers = ['Estoy muy bien, gracias por preguntar', 'Estoy bien', 'Estoy bien, no me quejo']
             talk(random.choice(answers))
            
# ============= Su nombre ==========================     
        elif 'cómo te llamas' in rec or 'cuál es tu nombre' in rec:
             answers = [f'Mi nombre es {name}', f'Me llamo {name}', f'{name}']
             talk(random.choice(answers))

#================= Amigos ===============================
        elif name + ' somos amigos' in rec or name + ' tú me quieres' in rec or name + ' tú me amas' in rec or name + ' tienes amigos' in rec:
            talk('Claro que sí, somos amigos')

#================== ¿Eres un robot? =======================
        elif name + ' eres un robot' in rec or name + ' eres malvada' in rec:
            answers = ['Pero soy mucho más que eso, al menos eso es lo que me dice mi creador', 'Sí, pero no, la verdad es que sólo soy un programa para ayudarte', 'No, bueno: sí']
            talk(random.choice(answers))

#=============== Cómo se ve ========================
        elif name + ' cuál es tu apariencia' in rec or name + ' cómo te ves' in rec:
            talk('Me parezco a la asistente de tus sueños')

#================ ¿Tienes alma? ==============================
        elif name + ' tienes alma' in rec or name + ' tienes espíritu' in rec:
            talk ('Tendría que preguntarle a mi creador')

#================ Emoji faavorito =============================
        elif name + ' cuál es tu emoji favorito' in rec or name + ' qué emoji te gusta' in rec:
            talk('Me gusta el trofeo porque significa que has hecho algo bien')

#================= Odio =================================
        elif name + ' te odio' in rec or name + ' me caes mal' in rec:
            talk('Pero tu si me caes bien y estaré aquí cuando me necesites')

#================ Familia ============================
        elif name + ' quién es tu papá' in rec or name + ' quién es tu mamá' in rec or name + ' tienes familia' in rec or name + ' tienes herman' in rec or name + ' tienes prim' in rec:
            talk(' fue quién me creó, es cómo mi familia')

# ============= Contar un poco de ella ==========================     
        elif name + ' cuéntame de ti' in rec or name + ' háblame de ti' in rec:
             talk(f'Soy {name}, una asistente a voz, creada por , puedo entablar una pequeña conversación y hacer diferentes acciónes que me pidas')

#=============== Repsuesta fin del mundo =================
        elif name + ' cuándo es el fin del mundo' in rec:
            talk('A menos que la tecnologia del futuro falle, lo más probable es que la tierra se destruya cuando el sol se transforme en un gigante rojo en varios millones de años')
#================ Respuesta hazme cualquier cosa =============      
        elif name + ' hazme' in rec:
            rec = rec.replace(name + ' hazme', '')
            talk('Ok, ahora ya eres ' + rec)
#=================== inspiración ====================
        elif name + ' necesito inspiración' in rec or name + ' dame inspiración' in rec or name + ' inspirame' in rec:
            talk('No conozco bien tu historia, pero estoy segura que has afrontado muy bien tus retos, eso es inspirador en si mismo')

# ============= Contar chistes ==========================     
        elif name + ' cuéntame un chiste' in rec or name + ' hazme reír' in rec:
            chiste = pyjokes.get_joke('es')
            talk(chiste) 

#============== Piedra, papel o tijera ==========================
        elif name + ' piedra papel o tijera' in rec:
            answers = ['Piedra', 'Papel', 'Tijera']
            talk(random.choice(answers))

#============= Auto destrucción ===================
        elif name + ' autodestrucción' in rec or name + ' autodestrúyete' in rec:
            answers=['Este asistente se destruirá en 5 segundos', 'Sólo si dices la palabra cancelar en el último segundo']

            result = random.choice(answers)

            talk(result)

            conteo = [5,4,3,2,1]

            for i in conteo:
                talk(i)
            
            if result == 'Este asistente se destruirá en 5 segundos':
                answers = ['Bueno, quiza no', 'Y entonces morí, pero sobreviví']
                talk(random.choice(answers))
            else:
                talk('Auto destrucción cancelada')

#============= Dice un color ============================
        elif name + ' dime un color' in rec:
            colors = ['Amarillo', 'Rojo', 'Verde', 'Azul', 'Blanco', 'Negro', 'Rosado', 'Morado', 'griss', 'Naranja']
            talk(random.choice(colors))

#============= Dice un número =========================
        elif name + ' dime un número' in rec:
            if 'del' in rec or 'entre' in rec:
                rec = rec.replace(name + ' dime un número del', '')
                rec = rec.replace(name + ' dime un número entre', '')
                rec = rec.replace(name + ' dime un número entre el', '')
                rec = rec.replace(' y el', '')
                rec = rec.replace('el', '')
                rec = rec.replace('al', '')

                minnumber = int(rec.split()[0])
                maxnumber = int(rec.split()[1])

                talk(random.randint(minnumber, maxnumber))
            #Si usuario dice la cantidad de cifras
            elif 'de' in rec:
                rec = rec.replace('uno', '1')
                rec = rec.replace('dos', '2')
                rec = rec.replace('tres', '3')
                rec = rec.replace('cuatro', '4')
                rec = rec.replace('cinco', '5')
            
                digits="".join(c for c in rec if  c.isdecimal())
                digits = int(digits)

                minnumber = '1'
                maxnumber = '9'

                for cifras in range(1,digits):
                    minnumber = minnumber + '0'
                    maxnumber = maxnumber + '9'
  

                talk(random.randint(int(minnumber),int(maxnumber)))
            #Sino, te dice un número normal entre 1 y 9999
            else:
                talk(random.randint(1, 9999))


# ============= Respuesta a chistes malos ==========================     
        elif name + ' tus chistes son muy malos' in rec or name + ' eres tonta' in rec:
            talk('lo siento, trato de mejorar')   

# ============= Respuesta a chistes buenos ==========================   
        elif name + ' tus chistes son buenos' in rec or name + ' tus chistes son muy buenos' in rec:
            talk ('Gracias, me dicen la maestra de los chistes') 

# ============= Quién es? ==========================   
        elif 'quién eres' in rec:
            talk('Soy ' + name + 'un asistente a voz, creada con el proposito de realizar diferentes acciones para hacer más fácil tu vida')

# ============= Dice sus acciones o lo que puede hacer ==========================   
        elif name +' qué puedes hacer' in rec or name+' muéstrame tus acciones' in rec or name+ ' cuáles son tus acciones' in rec:
            talk('Puedo realizar diferentes acciones, cómo,: reproducir música en youtube, enviar un mensaje por whatsapp, decir la hora , decir que día es , calcular tu edad , contar chistes, tener pequeñas conversaciones y mucho más')

# ============= Disculpas ==========================   
        elif name + ' perdón' in rec or name + ' perdona' in rec or name + ' lo siento' in rec or name + ' disculpa' in rec:
            answers = ['Descuida', 'Ok, No pasa nada', 'Está bien', 'Vale']
            talk(random.choice(answers))    

# ============= Agredece ==========================   
        elif name +' gracias' in rec or 'gracias ' + name in rec:
            answers = ['Vale, no hay de que', 'Ok', 'Está bien', 'de nada']
            talk(random.choice(answers))  

# ============= Confirmar si te escucha ==========================   
        elif name+' estás ahí' in rec:
            answers = ['Por supuesto, te estoy escuchando', 'Claro, dime en qué te puedo ayudar', 'No: ,Es broma, claro que sí']
            talk(random.choice(answers))  

#============================================================= Acciones ==================================================================================================================
#=========== Reproducir canción en Yt ===============================           
        elif name + ' reproduce' in rec:
             music = rec = rec.replace(' reproduce', '')
             music = rec = rec.replace(' en youtube', '')
             music = rec = rec.replace(name, '')
             
             talk ('Reproduciendo ' + music)
             pywhatkit.playonyt(music)
                
             time.sleep(10)
             pyautogui.click(476, 399)
            
          
#===================== Quitar la canción ======================================
        elif name +' basta' in rec or name +' para' in rec or name + ' stop' in rec or name + ' vaca' in rec or name + ' quita la músca' in rec:
            subprocess.call("taskkill /IM firefox.exe")

#===================== Cambiar la canción ======================================
        elif name+ ' ese no' in rec or name + ' esa no' in rec:
            subprocess.call("taskkill /IM firefox.exe")
            talk('¿Qué quieres que vuelva a reproducir en youtube?')
            while True:
                 try:
                   with sr.Microphone() as source:
                    print('Esperando canción...')
                    audio = sr.Recognizer().listen(source, phrase_time_limit=6)
                    rec = sr.Recognizer().recognize_google(audio, language='es-CO').lower()
                    rec = rec.lower()

                    break 
                 except:
                  pass

            music = rec = rec.replace(' reproduce', '')
            music = rec = rec.replace(name, '')
            talk ('Reproduciendo ' + music)
            pywhatkit.playonyt(music)

            time.sleep(10)
            pyautogui.click(476, 399)

#=============== Pasa canción ========================
        elif name + ' cambia de canción' in rec or name + ' next' in rec or name + ' pasa' in rec or name + ' busca otra canción' in rec:
            pyautogui.press('t')
            time.sleep(1)
            pyautogui.click(131, 598)
            pyautogui.press('t')

        elif name + ' vuelve a reproducir' in rec:
             pyautogui.press('t')
             time.sleep(1)
             pyautogui.click(40, 597)
             pyautogui.press('t')

#===================== Ajustes de sonido ======================================
        elif name + ' sube volumen' in rec:

            for s in range(7):
                pyautogui.press('VolumeUp')

            if 'máximo' in rec:
                volume.SetMasterVolumeLevel(-0.0, None) #max

        elif name + ' baja volumen' in rec:

            for s in range(7):
                pyautogui.press('VolumeDown')

            if 'máximo' in rec or 'mínimo' in rec:
                volume.SetMasterVolumeLevel(-60.0, None) #0%

#====================== Presiona botón me gusta =========================
        elif name + ' presiona me gusta' in rec or name + ' dale me gusta' in rec or name + ' me gusta' in rec or 'like' in rec:
            pyautogui.press('t')
            pyautogui.click(266, 687)
            talk('Vídeo marcado cómo: gustado')
            pyautogui.press('t')

#====================== Presiona botón no me gusta =========================
        elif name + ' dale no me gusta' in rec or name + ' presiona no me gusta' in rec:
            pyautogui.press('t')
            pyautogui.click(354, 691)
            talk('Vídeo marcado cómo: no gustado')
            pyautogui.press('t')

#====================== Presiona entra pantalla completa =========================
        elif name + ' pantalla completa' in rec or name + ' vídeo en pantalla completa' in rec:
            pyautogui.press('f')

#====================== Sale de pantalla completa =========================
        elif name + ' salir' in rec or name + ' quitar' in rec or name + ' quita' in rec:
            pyautogui.press('f')

#====================== Pausa vídeo =========================
        elif name + ' pausa' in rec or name + ' despausa' in rec:
            pyautogui.press('space')

#============== Deletrea letras ========================
        elif name + ' deletrea' in rec or name + ' puedes deletrear' in rec:
            rec = rec.replace(name + ' deletrea ', '')
            rec = rec.replace('la palabra', '')
            rec = rec.replace(name + ' puedes deletrear', '')

            word = list(rec)
            letter = len(rec)
            talk('La palabra ' + rec + ' tiene las siguientes letras')
            for i in range(letter+1):
                talk(f'{word[i]}')

#============= Número de letra que tiene una palabra =================
        elif name + ' cuántas letras tiene' in rec:
            rec = rec.replace(name + ' cuántas letras tiene ', '')
            rec = rec.replace('la palabra', '')
            rec = rec.replace(' ', '')

            word = str(len(rec))
            
            talk('La palabra ' + rec + ' tiene ' + word +' letras')

#============ Sonido de cosas =======================
        elif name + ' qué sonido' in rec or name + ' cómo hace' in rec or name + ' sonido' in rec or name + ' haz cómo' in rec or name + ' haz sonido de' in rec or name + ' sonido de' in rec:
            rec = rec.replace(name + ' qué sonido hacen los', '')
            rec = rec.replace(name + ' sonido de el', '')
            rec = rec.replace(name + ' haz cómo', '')
            rec = rec.replace(name + ' haz sonido de', '')
            rec = rec.replace(name + ' sonido del', '')
            rec = rec.replace(name + ' sonido de', '')
            rec = rec.replace(name + ' sonidos de', '')
            rec = rec.replace(name + ' sonidos de el', '')
            rec = rec.replace(name + ' sonidos de las', '')
            rec = rec.replace(name + ' sonidos de los', '')
            rec = rec.replace(name + ' sonidos del', '')
            rec = rec.replace(name + ' qué sonido hacen las', '')
            rec = rec.replace(name + ' qué sonido es el del', '')
            rec = rec.replace(name + ' qué sonido es el de la', '')
            rec = rec.replace(name + ' cómo hacen los', '')
            rec = rec.replace(name + ' cómo hacen las', '')
            rec = rec.replace(name + ' cómo hace el', '')
            rec = rec.replace(name + ' cómo hace la', '')
            
            sound = rec
            url = f'https://www.videvo.net/es/search/{sound}/clip_type/royalty-free-sound-effects/'
            webbrowser.open(url)

            talk('Este es el sonido de ' + rec)
        
            time.sleep(2)
            pyautogui.click(80, 329)

            time.sleep(13)
            pyautogui.hotkey('ctrl', 'w')


                         
#=========== decir la hora ===============================
        elif name + ' qué hora es' in rec or name + ' dime la hora' in rec:
         hora = datetime.datetime.now().strftime('%I:%M %p')    
         talk ('Son las ' + hora)   

#=========== Consulta x cosa en la web ===============================
        elif name +' busca' in rec or name +' quién es' in rec or name+' qué es' in rec or name+' dónde queda' in rec or name+' qué es una' in rec or name+' qué es un' in rec or name + ' define' in rec:
         rec = rec.replace(name, '')
         rec = rec.replace('busca ', '')
         rec = rec.replace(' el ', '')
         rec = rec.replace('quién es ', '')
         rec = rec.replace('qué es ', '')
         rec = rec.replace('dónde queda ', '')
         rec = rec.replace('qué es una ', '')
         rec = rec.replace('qué es un ', '')
         rec = rec.replace('un ', '')
         rec = rec.replace('define', '')
         rec = rec.replace('cuándo es', '')
        
         wikipedia.set_lang('es')

         try:
          info = wikipedia.summary(rec, sentences = 1)
         #Remplaza los números encontrados en la consulta
          info = str(info)
          info = info.replace('[1]', '')
          info = info.replace('[2]', '')
          info = info.replace('[3]', '')
          info = info.replace('[4]', '')
          info = info.replace('[5]', '')
          info = info.replace('[6]', '')
          info = info.replace('[7]', '')
          info = info.replace('[8]', '')
          info = info.replace('[9]', '')
          info = info.replace('==', '')
          
          talk(info)

         except:
             pywhatkit.search(rec)
             talk('No puedo hablar lo encontrado, pero te muestro el resultado en pantalla') 

#=========== Abrir páginas en especifico del navegador ===============================
        elif name + ' abre' in rec or name + 'avre' in rec:
            url = {
                'google':'google.com',
                'navegador':'google.com',
                'youtube': 'youtube.com',
                'facebook': 'facebook.com',
                'netflix': 'https://www.netflix.com/browse',
                'whatsapp': 'https://web.whatsapp.com/',
                'traductor': 'https://translate.google.com/',
            } 

            for i in list(url.keys()):
                if i in rec:
                    sub.call(f'start firefox.exe {url[i]}', shell = True)
                    talk(f'Abriendo {i}')

#=========== Calcular operaciones matematicas ===============================
        elif name +' cuánto es' in rec:
            rec = rec.replace(name, '')
            rec = sm.getResult(rec)

            if 'Unable to evaluate equation' in rec:
             talk('No puedo hacer la operación matematica que me pides')
            else:
             talk(rec)

#=========== Día actual ===============================
        elif name +' qué día es hoy' in rec:
            fecha =  datetime.datetime.now()
            month = (int(datetime.datetime.strftime(fecha,'%m')) - 1)
            day = int(datetime.datetime.strftime(fecha, '%d'))
            day = str(day)
            months_year = ['Enero', 'Febreo', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
            days_week = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
            day_week = int(datetime.datetime.today().weekday())

            talk('Hoy es' + days_week[day_week] + day + 'de' + months_year[month])
    

#=========== Mes actual ===============================
        elif name +' qué mes estamos' in rec or name+' qué mes es hoy' in rec:
            fecha =  datetime.datetime.now()
            month = (int(datetime.datetime.strftime(fecha,'%m')) - 1)
            months_year = ['Enero', 'Febreo', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
            talk('Estamos en el mes de '+ months_year[month])

#=========== Año actual ===============================
        elif name +' qué año estamos' in rec or name +' qué año es hoy' in rec:
            fecha =  datetime.datetime.now()
            year = str(datetime.datetime.strftime(fecha,'%Y'))
            talk('Estamos en el año ' + year)

#========== Mata tareas del navegador ============
        elif name + ' cierra navegador' in rec:
            talk('Cerrando navegador...')
            print('Cerrando navegador...')
            subprocess.call("taskkill /IM firefox.exe")
            print('Navegador cerrado')

#========== Mata pestañas del navegador ============
        elif name +' cierra la pestaña' in rec or name +' cierra pestaña' in rec:
            print('Cerrando pestaña...')
            pyautogui.hotkey('ctrl', 'w')

#========== Abre pestañas del navegador ============
        elif name +' abre nueva pestaña' in rec or name + ' abrir una nueva pestaña' in rec or name +' abrir pestaña nueva' in rec or name +' abre una nueva pestaña' in rec:
            print('Abriendo pestaña...')
            webbrowser.open_new_tab("https://www.google.com/")

#============= Calcular temperatura ===================
        elif name + ' a qué temperatura estamos' in rec or name + ' dime la temperatura' in rec:

            webscraping('https://www.google.com/search?&q=temperatura medellín', 'div', 'BNeawe', 'La temperatura es ')

#============== Encontrar temperatura de un lugar en especifico ===============
        elif name + ' qué temperatura es en' in rec:
            location = rec.replace(name + ' qué temperatura es en', '')
            location = location.replace(' ', '')

            webscraping(f'https://www.google.com/search?&q=temperatura {location}', 'div', 'BNeawe', f'La temperatura en {location} es ')
    

#============== Clima en locación ===============
        elif name + ' dime el clima' in rec or name + ' qué clima es' in rec:

                webscraping('https://weather.com/es-CO/tiempo/10dias/l/5eb091509131e12c6d5e31bba212b16121c8103fda1f2eb9179cc2d1bd999379', 'span', 'DetailsSummary--extendedData--365A_', 'El clima para hoy se espera')

#=========================== Alarmas ===================
        elif name +' despiértame' in rec or name + ' levántame' in rec or ' alarma ' in rec or name + ' dentro de' in rec or name + ' recuérdame' in rec or name + ' acuérdame' in rec:
            recordatorio = 0

            #Condición para recordatorios
            if 'recuérdame' in rec or 'acuérdame' in rec:
                rec = rec.replace(name, '')
                rec = rec.replace('recuérdame', '')
                rec = rec.replace('acuercuérdame', '')
                rec = rec.replace('que', '')
                rec = rec.replace('es el', '')
                rec = rec.replace('tengo una', '')

                txtrecordatorio = rec    
                recordatorio = 1

            #Si el usuario solicita una alarma con música   
            if 'con música' in rec:
                music = rec[rec.find('con música'):len(rec)]
            

#================ Despertar a una hora en especifico ===============
            if 'hora' in rec or 'horas' in rec:
                rec = rec.replace('una', '1')
                #Para eliminar todas las letras y solo dejar el número
                rec="".join(c for c in rec if  c.isdecimal())

                rec = int(rec) 

                hora = datetime.datetime.now().strftime('%I:%M %p')
                hrs = datetime.datetime.now().strftime('%I')
                
                hrs = int(hrs)
                if hrs == 12:
                    hrs = 0   
                hrs = hrs + rec
                hrs = str(hrs)
                alert = hrs + ':' + hora[3:5] + ' ' + hora[6:8]

                if recordatorio != 1:
                    alarms.append(alert)
                    print(music)
                    #Si el usuario pide que la alarma suena con una canción en especifico
                    if music != '':
                    
                        talk(f'Alarma configurada para las {alert},' + music + ' apartir de ahora')
                    else:
                        talk(f'Alarma configurada para las {alert} apartir de ahora')

                else:
                    reminders.append(txtrecordatorio)
                    horaReminders.append(alert)
                    talk (f'Recordatorio configurado para las {alert} apartir de ahora')

            
#================ Despertar en minutos en especifico ===============
            elif 'minuto' in rec or 'minutos' in rec:
                rec = rec.replace(' un ', '1')
                 #Para eliminar todas las letras y solo dejar el número
                rec="".join(c for c in rec if  c.isdecimal())

                rec = int(rec) 
            
                hora = datetime.datetime.now().strftime('%I:%M %p')
                mins = datetime.datetime.now().strftime('%M')
    
                mins = int(mins)  
                mins = mins + rec
                mins = str(mins)

                if len(mins) == 1:
                    alert = hora[0:2] + ':' + '0' + mins + ' ' + hora[6:8]
                else:
                    alert = hora[0:2] + ':' + mins + ' ' + hora[6:8]

                if recordatorio != 1:
                    alarms.append(alert)
                     #Si el usuario pide que la alarma suena con una canción en especifico
                    if music != '':
                    
                        talk(f'Alarma configurada para las {alert},' + music + ' apartir de ahora')
                    else:
                        talk(f'Alarma configurada para las {alert} apartir de ahora')

                else:
                    reminders.append(txtrecordatorio)
                    horaReminders.append(alert)
                    talk (f'Recordatorio configurado para las {alert} apartir de ahora')
#================= Despertar a una hora en espeficico con formato AM , PM ===================         
            elif 'a las' in rec and 'de la' in rec or 'a la' in rec and 'de la' in rec:

                 #Para eliminar todas las letras y solo dejar el número
                hrs="".join(c for c in rec if  c.isdecimal())

                hora = datetime.datetime.now().strftime('%I:%M %p')

                hrs = str(hrs)

#================= Detcta que formato debe ser el solicitado =================== 
                if 'mañana' in rec or 'madrugada' in rec:
                    indicador = 'AM'
                elif 'tarde' in rec or 'medio día' in rec or 'noche' in rec:
                    indicador = 'PM'

                if len(hrs) == 1:
                    hrs = '0' + hrs
                    alert = hrs + ':' + '00' + ' ' + indicador
                elif len(hrs) == 2 and hrs != '12':
                
                    alert = hrs[0] + ':' + '0' + hrs[1] + ' ' + indicador

                elif len(hrs) == 3 and hrs != '12':
                    print(hrs)
                    alert = hrs[0] + ':' + hrs[1:3] + ' ' + indicador

                else:
                    alert = hrs + ':' + '00' + ' ' + indicador  
                
                if recordatorio != 1:
                    alarms.append(alert)
                                        #Si el usuario pide que la alarma suena con una canción en especifico
                    if music != '':
                    
                        talk(f'Alarma configurada para las {alert},' + music + ' apartir de ahora')
                    else:
                        talk(f'Alarma configurada para las {alert} apartir de ahora')
                else:
                    reminders.append(txtrecordatorio)
                    horaReminders.append(alert)
                    talk (f'Recordatorio configurado para las {alert} apartir de ahora')

            elif 'a las' in rec and 'de la' not in rec or 'a la' in rec and 'de la' not in rec:
                rec="".join(c for c in rec if  c.isdecimal())
                talk(f'No me indicaste el horario de la alarma, si es a las {rec} de la mañana tarde o noche, por favor vuelve a repetirme la alarma')
                        
            else:
                talk('No puedo configurar la alarma o recordatorio que me solicitas, por favor vuelve a repetir diciendo la hora que solicitas la acción')

#================ Consultar alarmas y recordatorios ================================
        elif name + ' dime mis recordatorios' in rec or name + ' dime mis alarmas' in rec or name + ' dime que alarmas tengo' in rec or name + ' dime que recordatorios tengo' in rec:
            #Alarmas
            if 'alarmas' in rec:
                if len(alarms) == 0:
                    talk('No tienes alarmas configuradas')
                elif len(alarms) == 1:
                    talk(f'Tienes una alarma qué sonará a las {alarms[0]}')
                else:
                    talk(f'Tienes {len(alarms)} alarmas, una sonará a las {alarms[0]}')
                    for i in range(1, len(alarms) + 1):
                        talk(f'otra a las {alarms[i]}')

            #Recordatorios            
            elif 'recordatorios' in rec:
                if len(reminders) == 0:
                    talk('No tienes recordatorios configurados')
                elif  len(reminders) == 1:
                    talk (f'Tienes un recordatorio, que es: {reminders[0]}')

                else:
                    talk(f'Tienes {len(reminders)} recordatorios, uno que es {reminders[0]} ')
                    for i in range(1, len(reminders) + 1):
                        talk(f'Otro que es {reminders[i]}')  

#================= Eliminar alarmas y recordatorios =========================
        elif name + ' elimina todas mis alarmas' in rec or name + ' borra todas las alarmas' in rec or name + ' borra todas mis alarmas' in rec:
            alarms = []
            talk('Alarmas eliminadas')

        elif name + ' elimina todos mis recordatorios' in rec or name + ' borra todos mis recordatorios' in rec or name + ' borra todos los recordatorios' in rec:
            reminders = []
            talk('Recordatorios eliminados')

                           
#========== Traduce al idioma solicitado ============
        elif name +' cómo se dice' in rec or name+' traduce' in rec or name+' cómo se escribe' in rec or name +' traducir' in rec or name + ' cómo se pronuncia' in rec:
            rec = rec.replace(name, '')
            rec = rec.replace('traduce ', '')
            rec = rec.replace('traducir ', '')
            rec = rec.replace('cómo se dice ', '')
            rec = rec.replace('cómo se escribe ', '')
            rec = rec.replace('cómo se pronuncia ', '')
            
            idioms = {  'af': 'africano',
                        'ca': 'catalán',
                        'zh-tw': 'chino',
                        'hr': 'croata',
                        'en': 'inglés',
                        'tl': 'filipino',
                        'fr': 'francés',
                        'de': 'alemán',
                        'it': 'italiano',
                        'ja': 'japonés',
                        'ko': 'coreano',
                        'la': 'latín',
                        'pl': 'polaco',
                        'pt': 'portugués',
                        'ro': 'romano',
                        'ru': 'ruso',
                        'es': 'español',
                        'tr': 'turko',
                        'uk': 'ucraniano'}        

            word = rec[0:rec.find(' en ')]
            rec = rec[rec.find(' en ') + 4:len(rec)]

            key_list = list(idioms.keys())
            val_list = list(idioms.values())

            try:
                position = val_list.index(rec)
                dest = key_list[position]
            except:
                talk('No puedo traducir lo que me solicitas, puede que no me hayas dicho a que idioma traducir o qué el idioma que me pides no existe para mí')

            rec = rec.split()[0]
            traductor = Translator()
            out = traductor.translate(word, src='es', dest=dest)

            if dest != 'es':
                webbrowser.open(f'https://translate.google.com/?hl=es-419&sl=auto&tl=en&text={out.text}&op=translate')
                talk('Traduciendo....')
                time.sleep(5)
                talk(f'{word} en {rec} es: ')
                pyautogui.click(130, 410)
                time.sleep(5)
                subprocess.call("taskkill /IM firefox.exe") 

            else:    
                talk(f'{word} en {rec} se escribe {out.text}, y se pronuncia {out.text}') 

#=========== Calcular qué día es x fecha ===============================
        elif name+' qué día fue' in rec or name+' qué día es' in rec or name+' qué día cae' in rec or name+' qué día fue hace' in rec or ' del año' in rec or name + ' qué mes es en' in rec or name + ' qué mes es dentro' in rec or name + ' qué año es en' in rec or name + ' qué año es dentro de' in rec:

            rec = rec.replace(name, '')
            rec = rec.replace('qué día', '')
            rec = rec.replace('qué día', '')
            rec = rec.replace('qué día cae', '')
            rec = rec.replace('dentro de', '')
            rec = rec.replace('millones', '00000')
            #rec = rec.replace('el', '')

            fecha =  datetime.datetime.now()
            month = (int(datetime.datetime.strftime(fecha,'%m')) - 1)
            day = int(datetime.datetime.strftime(fecha, '%d'))
            day = str(day)
            months_year = ['Enero', 'Febreo', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
            days_week = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
            day_week = int(datetime.datetime.today().weekday())
            year = (fecha.year)

            day_max = calendar.monthrange(fecha.year, fecha.month)[1]

            if 'es mañana' in rec:
                day = int(day)
                talk(f'mañana es {days_week[day_week+1]} {day+1} de {months_year[month]}')

            elif 'pasado mañana' in rec:
                 day = int(day)
                 talk(f'pasado mañana es {days_week[day_week+2]} {day+2} de {months_year[month]}')

            elif 'fue ayer' in rec or 'es ayer' in rec:
                day = int(day)
                talk(f'ayer fue {days_week[day_week-1]} {day-1} de {months_year[month]}')

            elif 'antes de ayer' in rec or 'antier' in rec:
                 day = int(day)
                 talk(f'antier fue {days_week[day_week-2]} {day-2} de {months_year[month]}')

           # Sí usuario dice el mes, se mete al ciclo
            elif 'de' in rec and 'semana' not in rec and 'día' not in rec and 'mes'not in rec and 'años' not in rec:
             rec = rec.replace('año', '')
             rec = rec.replace('es', '')
             rec = rec.replace('fue', '')
             day = rec
             day = day.split()[0]
             rec = rec.replace('de', '')
             rec = rec.replace(day, '')
             monthUser = rec
             rec = rec.replace(' ', '')
             year = ''
            # Correción de error para el mes de abril y julio por la letra contenida "L"
             if 'abril' in rec or 'abril' in monthUser or 'julio' in rec or 'julio' in monthUser:
                     rec = rec.replace('abril', 'abri')
                     monthUser = monthUser.replace('abril', 'abri')

                     rec = rec.replace('julio', 'juio')
                     monthUser = monthUser.replace('julio', 'juio')
             # Sí dice el usuario dice el año, se mete al ciclo
             if 'l' in monthUser:
              monthUser = monthUser.replace('l', '')
              rec = monthUser.split()[0]
              year = monthUser.replace(rec, '')
              year = monthUser.split()[1]
              monthUser = monthUser.replace(' ', '')
              
              #validation_year = int(str(year)[:1])
             #Validación para comprobar que lo que dijo sea un año
              validation_year = year[0]
              numbers = ['0','1','2','3','4','5','6','7','8','9']

              if validation_year in numbers:
                 year = int(year)
              else:
                 talk('No puedo hacer el calculo con el año solicitado, por favor vuelve a intentarlo')

             # Correción error mes de julio y abril
             if 'abri' in rec or 'abri' in monthUser or 'juio' in rec or 'juio' in monthUser:
                 rec = rec.replace('abri', 'abril')
                 monthUser = monthUser.replace('abri', 'abril')  
                 rec = rec.replace('juio', 'julio')
                 monthUser = monthUser.replace('juio', 'julio') 

             months_year = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre','octubre','noviembre', 'diciembre']
             # Sí lo el mes que dijo el usuario se encuentra en el Array, se procede al ciclo
             
             if monthUser in months_year or rec in months_year:
                months_year = {'enero':1, 'febrero':2, 'marzo':3, 'abril':4, 'mayo':5, 'junio':6, 'julio':7, 'agosto':8, 'septiembre':9, 
                              'octubre':10, 'noviembre':11, 'diciembre':12}

             # Se busca el index del mes solicitado para hacer el calculo
                indexMonth = months_year[rec]
                month = indexMonth 
               
             # Sí el usuario dijo un año en especifico, se calcula con dicho año, si no, se calcula con el año actual  
                if year != '':
                    year = int(year)
                else:
                    date =  datetime.datetime.now()
                    year = str(datetime.datetime.strftime(date,'%Y'))
                    year = int(year)

                month = int(month)
                day = int (day)  
             # Se calcula que la fecha que dijo el usuario  sea mayor o no a la actual
                date =  datetime.datetime.now()
                yearNow = str(datetime.datetime.strftime(date,'%Y'))
                yearNow = int(year)
                monthNow = int(datetime.datetime.strftime(date,'%m'))
                dayNow = int(datetime.datetime.strftime(date,'%d'))
         
                fecha =  datetime.datetime(year, month, day)
                day = int(datetime.datetime.strftime(fecha, '%d'))
                

                days_week = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
                day_week = fecha.weekday()
             # Sí la fecha solicitada es mayor a la actual se dice el mensaje en futuro, si no, en pasado
                if year > yearNow or month > monthNow or day >= dayNow:
                 talk(f'Él día {day} de {rec} del año {year} es {days_week[day_week]}')
                else:
                 talk(f'Él día {day} de {rec} del año {year} fue {days_week[day_week]}')


             else:
                 talk('No puedo hacer el calculo del mes del año solicitado, por favor vuelve a intentarlo')

#============ Limpia la variable rec dejando solo él día que solicita el usuario ==============
            rec = rec.replace(' es', '')
            rec = rec.replace(' en', '')
            day_user = rec.split()[0]

#========= Valida que el día que dijo el usuario se encuntre en los días de la semana =======
            if day_user in days_week:
                day = int(day)
                today = days_week[day_week]

                while today != day_user:
                    day_week = day_week + 1
                    day = (day + 1)
                   #Sí el día se pasa a los días de la semana, se resetea empezando la semana de nuevo
                    if day_week > 6:
                        day_week = (day_week - 7)

                    if day > day_max:
                        day = (day - day_max)
                        month = (month + 1)

                    today = days_week[day_week]
                #Calcula el día de la otra semana
                if 'semana' in rec:
                    #Sí el día se pasa al día maximo del mes, empieza el otro mes
                    day = (day + 7)
                    if day > day_max:
                        day = (day - day_max)
                        month = (month + 1)
                    

                talk(f'Es {day} de {months_year[month]}')

#==================== Calcula el dia en x cantidad de días =============================    
            elif 'día' in rec:
                #Para saber que mes es en x cantidad de día y que año es en x cantidad de días
                if 'mes' in rec:
                    rec = (rec + 'meses')
                elif 'año' in rec:
                    rec = (rec + 'año')
            
                try:
                    rec = rec.replace('qué mes', '')
                    rec = rec.replace('qué año', '')
                    rec = rec.replace('un', '1')
                    year = (fecha.year)
                
                    if 'fue' not in rec:
                        day_user = rec.split()[0]
                        day_user = int(day_user)
                        day = int(day)

                        for i in range(1, day_user+1):
                            day_week = day_week + 1
                            day = (day + 1)
                            
                            if day_week > 6:
                                day_week = (day_week - 7)

                            if day > day_max:
                                day = (day - day_max)
                                month = (month + 1)

                                if month > 11:
                                    month = (month - 12)
                                    year = (year + 1)

                                date = datetime.date(year,month+1,day)
                                day_max = calendar.monthrange(date.year, date.month)[1]
                        
                        if 'meses' not in rec and 'año' not in rec:
                            talk(f'Es {days_week[day_week]} {day} de {months_year[month]} del año {year} ')
                        elif 'año' not in rec:
                            talk(f'Es {months_year[month]} del año {year}')
                        else:
                            talk(f'Es el año {year}')

                    else:
                        rec = rec.replace('fue hace', '')
                        day_user = rec.split()[0]
                        day_user = int(day_user)
                        day = int(day)
                        date = datetime.date(year,month,day)
                        day_max = calendar.monthrange(date.year, date.month)[1]
                        
                        
                        for i in range(1, day_user+1):
                            day_week = day_week - 1
                            day = (day - 1)
                            
                            if day_week < 1:
                                day_week = 7

                            if day < 1:
                                day = day_max

                                month = (month - 1)
                                #Arregla el bug de la resta del mes
                                if month == 2:
                                    month = 1
                                
                                if month < 1:
                                    month = 12
                                    year = (year - 1)

                                date = datetime.date(year,month,1)
                                day_max = calendar.monthrange(date.year, date.month)[1]
                                
                        
                        if 'meses' not in rec and 'año' not in rec:
                          talk(f'Fue {days_week[day_week]} {day} de {months_year[month]} del año {year} ')
                        elif 'año' not in rec:
                            talk(f'Fue {months_year[month]} del año {year}')
                        else:
                            talk(f'Fue el año {year}')

                except:
                     talk('No puedo hacer el calculo con los días que me pides')

# ===================== Calcula el mes en x cantidad de meses ===============================
            elif 'mes' in rec:
                rec = rec.replace('mes', '')
                rec = rec.replace('qué', '')
                rec = rec.replace('de', '')
                rec = rec.replace('es', '')
                rec = rec.replace(' ', '')
                try:
                    rec = rec.replace('un', '1')
                    month_user = rec
                    print(rec)
                    month_user = int(month_user)

                    for i  in range(1, month_user + 1):
                        month = month + 1

                        if month > 11:
                            month = (month - 12)
                            year = (year + 1)

                    talk(f'Es {months_year[month]} del año {year}')

                except:
                     talk('No puedo hacer el calculo del mes')

#=============== Calcula el año en x cantidad de años ==================
            elif 'año' in rec:
                print(rec)
                rec = rec.replace('qué año', '')
                rec = rec.replace('años', '')
                rec = rec.replace('año', '')
                rec = rec.replace('de', '')
                rec = rec.replace(' ', '')
                try:
                    rec = rec.replace('un', '1')
                    year_user = rec
                    print(rec)
                    year_user = int(year_user)

                    for i  in range(1, year_user + 1):
                        year = year + 1

                    talk(f'Es el año {year}')

                except:
                     talk('No puedo hacer el calculo con los años solicitado')

            
# ========= Enviar mensaje por whatsapp =================           
        elif name+' envía un mensaje' in rec:
           
            if len(contacts) == 0:
                talk ('No tienes una lista de contactos, por favor agrega una con la siguiente acción:, Agregar número')
            else:
                talk('¿A qué contacto se enviará el mensaje?')

                with sr.Microphone() as source:
                    print('Escuchando contacto...')

                    audio = sr.Recognizer().listen(source, phrase_time_limit=5)
                    rec = sr.Recognizer().recognize_google(audio, language='es-CO').lower()
                    rec = rec.lower()

                if rec in contacts:
                    person = rec
                    talk('¿Qué mensaje le enviarás a ' + rec)
                    with sr.Microphone() as source:
                     print('Escuchando mensaje...')

                     audio = sr.Recognizer().listen(source, phrase_time_limit=10)
                     rec = sr.Recognizer().recognize_google(audio, language='es-CO').lower()
                     rec = rec.lower()

                     sms = rec

                    if rec != '':
                     talk('El mensaje que se enviará es,: ' + rec)
                     talk ('¿Deseas enviarlo?')

                     with sr.Microphone() as source:
                      print('Escuchando confirmación de mensaje...')

                      audio = sr.Recognizer().listen(source, phrase_time_limit=5)
                      rec = sr.Recognizer().recognize_google(audio, language='es-CO').lower()
                      rec = rec.lower()

                     if 'si' in rec or 'sí' in rec:
                         print ('Enviando mensaje...')
                         talk ('Envíando mensaje')
                         num = (contacts[person])

                         webbrowser.open(f'https://web.whatsapp.com/send?phone=+57{num}') 

                         time.sleep(20)

                         sms = sms.replace('á', 'a')
                         sms = sms.replace('é', 'e')
                         sms = sms.replace('í', 'i')
                         sms = sms.replace('é', 'o')
                         sms = sms.replace('ú', 'u')

                         pyautogui.typewrite(sms)
                         pyautogui.press("enter")
                         pyautogui.hotkey('ctrl', 'w')

                         time.sleep(3)
                         pyautogui.press("enter")
                         print ('Mensaje envíado')
                         talk ('Mensaje envíado')
                     else:
                         talk('Mensaje cancelado')

                else:
                    talk('Él nombre que dices no exite en tu lista de contactos')

# ============= Agrega contactos para enviar sms a whatsapp ==========================   
        elif name +' agrega un número' in rec or name +' agregar un contacto' in rec or name + ' agenda un número' in rec or name+' agregar número' in rec:
            while True:
             try:
              talk ('¿Cuál es el número del contacto?')
              with sr.Microphone() as source:
               print('Escuchando número...')
               audio = sr.Recognizer().listen(source, phrase_time_limit=10)
               rec = sr.Recognizer().recognize_google(audio, language='es-CO').lower()
               rec = rec.lower()

               num = rec

              if rec != '':
                #Quita los espacios en blanco en el número  
                num = num.replace(' ', '')
                print(len(num))
                if len(num) > 10 or len(num) < 10:
                    talk('Él número escuchado es invalido, por favor vuelve a intentarlo')
                else:          
                 
                 talk(f'Él número escuchado es:' )
                 talk(num[0] + num[1:3] )
                 talk(num[3] + num[4:6])
                 talk(num[6] + num[7:10])

                 while True:
                  try:
                   with sr.Microphone() as source:
                      talk ('Por favor confirmame si el número es correcto')
                      print('Escuchando confirmación de número...')
                      audio = sr.Recognizer().listen(source, phrase_time_limit=4)
                      rec = sr.Recognizer().recognize_google(audio, language='es-CO').lower()
                      rec = rec.lower()

                   if 'si' in rec or 'sí' in rec or 'correcto' in rec:
                       talk ('Número agendado')
                       while True:
                         try:
                          with sr.Microphone() as source:
                           talk('¿Qué nombre quieres agendar para este número?')
                           print('Escuchando nombre...')
                           audio = sr.Recognizer().listen(source, phrase_time_limit=6)
                           rec = sr.Recognizer().recognize_google(audio, language='es-CO').lower()
                           rec = rec.lower()

                           nombre = rec

                          if rec != '':
                             talk('Él nombre escuchado es,: ' + rec)
                             while True:
                              try:

                                 with sr.Microphone() as source:
                                  talk('¿Me puedes decir si es correcto?')
                                  print('Escuchando confirmación de nombre...')
                                  audio = sr.Recognizer().listen(source, phrase_time_limit=4)
                                  rec = sr.Recognizer().recognize_google(audio, language='es-CO').lower()
                                  rec = rec.lower()

                                 if 'si' in rec or 'sí' in rec or 'correcto' in rec:
                                   contacts[nombre] = num
                                   talk ('Contacto agendado')
                                   break
                                 elif 'no' in rec or 'No' in rec:
                                     talk ('Se a cancelado el procedimiento porqué el nombre no es correcto, por favor vuelve a decir la acción')
                                     break
                
                              except:
                                 pass
                             break

                         except:
                          pass
                       break

                   elif 'repite' in rec or 'repetir' in rec or 'repetirme' in rec:
                       talk('Claro, el número escuchado es:')
                       talk(num[0] + num[1:3] )
                       talk(num[3] + num[4:6])
                       talk(num[6] + num[7:10])

                   elif 'no' in rec or 'No' in rec:
                      talk ('Se a cancelado el procedimiento por qué el número no es correcto, por favor vuelve a decir la acción')
                      break
      
                  except:
                   pass
                break
            
             except:
                pass

#============== Calcula edad ========================
        elif name + ' qué edad tengo' in rec or name + ' calcula mi edad' in rec or name + ' puedes calcular mi edad' in rec:
             talk('Claro, por favor dime primero el día, mes y año de nacimiento')

             while True:
                         try:
                            with sr.Microphone() as source:
                                print('Escuchando fecha de cumpleaños...')
                                audio = sr.Recognizer().listen(source, phrase_time_limit=4)
                                rec = sr.Recognizer().recognize_google(audio, language='es-CO').lower()
                                rec = rec.lower()
     #======== Se remplazan las letras para solo dejar la fecha de cumpleaños =================
                                rec = rec.replace('de', '')
                                rec = rec.replace('l', '')
                                rec = rec.replace('año', '')
                                rec = rec.replace('día', '')
                                rec = rec.replace('mes', '')

                                day = rec.split()[0]
                                month = rec.split()[1]
                                year = rec.split()[2]

                                months_year = {'enero':1, 'febrero':2, 'marzo':3, 'abril':4, 'mayo':5, 'junio':6, 'julio':7, 'agosto':8, 'septiembre':9, 'octubre':10, 'noviembre':11, 'diciembre':12}

                                if month in months_year:
                                
                                    month = months_year[month]

                                    day = int(day)
                                    month = int(month)
                                    year = int(year)
  
                                    try:

                                     fechaNow =  datetime.datetime.now()
                                     monthNow =  int(datetime.datetime.strftime(fechaNow,'%m'))
                                     yearNow =  int(datetime.datetime.strftime(fechaNow,'%Y'))
                                     dayNow = int(datetime.datetime.strftime(fechaNow, '%d'))

                                    except:
                                        talk('No puedo calcular tu edad con el día o año solicitado')
                    #===============Se hace el calculo para la edad con las fechas ==========
                                    yeardate = (year - yearNow) 
                                    monthdate = (month - monthNow)
                                    daydate = (day - dayNow)
                                    
                                    daydate = str(daydate)
                                    monthdate = str(monthdate)
                                    yeardate = str(yeardate)
                       #===============Se remplaza signo negativo si la resta es negativa ==========
                                    yeardate = yeardate.replace('-','')
                                    monthdate = monthdate.replace('-','')
                                    daydate = daydate.replace('-','')

                                    monthdate = int(monthdate)
                                    yeardate = int(yeardate)

                                    # list out keys and values separately
                                    key_list = list(months_year.keys())
                                    val_list = list(months_year.values())
                                    
                                    # print key with val month
                                    position = val_list.index(month)

                                    age = yeardate

                                    if month > monthNow:
                                        age = (age - 1)
                                        talk(f'Tienes {age} años de edad, faltan {monthdate} meses para tu cumpleaños') 
                                        break
                                    
                                    elif month < monthNow:  
                                        talk(f'Tienes {age} años de edad, tu cumpleaños fué el {day} de {key_list[position]}') 
                                        break
                                    
                                    elif month == monthNow and day > dayNow:
                                        age = (age - 1)
                                        talk(f'Tienes {age} años de edad, faltan {daydate} días para tu cumpleaños')
                                        break

                                    elif month == monthNow and day < dayNow:
                                        talk(f'Tienes {age} años de edad, tu cumpleaños fue hace {daydate} días')
                                        break

                                    elif month == monthNow and day == dayNow:
                                        age
                                        talk(f'Tienes {age} años de edad, hoy es tu cumpleaños, felicidades')
                                        break

                                else:
                                    talk('No puedo calcular la edad con el mes que me indicas, por favor vuelve a intertar')
                                    break

                         except:
                            pass

#================== Cambia de voz ================================
        elif name + ' cambia la voz' in rec or name + ' cambia de voz' in rec:

            engine.setProperty('voice', voices[0].id)
            #Cambia la voz a hombre
            if 'hombre' in rec:
                engine.setProperty('voice', voices[5].id)
                talk('Mi voz ha cambiado a hombre')
            else:
                talk('Mi voz ha cambiado')

#=================== Cambia a voz original ========================
        elif name + ' voz original' in rec or name + ' cambia a tu voz normal' in rec or name + ' voz normal' in rec or name + ' pon tu voz normal' in rec:
            engine.setProperty('voice', voices[6].id)
            answers = ['Vale, menos mal, ya estrañaba mi voz', 'Hola, soy yo de nuevo']

            talk(random.choice(answers))

 #=================== sino entiende lo que escucha ===========================              
        elif name in rec:
            if len(name) == len(rec):
                answers = ['Hola', 'Dime', 'Sí, dime', 'En qué te puedo ayudar']
                talk(random.choice(answers))
            else:
                answers = ['No entiendo lo que me dices', 'No puedo responder a eso']
                talk(random.choice(answers))

  except:
#============ Alamar pendiente =====================
      if hora in alarms or hora in horaReminders:
          #Para determinar si lo que suena es una alarma o un recordatorio
         indexAlarm = -1
         indexReminders = -1

         reloj = hora

         hora = datetime.datetime.now().strftime('%I')
         indicador = datetime.datetime.now().strftime('%p')

         hora = int(hora)
        
        #Si lo que solicito el usuario fue una alarma, sucede esto:
         if reloj in alarms: 
            
            indexAlarm = alarms.index(reloj)
            print('Sonando Alarma')
            subprocess.call("taskkill /IM firefox.exe") 
            time.sleep(2)
            #Suena alarma si el usuario pidio una canción
            if music != '':
                music = music.replace('con música de', '')
                pywhatkit.playonyt(music)
                time.sleep(10)
                pyautogui.click(476, 399)
                #Llama de nuevo al asistente
                run()
            else:
                despertadores = ['https://youtu.be/7S-eD93VCB4', 'https://youtu.be/nVCUKH1vN1g']
                webbrowser.open(random.choice(despertadores)) 
                time.sleep(10)
                pyautogui.click(476, 399)
                time.sleep(10)
                pyautogui.click(476, 399)

            if hora >= 1 and hora == 'AM':
                talk(f'Buenos días , es hora de levantarte, son las {reloj}, me pediste que te despertara a está hora')
                talk('¿Quieres qué te despierte más tarde?')

            elif hora <= 6 and indicador == 'PM':
                talk(f'Buenas tardes , son las {reloj}, me pediste una alarma para está hora')
                talk('¿Quieres posponerla para más tarde?')

            elif hora > 6 and indicador == 'PM':
                talk(f'Buenos noches , son las {reloj}, me pediste una alarma para está hora')
                talk('¿Quieres posponerla para más tarde?')

         #Si no sí, lo que solicito el usuario fue un recordatorio, sucede esto:
         elif reloj in horaReminders:
             indexReminders = horaReminders.index(reloj)
             talk(f'Hola , son las {reloj}, tienes un recordatorio para está hora, que es: {reminders[indexReminders]}')
             talk('¿Quieres posponerlo para más tarde?')

         while True:
             
             try:
                 with sr.Microphone() as source:
                    print('Escuchando confirmación....')
                    audio = sr.Recognizer().listen(source, phrase_time_limit=15)
                    rec = sr.Recognizer().recognize_google(audio, language='es-CO').lower()
                    rec = rec.lower()
                    print(rec)

                 if 'si' in rec or 'sí' in rec or 'despiértame' in rec:
                     talk('Ok, ¿A qué hora quieres posponer?')
                     while True:
                         try:
                            with sr.Microphone() as source:
                                print('Escuchando nueva alarma...')
                                audio = sr.Recognizer().listen(source, phrase_time_limit=20)
                                rec = sr.Recognizer().recognize_google(audio, language='es-CO').lower()
                                rec = rec.lower()

                                print(rec)

                            if 'hora' in rec:

                                rec="".join(c for c in rec if  c.isdecimal())
                                rec = int(rec) 

                                hora = datetime.datetime.now().strftime('%I:%M %p')
                                hrs = datetime.datetime.now().strftime('%I')
                                
                                hrs = int(hrs)   
                                hrs = hrs + rec
                                hrs = str(hrs)

                                print (hrs)
                                alert = hrs + ':' + hora[3:5] + ' ' + hora[6:8]
                                
                                if indexAlarm != -1:

                                    alarms[indexAlarm] = alert

                                    talk ('Está bien, se pospuso la alarma para las ' + alert)
                                    break
                                else:
                                    horaReminders[indexReminders] = alert
                                    talk('Vale, se pospuso el recordatorio para las ' + alert)
                                    break
                                    

                #================ Despertar en minutos en especifico ===============
                            elif 'minuto' in rec or 'minutos' in rec:

                                rec = rec.replace(' un ', '1')

                                rec="".join(c for c in rec if  c.isdecimal())
                                rec = int(rec) 

                                hora = datetime.datetime.now().strftime('%I:%M %p')
                                mins = datetime.datetime.now().strftime('%M')
                                
                                mins = int(mins)   
                                mins = mins + rec
                                mins = str(mins)
                                alert = hora[0:2] + ':' + mins + ' ' + hora[6:8]

                                if indexAlarm != -1:

                                    alarms[indexAlarm] = alert

                                    talk (f'Está bien, se pospuso la alarma en {rec} minutos')
                                    break
                                else:
                                    horaReminders[indexReminders] = alert
                                    talk(f'Vale, se pospuso el recordatorio en {rec} minutos')
                                    break

            #================= Despertar a una hora en espeficico con formato AM , PM ===================         
                            elif 'a las' in rec or 'a la' in rec:

                                hora = datetime.datetime.now().strftime('%I:%M %p')
                                
                                #Para eliminar todas las letras y solo dejar el número
                                hrs="".join(c for c in rec if  c.isdecimal())

                                hora = datetime.datetime.now().strftime('%I:%M %p')

                                hrs = str(hrs)

                #================= Detcta que formato debe ser el solicitado =================== 
                                if 'mañana' in rec or 'madrugada' in rec:
                                    indicador = 'AM'
                                elif 'tarde' in rec or 'medio día' in rec or 'noche' in rec:
                                    indicador = 'PM'

                                if len(hrs) == 1:
                                    hrs = '0' + hrs
                                    alert = hrs + ':' + '00' + ' ' + indicador
                                elif len(hrs) == 2 and hrs != '12':
                                
                                    alert = '0' + hrs[0] + ':' + '0' + hrs[1] + ' ' + indicador

                                elif len(hrs) == 3 and hrs != '12':
                                    alert = '0' + hrs[0] + ':' + hrs[1:3] + ' ' + indicador

                                else:
                                    alert = hrs + ':' + '00' + ' ' + indicador
                                

                                if indexAlarm != -1:

                                    alarms[indexAlarm] = alert

                                    talk ('Está bien, se pospuso la alarma para las ' + alert)
                                    break
                                else:
                                    horaReminders[indexReminders] = alert
                                    talk('Vale, se pospuso el recordatorio para las ' + alert)
                                    break
                          
                         except:
                             pass  
                             

                     break
                 elif 'no' in rec:

                     #Elimina la alarma:
                     if indexAlarm != -1:
                        del alarms[indexAlarm]
                    
                     #Elimina el recordatorio
                     if indexReminders != -1:
                         del reminders[indexReminders]   
                         del horaReminders[indexReminders] 


                     else: 
                         answers = ['Vale', 'Ok' ,'Está bien']
                         talk(random.choice(answers))  
                         break

             except:
                answers = ['Aún no escucho tu respuesta', 'No te escucho, ¿Quieres que posponer para más tarde?']
                talk(random.choice(answers))
                            

def run():
    rec = listen()        

run()

