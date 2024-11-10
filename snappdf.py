import os
import subprocess
import sys

# 가상 환경 이름
VENV_DIR = 'venv'

def create_virtualenv():
    """가상 환경을 생성하고 활성화합니다."""
    # 가상 환경 생성
    if not os.path.exists(VENV_DIR):
        subprocess.check_call([sys.executable, '-m', 'venv', VENV_DIR])
        print(f"Virtual environment '{VENV_DIR}' created.")
    else:
        print(f"Virtual environment '{VENV_DIR}' already exists.")

def install_requirements():
    """requirements.txt 파일을 읽고 필요한 라이브러리를 설치합니다."""
    # pip 업그레이드
    subprocess.check_call([os.path.join(VENV_DIR, 'Scripts', 'python'), '-m', 'pip', 'install', '--upgrade', 'pip'])

    # requirements.txt 파일이 있는지 확인하고, 라이브러리 설치
    if os.path.exists('requirements.txt'):
        subprocess.check_call([os.path.join(VENV_DIR, 'Scripts', 'python'), '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("All required libraries have been installed.")
    else:
        print("requirements.txt file not found. Please create one with the required libraries.")

def run_flask_app():
    """Flask 앱을 실행합니다."""
    # 환경 변수 설정
    os.environ['FLASK_APP'] = 'app.py'
    os.environ['FLASK_ENV'] = 'development'

    # Flask 서버 실행
    subprocess.check_call([os.path.join(VENV_DIR, 'Scripts', 'python'), 'app.py'])

if __name__ == '__main__':
    create_virtualenv()
    install_requirements()
    run_flask_app()