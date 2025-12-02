from flask import Flask, render_template
from flask_login import LoginManager
from config import Config
from models import db, Usuario
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Debes iniciar sesión para acceder.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))
    
    from controllers.auth_controller import auth_bp
    from controllers.main_controller import main_bp
    from controllers.carrera_controller import carrera_bp
    from controllers.materia_controller import materia_bp
    from controllers.persona_controller import persona_bp
    from controllers.estudiante_controller import estudiante_bp
    from controllers.docente_controller import docente_bp
    from controllers.asignacion_controller import asignacion_bp
    from controllers.inscripcion_controller import inscripcion_bp
    from controllers.nota_controller import nota_bp
    from controllers.usuario_controller import usuario_bp
    from controllers.rol_controller import rol_bp
    from controllers.reporte_controller import reporte_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(carrera_bp)
    app.register_blueprint(materia_bp)
    app.register_blueprint(persona_bp)
    app.register_blueprint(estudiante_bp)
    app.register_blueprint(docente_bp)
    app.register_blueprint(asignacion_bp)
    app.register_blueprint(inscripcion_bp)
    app.register_blueprint(nota_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(rol_bp)
    app.register_blueprint(reporte_bp)
    
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    from utils.helpers import format_date, format_datetime
    app.jinja_env.filters['format_date'] = format_date
    app.jinja_env.filters['format_datetime'] = format_datetime
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    with app.app_context():
        db.create_all()
        
        from seed_data import init_data
        init_data()
    
    app.run(debug=True, host='0.0.0.0', port=5000)