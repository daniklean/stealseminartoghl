from flask import Flask

def create_app(config_object="config.settings.Config"):
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__)
    if isinstance(config_object, str):
        app.config.from_object(config_object)
    else:
        app.config.from_mapping(config_object)

    from controllers.webhooks_controller import webhook_bp
    app.register_blueprint(webhook_bp)
    return app
