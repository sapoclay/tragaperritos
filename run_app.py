import os
import sys
import platform
import subprocess
import venv
from pathlib import Path

def is_venv_exists():
    venv_dir = 'venv'
    return os.path.exists(venv_dir) and os.path.isdir(venv_dir)

def create_venv():
    print("Creando el entorno virtual...")
    venv.create('venv', with_pip=True)
    activate_venv()

def get_python_executable():
    if platform.system().lower() == 'windows':
        return os.path.join('venv', 'Scripts', 'python.exe')
    return os.path.join('venv', 'bin', 'python')

def get_pip_executable():
    if platform.system().lower() == 'windows':
        return os.path.join('venv', 'Scripts', 'pip.exe')
    return os.path.join('venv', 'bin', 'pip')

def install_requirements():
    pip_exe = get_pip_executable()
    requirements_file = 'requirements.txt'
    
    if not os.path.exists(requirements_file):
        print(f"Error: {requirements_file} not found")
        sys.exit(1)
    
    print("Instalando dependencias desde requirements.txt...")
    subprocess.run([pip_exe, 'install', '-r', requirements_file], check=True)

def run_main_app():
    python_exe = get_python_executable()
    main_file = 'tragaperritos.py'
    
    if not os.path.exists(main_file):
        print(f"Error: {main_file} not found")
        sys.exit(1)
    
    print("Iniciando la aplicación...")
    subprocess.run([python_exe, main_file], check=True)

def activate_venv():
    venv_dir = 'venv'
    if platform.system().lower() == 'windows':
        activate_script = os.path.join(venv_dir, 'Scripts', 'activate.bat')
    else:
        activate_script = os.path.join(venv_dir, 'bin', 'activate')

    if not os.path.exists(activate_script):
        print(f"Error: El script de activación del entorno virtual no ha funcionado {activate_script}")
        sys.exit(1)

    print("Activando el entorno virtual...")
    try:
        if platform.system().lower() == 'windows':
            subprocess.run(['cmd', '/c', activate_script], check=True)
        else:
            subprocess.run(['source', activate_script], check=True)

        # Activar el entorno virtual en el script
        venv_path = os.path.abspath(venv_dir)
        os.environ['VIRTUAL_ENV'] = venv_path
        os.environ['PATH'] = os.path.join(venv_path, 'Scripts' if platform.system().lower() == 'windows' else 'bin') + os.pathsep + os.environ.get('PATH', '')
        # Elimina PYTHONHOME si existe, ya que puede interferir con el entorno virtual
        os.environ.pop('PYTHONHOME', None)
        print("Entorno virtual activado correctamente!")
    except subprocess.CalledProcessError as e:
        print(f"Error activando el entorno virtual: {e}")
        sys.exit(1)

def main():
    # Cambiar al directorio que contenga este script
    os.chdir(Path(__file__).parent)
    
    if not is_venv_exists():
        create_venv()
    else:
        activate_venv()
    
    try:
        install_requirements()
        run_main_app()
    except subprocess.CalledProcessError as e:
        print(f"Error ocurrido: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()