# chatbot-flask
El presente proyecto consiste en la implementación de un chatbot, utilizando como tecnologías principales Python (Flask) para el back-end ; HTML, JavaScript y Tailwind para el front-end y SQLite para el almacenamiento de datos. La aplicación se conecta con una API de Anthropic (Claude), hacia la cual se envía la información (mensaje de chat) y posteriormente se almacena la respuesta entregada por el modelo y se muestra como la respuesta al mensaje enviado inicialmente por el usuario.

## Instrucciones de uso
La implementación en sí está bastante automatizada, de modo que los pasos para la implementación de la aplicación son relativamente breves:

1. Instalar las librerías necesarias para el funcionamiento de la app, para ello está incluido un archivo txt con las librerías necesarias. Para su instalación, simplemente ejecutar el comando:
   ```bash
   pip install -r requirements.txt
   
2. Una vez instaladas las librerías, se debe crear la variable de entorno .env. Para ello, solo basta con copiar el contenido del archivo .env.example y adicionalmente se debe completar la clave para la api de Anthropic desde la variable ANTHROPIC_API_KEY

3. Finalmente,ya con todo configurado, solo basta con ejecutar el script que monta la aplicación Flask con el comando:
   ```bash
   python run.py

## Base de datos
La base de datos implementada, se crea automáticamente dentro del directorio del proyecto gracias al script db.py (ubicado en /app). Esta implementación sigue las indicaciones del documento entregado y se modela de la siguiente manera:

![Ejemplo](https://i.gyazo.com/d2aecc05f82c457bdba280039bd315a3.png)

Donde las relaciones entre cada tabla son 1:n  y cada llave primaria (PK) posee además un autoincremento para llevar un registro ordenado de los flujos de datos que se procesan en la app.

## Funcionalidades (y endpoints asociados)
Ya con el proyecto en funcionamiento, es sumamente importante mencionar las funcionalidades con las que cuenta.<br>

Primeramente, al ingresar al directorio principal de la aplicación (http://127.0.0.1:5000/) se puede visualizar el apartado de login.<br>

Aquí, el usuario debe ingresar su username para ingresar al chat. En caso de no estar registrado previamente, se hará una inserción en la tabla de usuarios y será redirigido al chat. Todo esto se realiza en el endpoint /login, con los datos recibidos del formulario de login de la vista index.html.
<br><br>
Ya dentro del apartado de chat, en caso de existir alguna conversación (o más de una conversación, lo cual se valida mediante el endpoint /history/user_id) previa asociada al usuario, se mostrará por defecto la última conversación disponible, pudiendo además navegar entre las conversaciones que existan (en donde los mensajes respectivos se extraen del endpoint /conversation/conversation_id). <br>
En caso de existir menos de 10 conversaciones, el usuario podrá crear una nueva conversación presionando el botón "nueva conversación", en donde simplemente debe escribir un mensaje y esperar la respuesta del asistente IA, creando así una nueva conversación (todo lo anterior validandose mediante el endpoint /chat). Para explicar de forma más detallada el flujo de los datos dentro de un chat, se adjunta el siguiente diagrama de flujo (además, se recomienda revisar los comentarios a lo largo del código):

![Ejemplo](https://i.gyazo.com/d2aecc05f82c457bdba280039bd315a3.png)


