# chatbot-flask
Implementacion de chatbot, utilizando flask, HTML, JavaScript, Python, y tailwind

## Instrucciones de uso
La implementación en si está bastante automatizada, de modo que los pasos para la implementación de la aplicación son relativamente breves:

1. Instalar las librerias necesarias para el funcionamiento de la app, para ello está incluido un archivo txt con las librerias necesarias. Para instalar entonces las dependencias, simplemente ejecutar el comando:
   ```bash
   pip install -r requirements.txt
   
2. Una vez instaladas las librerias, se debe crear la variable de entorno .env. Para ello, solo basta con copiar el contenido del archivo .env.example y adicionalmente se debe completar la clave para la api de Anthropic desde la variable ANTHROPIC_API_KEY

3. Finalmente,ya con todo configurado, solo basta con ejecutar el sript que monta la aplicación Flask con el comando:
   ```bash
   python run.py

## Base de datos
La base de datos implementada, se crea automaticamente dentro del directorio del proyecto gracias al script db.py (ubicado en /app). Esta implementación sigue las indicaciones del documento entregado y se modela de la siguiente manera:
![Ejemplo](https://i.gyazo.com/d2aecc05f82c457bdba280039bd315a3.png)
Donde las relaciones entre cada tabla son 1:n  y cada llave primaria (PK) posee además un autoincremento para llevar un registro ordenado de los flujos de datos que se procesan en la app.


