import subprocess
import sys
import os

def generate_requirements_file(output_file='requirements.txt'):
    try:
        subprocess.check_call([sys.executable, '-m', 'pipreqs', '--force', '.'])
    except subprocess.CalledProcessError as e:
        print(f"Error al generar el archivo requirements.txt: {e}")