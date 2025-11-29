import os
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file, subfolder=''):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
        os.makedirs(upload_path, exist_ok=True)
        
        file_path = os.path.join(upload_path, filename)
        file.save(file_path)
        
        return os.path.join(subfolder, filename)
    return None

def delete_file(file_path):
    try:
        full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_path)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
    except Exception as e:
        print(f"Error eliminando archivo: {e}")
    return False

def format_date(date_obj):
    if date_obj:
        return date_obj.strftime('%d/%m/%Y')
    return ''

def format_datetime(datetime_obj):
    if datetime_obj:
        return datetime_obj.strftime('%d/%m/%Y %H:%M')
    return ''