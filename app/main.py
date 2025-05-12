from __init__ import create_app
from config.settings import Config

app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0", 
        port=Config.FLASK_PORT, 
        debug=Config.DEBUG
    )
