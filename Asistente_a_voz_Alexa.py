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


#Bucle para que el asistente simpre este activo
while True:
  #Variable que guarda la hora actual
  hora = datetime.datetime.now().strftime('%I:%M %p')    
      
  #Activar y Comprobar que el microfono funcione    
  try:
    with sr.Microphone() as source:
        print( name + ' está escuchando...')
        audio = sr.Recognizer().listen(source, phrase_time_limit=5)
        rec = sr.Recognizer().recognize_google(audio, language='es-CO').lower()
        rec = rec.lower()

        #Muestra que escuchó el asistente
        print('Escuchó: ' + rec)

# ============ Cómo está ==========================     
        if name + ' cómo estás' in rec:
                answers = ['Estoy muy bien, gracias por preguntar', 'Estoy bien', 'Estoy bien, no me quejo']
                talk(random.choice(answers))
            
# ============= Su nombre ==========================     
        elif 'cómo te llamas' in rec or 'cuál es tu nombre' in rec:
             answers = [f'Mi nombre es {name}', f'Me llamo {name}', f'{name}']
             talk(random.choice(answers))

# ============= Contar un poco de ella ==========================     
        elif name + ' cuéntame de ti' in rec or name + ' háblame de ti' in rec:
             talk(f'Soy {name}, una asistente a voz, puedo entablar una pequeña conversación y hacer diferentes acciónes que me pidas')
             
# ============= Contar chistes ==========================     
        elif name + ' cuéntame un chiste' in rec or name + ' hazme reír' in rec:
            chiste = pyjokes.get_joke('es')
            talk(chiste) 

#============== Piedra, papel o tijera ==========================
        elif name + ' piedra papel o tijera' in rec:
            answers = ['Piedra', 'Papel', 'Tijera']
            talk(random.choice(answers))


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

#=== Finaliza el programa diciendo el nombre del asisten más alguna de estas dos palabras "descansa o finalizar"==========
        elif name + ' descansa' in rec or name + ' finalizar' in rec:
            break

 #=================== sino entiende lo que escucha ===========================              
        elif name in rec:
            if len(name) == len(rec):
                answers = ['Hola', 'Dime', 'Sí, dime', 'En qué te puedo ayudar']
                talk(random.choice(answers))
            else:
                answers = ['No entiendo lo que me dices', 'No puedo responder a eso']
                talk(random.choice(answers))

  except:
    pass



