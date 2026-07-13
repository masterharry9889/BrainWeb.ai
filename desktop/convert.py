import sys
from PIL import Image

def convert():
    input_path = r'd:\INGOT.ai\frontend\logo\21b08db87f66fdbe20e5f52fa9ddb93f.webp'
    output_ico = r'd:\INGOT.ai\desktop\icon.ico'
    output_png = r'd:\INGOT.ai\desktop\build\icon.png'
    
    try:
        img = Image.open(input_path)
        img = img.convert("RGBA")
        
        # Save ICO
        # Next.js might want multiple sizes or standard 32x32 for favicon, but let's just do standard icon sizes.
        # Actually Next.js usually likes 32x32 or 48x48.
        icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
        img.save(output_ico, format='ICO', sizes=icon_sizes)
        print("ICO created successfully.")
        
        # Save PNG for build
        img_large = img.resize((512, 512), Image.Resampling.LANCZOS)
        img_large.save(output_png, format='PNG')
        print("PNG created successfully.")
        
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    convert()
