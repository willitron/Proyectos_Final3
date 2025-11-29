

from PIL import Image, ImageDraw, ImageFont
import os

def create_institutional_logo():
    os.makedirs('static/img', exist_ok=True)
    
    size = 500
    
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    azul_principal = (26, 35, 126, 255)  
    azul_claro = (40, 53, 147, 255)      
    blanco = (255, 255, 255, 255)
    dorado = (255, 193, 7, 255)
    
    draw.ellipse([20, 20, 480, 480], fill=None, outline=dorado, width=8)
    
    draw.ellipse([40, 40, 460, 460], fill=azul_principal, outline=blanco, width=6)
    
    book_width = 200
    book_height = 140
    book_x = (size - book_width) // 2
    book_y = 150
    
    left_page = [
        (book_x, book_y),
        (book_x + book_width // 2 - 10, book_y),
        (book_x + book_width // 2 - 5, book_y + book_height),
        (book_x + 20, book_y + book_height)
    ]
    draw.polygon(left_page, fill=blanco, outline=azul_claro)
    
    right_page = [
        (book_x + book_width // 2 + 10, book_y),
        (book_x + book_width, book_y),
        (book_x + book_width - 20, book_y + book_height),
        (book_x + book_width // 2 + 5, book_y + book_height)
    ]
    draw.polygon(right_page, fill=blanco, outline=azul_claro)
    
    for i in range(3):
        y_pos = book_y + 40 + i * 25
        draw.line([(book_x + 30, y_pos), (book_x + book_width // 2 - 30, y_pos)], 
                 fill=azul_claro, width=3)
        draw.line([(book_x + book_width // 2 + 30, y_pos), (book_x + book_width - 30, y_pos)], 
                 fill=azul_claro, width=3)
    
    try:
        try:
            font_large = ImageFont.truetype("arialbd.ttf", 80)
            font_small = ImageFont.truetype("arial.ttf", 40)
        except:
            try:
                font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
                font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
            except:
                font_large = ImageFont.load_default()
                font_small = ImageFont.load_default()
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    text_main = "IB"
    bbox = draw.textbbox((0, 0), text_main, font=font_large)
    text_width = bbox[2] - bbox[0]
    text_x = (size - text_width) // 2
    text_y = 310
    
    draw.text((text_x + 2, text_y + 2), text_main, fill=(0, 0, 0, 128), font=font_large)
    # Texto principal
    draw.text((text_x, text_y), text_main, fill=dorado, font=font_large)
    
    text_bottom = "INSTITUTO"
    bbox_bottom = draw.textbbox((0, 0), text_bottom, font=font_small)
    text_width_bottom = bbox_bottom[2] - bbox_bottom[0]
    text_x_bottom = (size - text_width_bottom) // 2
    draw.text((text_x_bottom, 390), text_bottom, fill=blanco, font=font_small)
    
    output_path = 'static/img/logo.png'
    img.save(output_path)
    print(f"✅ Logo creado exitosamente en: {output_path}")
    print(f"📏 Dimensiones: {size}x{size} píxeles")
    print(f"📁 Tamaño del archivo: {os.path.getsize(output_path) / 1024:.2f} KB")
    
    img_small = img.resize((150, 150), Image.LANCZOS)
    small_path = 'static/img/logo_small.png'
    img_small.save(small_path)
    print(f"✅ Logo pequeño creado en: {small_path}")
    
    return output_path

def create_simple_logo():
    os.makedirs('static/img', exist_ok=True)
    
    size = 500
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    draw.ellipse([50, 50, 450, 450], fill=(26, 35, 126, 255), outline=(255, 193, 7, 255), width=10)
    
    try:
        font = ImageFont.truetype("arialbd.ttf", 150)
    except:
        font = ImageFont.load_default()
    
    text = "IB"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((size - text_width) // 2, (size - text_height) // 2 - 30)
    
    draw.text(position, text, fill=(255, 193, 7, 255), font=font)
    
    output_path = 'static/img/logo.png'
    img.save(output_path)
    print(f"✅ Logo simple creado en: {output_path}")
    
    return output_path

if __name__ == '__main__':
    print("=" * 60)
    print("GENERADOR DE LOGO - INSTITUTO BALLIVIÁN")
    print("=" * 60)
    print()
    
    try:
        create_institutional_logo()
        print()
        print("Logo profesional generado correctamente!")
        print()
        print("Próximos pasos:")
        print("1. Revisa el logo en: static/img/logo.png")
        print("2. Si deseas personalizarlo, puedes:")
        print("   - Reemplazarlo con tu propio logo")
        print("   - Editar este script para cambiar colores/diseño")
        print("3. El logo aparecerá automáticamente en todos los PDFs")
        print()
        print("Tip: Para mejor calidad, usa un logo PNG de 500x500px")
        
    except Exception as e:
        print(f"⚠️  Error creando logo profesional: {e}")
        print("Creando logo simple alternativo...")
        try:
            create_simple_logo()
            print("Logo simple creado correctamente")
        except Exception as e2:
            print(f"Error creando logo: {e2}")
            print()
            print("Por favor, crea manualmente un logo y guárdalo en:")
            print("static/img/logo.png")
    
    print()
    print("=" * 60)