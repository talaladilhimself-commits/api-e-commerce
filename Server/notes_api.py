import connexion
from config import CONFIG
from create_db import try_create_database

app = connexion.FlaskApp(__name__)

try_create_database()

port = int(CONFIG["server"]["port"])
app.add_api("notes-api.yaml")

app.debug = True

app.run(host=CONFIG["server"]["listen_ip"], port=port)
