from app import create_app
from models import db
from seed_data import init_data

def init_database():
    print("=" * 60)
    print("INICIALIZANDO BASE DE DATOS SQLite")
    print("=" * 60)
    print()
    
    app = create_app()
    
    with app.app_context():
        print(" Eliminando tablas existentes...")
        db.drop_all()
        print("Tablas eliminadas")
        print()
        
        print("Creando estructura de tablas...")
        db.create_all()
        print("Tablas creadas exitosamente")
        print()
        
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        print("Tablas creadas en la base de datos:")
        for i, table in enumerate(tables, 1):
            print(f"   {i:2d}. {table}")
        print()
        
        print("Cargando datos de prueba...")
        init_data()
        
        print()
        print("=" * 60)
        print("BASE DE DATOS INICIALIZADA CORRECTAMENTE")
        print("=" * 60)
        print()
        print("Archivo de base de datos: instituto_ballivian.db")
        print()
        print("Usuarios de prueba:")
        print("   • admin / admin123 (Administrador)")
        print("   • secretaria / secretaria123 (Secretaria)")
        print("   • docente / docente123 (Docente)")
        print("   • estudiante / estudiante123 (Estudiante)")
        print()
        print("Para iniciar la aplicación: python app.py")
        print()

if __name__ == '__main__':
    init_database()