import subprocess
import sys
import os

def build_exe():
    """Сборка программы в исполняемый файл"""
    
    # Проверяем наличие PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print("Устанавливаю PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Команда для сборки
    cmd = [
        "pyinstaller",
        "--onefile",                    # Один файл
        "--name=sshlite",              # Имя файла
        "--console",                   # Консольное приложение
        "--clean",                     # Очистить кэш
        "main.py"
    ]
    
    print("Начинаю сборку sshlite.exe...")
    try:
        subprocess.run(cmd, check=True)
        print("\n✓ Сборка завершена!")
        print("Исполняемый файл: dist/sshlite.exe")
    except subprocess.CalledProcessError as e:
        print(f"✗ Ошибка сборки: {e}")

if __name__ == "__main__":
    build_exe()