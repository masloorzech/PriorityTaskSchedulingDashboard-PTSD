

def register_blueprints(app):
    from .users import users_bp
    from .tasks import tasks_bp
    from .weather import weather_bp

    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(tasks_bp, url_prefix="/tasks")
    app.register_blueprint(weather_bp, url_prefix="/weather")
