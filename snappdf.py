import os
import subprocess
import sys

# Virtual Environment directory name
VENV_DIR = 'venv'

# OS-specific path settings
if os.name == 'nt':  # Windows
    PYTHON_PATH = os.path.join(VENV_DIR, 'Scripts', 'python')
else:  # Linux/Mac
    PYTHON_PATH = os.path.join(VENV_DIR, 'bin', 'python')

def create_virtualenv():
    """Creates a virtual environment if it doesn't exist."""
    if not os.path.exists(VENV_DIR):
        subprocess.check_call([sys.executable, '-m', 'venv', VENV_DIR])
        print(f"Virtual environment '{VENV_DIR}' created.")
    else:
        print(f"Virtual environment '{VENV_DIR}' already exists.")

def check_installed_packages():
    """Checks if all required packages are installed in the virtual environment."""
    # Checking installed package list
    result = subprocess.run([PYTHON_PATH, '-m', 'pip', 'freeze'],
                            capture_output=True, text=True)
    installed_packages = result.stdout.splitlines()

    # Reading requirements.txt
    with open('requirements.txt', 'r') as f:
        required_packages = f.read().splitlines()

    # Checking requirements in installed package list
    for package in required_packages:
        if package not in installed_packages:
            print(f"Package '{package}' is missing and will be installed.")
            return False
    print("All required packages are already installed.")
    return True

def install_requirements():
    """Installs or upgrades packages specified in requirements.txt."""
    # Upgrading PIP
    subprocess.check_call([PYTHON_PATH, '-m', 'pip', 'install', '--upgrade', 'pip'])

    # Installing libraries in requirements.txt
    subprocess.check_call([PYTHON_PATH, '-m', 'pip', 'install', '-U', '-r', 'requirements.txt'])
    print("All required libraries have been installed.")

def run_flask_app():
    """Sets Flask environment variables and runs the Flask app."""
    os.environ['FLASK_APP'] = 'app.py'
    os.environ['FLASK_ENV'] = 'development'
    subprocess.check_call([PYTHON_PATH, 'app.py'])

if __name__ == '__main__':
    # Set up virtual environment
    create_virtualenv()

    # Check for required packages and install if missing
    if not check_installed_packages():
        install_requirements()

    # Run the Flask app
    run_flask_app()
