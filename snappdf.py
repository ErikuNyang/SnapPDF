import os
import subprocess
import sys

# 가상 환경 폴더 이름
VENV_DIR = 'venv'

def create_virtualenv():
    """가상 환경을 생성합니다."""
    if not os.path.exists(VENV_DIR):
        subprocess.check_call([sys.executable, '-m', 'venv', VENV_DIR])
        print(f"Virtual environment '{VENV_DIR}' created.")
    else:
        print(f"Virtual environment '{VENV_DIR}' already exists.")

def check_installed_packages():
    """필요한 패키지가 설치되어 있는지 확인합니다."""
    # 설치된 패키지 목록을 확인하기 위한 명령어
    result = subprocess.run([os.path.join(VENV_DIR, 'Scripts', 'python'), '-m', 'pip', 'freeze'],
                            capture_output=True, text=True)
    installed_packages = result.stdout.splitlines()

    # requirements.txt 파일 읽기
    with open('requirements.txt', 'r') as f:
        required_packages = f.read().splitlines()

    # requirements 설치 확인
    for package in required_packages:
        if package not in installed_packages:
            print(f"Package '{package}' is missing and will be installed.")
            return False
    print("All required packages are already installed.")
    return True

def install_requirements():
    """필요한 라이브러리를 설치합니다."""
    # pip 업그레이드
    subprocess.check_call([os.path.join(VENV_DIR, 'Scripts', 'python'), '-m', 'pip', 'install', '--upgrade', 'pip'])

    # requirements.txt 파일에 있는 라이브러리를 최신버젼으로 설치
    subprocess.check_call([os.path.join(VENV_DIR, 'Scripts', 'python'), '-m', 'pip', 'install', '-U', '-r', 'requirements.txt'])
    print("All required libraries have been installed.")

def run_flask_app():
    """Flask 앱을 실행합니다."""
    os.environ['FLASK_APP'] = 'app.py'
    os.environ['FLASK_ENV'] = 'development'
    subprocess.check_call([os.path.join(VENV_DIR, 'Scripts', 'python'), 'app.py'])

if __name__ == '__main__':
    # 가상 환경 생성
    create_virtualenv()

    # 패키지 확인 및 설치
    if not check_installed_packages():
        install_requirements()

    # Flask 앱 실행
    run_flask_app()
