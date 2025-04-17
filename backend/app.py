from src import config, app
from src.routes import api

if __name__ == "__main__":
    app.run(host= config.HOST,
            port= config.PORT,
            debug= config.DEBUG)