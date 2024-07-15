import subprocess
import sys
import os

# Función para instalar o actualizar paquetes
def install_or_update_packages(requirements_file='requirements.txt'):
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pipreqs'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        try:
            with open(requirements_file, 'r') as f:
                required_packages = f.readlines()
            required_packages = [pkg.strip() for pkg in required_packages]
        except FileNotFoundError:
            required_packages = []

        installed_packages = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
        installed_packages = installed_packages.decode('utf-8').split('\n')
        
        installed_dict = {}
        for pkg in installed_packages:
            if '==' in pkg:
                pkg_name, pkg_version = pkg.split('==')
                installed_dict[pkg_name] = pkg_version

        for pkg in required_packages:
            pkg_name, pkg_version = pkg.split('==')
            if pkg_name in installed_dict:
                if pkg_version != installed_dict[pkg_name]:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', pkg])
            else:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg])
    
    except subprocess.CalledProcessError as e:
        print(f"Error al instalar/actualizar paquetes: {e}")
