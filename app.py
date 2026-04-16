import os
from flask import Flask, redirect, url_for
from flask_login import LoginManager, current_user
from models import db, User

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'super-secret-cashx-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cashx.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from routes_auth import auth_bp
    from routes_dashboard import dashboard_bp
    from routes_services import services_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(services_bp)

    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.home'))
        return redirect(url_for('auth.login'))

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)
