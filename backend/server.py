from waitress import serve
from core.wsgi import application  

serve(application, host='127.0.0.1', port=8000)
