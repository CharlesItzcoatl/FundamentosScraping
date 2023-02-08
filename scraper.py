import requests
# La función html es la que permite convertir un archivo .html a un archivo especial 
# al que se puede aplicar XPath.
import lxml.html as html
# La combinación de estas dos clases nos permite crear la carpeta que guarde las noticias.
import os
import datetime

# Usar el sagrado text-fill porque poner h2 no funciona.
HOME_URL = 'https://www.larepublica.co/'
XPATH_LINK_TO_ARTICLE = '//text-fill/a/@href'
XPATH_TITLE = '//div[@class = "mb-auto"]/text-fill/span/text()'
XPATH_SUMMARY = '//div[@class = "lead"]/p/text()'
XPATH_BODY = '//div[@class = "html-content"]/p[not(@class)]/text()'


def parse_notice(link, today):
    # try para obtener la información de cada link.
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            # try para obtener cada elemento de nuestro interés; título, resumen y cuerpo.
            try:
                # El método parsed nos devuelve un html con superpoderes
                # y el método xpath devuelve una lista que puede obtener varios elementos, 
                # pero sabemos que sólo es un título.
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                # En el caso del cuerpo, sabemos que esta lista contiene varios elementos, los cuales corresponden a cada
                # párrafo.
                body = parsed.xpath(XPATH_BODY)
            # Puede ocurrir que una noticia no cuente con resumen, por lo que el índice 0 nunca existirá y se eleva la
            # excepción. Las noticias que no cuenten con estos elementos no nos sirven.
                
            except IndexError:
                return

            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    # El sagrado try para elevar excepciones cuando ocurren errores como la obtención de un link.
    try:
        response = requests.get(HOME_URL)
        # Devuelve el código de estado.
        if response.status_code == 200:
            # El atributo content devuelve el documento html de la respuesta.
            # El método decode permite transformar los caracteres especiales en algo
            # que Python puede manejar sin problemas.
            home = response.content.decode('utf-8')
            # La variable parsed obtiene el contenido html de home y lo transforma en un
            # documento especial en el que se puede usar XPath.
            parsed = html.fromstring(home)
            # Obtiene una lista resultado de aplicar el XPath a la lista de links.
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            #print(links_to_notices)
            # Obtiene la fecha actual en el formato indicado.
            today = datetime.date.today().strftime('%d-%m-%Y')
            # Si no existe la carpeta/dirección con este nombre, crea la carpeta con nombre igual a today.
            if not os.path.isdir(today):
                os.mkdir(today)
                # Para cada elemento de la lista links_to_notices:
                for link in links_to_notices:
                    #print(link)
                    # Función que, de cada link, obtenga el título, resumen y cuerpo y lo guarde usando la fecha de hoy.
                    parse_notice(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == '__main__':
    run()


