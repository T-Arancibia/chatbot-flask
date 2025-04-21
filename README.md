# chatbot-flask
Implementacion de chatbot, utilizando flask, HTML, JavaScript, Python, y tailwind

## Instrucciones de uso
La implementación en si está bastante automatizada, de modo que los pasos para la implementación de la aplicación son relativamente breves:

1. Instalar las librerias necesarias para el funcionamiento de la app, para ello está incluido un archivo txt con las librerias necesarias. Para instalar entonces las dependencias, simplemente ejecutar el comando:
   ```bash
   pip install -r requirements.txt
2. Una vez instaladas las dependencias, se debe crear la variable de entorno .env. Para ello, solo basta con copiar el contenido del archivo .env.example y adicionalmente se debe completar la clave para la api de Anthropic desde la variable ANTHROPIC_API_KEY
3. Finalmente,ya con todo configurado, solo basta con ejecutar el sript que monta la aplicación Flask con el comando:
   ```bash
   python run.py
