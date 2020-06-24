from selenium import webdriver

driver = webdriver.Chrome('D:\ProgramData\Selenium drivers\chromedriver.exe')


def site_login():
    # Login moodle
    driver.get('https://moodle-exam.upm.es/login/login.php')
    driver.find_element_by_id('username').send_keys('email')
    driver.find_element_by_id('password').send_keys('password')
    driver.find_element_by_id('loginbtn').click()


def go_to_question(url_pregunta):
    driver.get(url_pregunta)
    tabla = driver.find_elements_by_xpath("//tr")
    nombre = tabla[0].text
    pregunta = tabla[2].text.split(' ')[1]
    #buscar solucion
    solucion = driver.find_element_by_css_selector(
        'div.rightanswer')
    if solucion.text[26:] == '' or solucion.text[26:] == ',':
        # Debe ser entera en latex.
        solucion = solucion.find_element_by_xpath(
            './/*[@class="texrender"]').get_attribute('title')
    else:
        solucion = solucion.text[26:]
    # Buscar respuesta
    try:
    # mal
        bloque = driver.find_element_by_class_name('ablock')
        respuesta = bloque.find_element_by_xpath(
            './/*[contains(@class,"incorrect")]')
        if respuesta.text[3:] == '' or respuesta.text[3:] == ',':
            # Debe ser entera en latex
            respuesta = respuesta.find_element_by_xpath(
                './/script').get_attribute('innerHTML')
        else:
            respuesta = respuesta.text[3:]
        bien = 'False'
    except:
    # bien
        try:
            bloque = driver.find_element_by_class_name('ablock')
            respuesta = bloque.find_element_by_xpath(
                './/*[contains(@class,"correct")]')
            if respuesta.text[3:] == '' or respuesta.text[3:] == ',':
                # Debe ser entera en latex
                    respuesta = respuesta.find_element_by_xpath(
                    './/script').get_attribute('innerHTML')
            else:
                respuesta = respuesta.text[3:]
            bien = 'True'
        except:
            respuesta = None
            bien = 'NS/NC'


    return '{};{};{};{};{}\n'.format(nombre, pregunta, respuesta, solucion, bien) 


def go_to_problema(url_pregunta):
    driver.get(url_pregunta)
    tabla = driver.find_elements_by_xpath("//tr")
    nombre = tabla[0].text
    pregunta = tabla[2].text.split(' ')[2]
    # Buscar respuesta
    try:
        # Preguntas de varias repuestas (Cloze)
        # Busco el hover para sacar la solucion
        hover = driver.find_elements_by_tag_name(
            "span[class='feedbackspan yui3-overlay-content yui3-widget-stdmod'")
        
        respuestas = driver.find_elements_by_xpath(
            '//*[contains(@class,"form-control")]')

        if len(respuestas)!= 2:
            raise ValueError('Pregunta Gift')
        
        bien = []
        respuesta = []
        solucion = []
        for i, respuesta_i in enumerate(respuestas):
            res = hover[i].get_attribute("innerHTML").split('<br>')
            respuesta.append(respuesta_i.get_attribute('value'))
            solucion.append(res[1][25:])
            if res[0] == 'Correcto':
                bien.append('True')
            else:
                bien.append('False')
    except:
        # Preguntas de una respuesta (Gift)   
        try:
            # bien
            respuesta = driver.find_element_by_tag_name(
                "input[class='form-control d-inline correct']").get_attribute('value')
            bien = 'True'
        except:
            # mal
            respuesta = driver.find_element_by_tag_name(
                "input[class='form-control d-inline incorrect']").get_attribute('value')
            bien = 'False'

    try:
    # buscar solucion
    # solo vale para Gift
        solucion = driver.find_element_by_css_selector(
            'div.rightanswer').text[25:]
    except:
        pass

    return '{};{};{};{};{}\n'.format(nombre, pregunta, respuesta, solucion, bien)




site_login()

# attemps = [263398, 263431, 263474, 263600, 263351, 263508, 263739, 263465, 263491]
# # attemps = [263431]

text_file = open("attemps.txt", "r")
attemps = text_file.read().split('\n')
# print(attemps)

with open('output_teoria.csv', 'w') as file:
    for intento in attemps:
        for slot in range(12):
            url_pregunta = 'https://moodl...../mod/quiz/reviewquestion.php?attempt={}&slot={}'.format(intento, slot+1)
            # print(go_to_question(url_pregunta))
            file.write(go_to_question(url_pregunta))


text_file = open("attemps_problemas_2.txt", "r")
attemps = text_file.read().split('\n')

# # attemps =  [265207,265208,265209,265210,265211, 265226, 265227, 265228]


with open('output_preguntas2.csv', 'w') as file:
    for intento in attemps:
        for slot in range(3):
            url_pregunta = 'https://moodle...../mod/quiz/reviewquestion.php?attempt={}&slot={}'.format(
                intento, slot+1)
            # print(go_to_problema(url_pregunta))
            file.write(go_to_problema(url_pregunta))
