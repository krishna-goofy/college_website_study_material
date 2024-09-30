from flask import Flask, render_template
from db import db  # Ensure this imports your db object
import os
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///study_material.db'
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')

    csrf = CSRFProtect(app)  # Initialize CSRF protection

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    db.init_app(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Import routes here to avoid circular imports
    from admin.routes import admin_bp
    from user.routes import user_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(user_bp, url_prefix='/user')

    @app.route('/')
    def home():
        return render_template('home.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
