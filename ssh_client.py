import warnings
warnings.filterwarnings("ignore")

import paramiko
import sys
import time
from typing import Optional
from colorama import init, Fore, Style
try:
    import pyreadline3.readline as readline
except ImportError:
    try:
        import readline
    except ImportError:
        readline = None

init(autoreset=True)

class SSHClient:
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        self.current_path = "~"
        self.setup_autocomplete()
    
    def connect(self, hostname: str, username: str, password: Optional[str] = None, 
                key_filename: Optional[str] = None, port: int = 22) -> bool:
        """Подключение к SSH серверу"""
        print(f"Подключение к {hostname}:{port}...", end="")
        sys.stdout.flush()
        
        try:
            self.client.connect(
                hostname=hostname,
                username=username,
                password=password,
                key_filename=key_filename,
                port=port,
                timeout=10
            )
            print(f"\r{Fore.GREEN}✓ Подключен к {hostname}:{port}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"\r{Fore.RED}✗ Ошибка подключения к {hostname}: {e}{Style.RESET_ALL}")
            return False
    
    def execute_command(self, command: str) -> tuple:
        """Выполнение команды на удаленном сервере"""
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            
            # Потоковый вывод в реальном времени
            while True:
                line = stdout.readline()
                if not line:
                    break
                print(line.rstrip(), flush=True)
            
            # Проверяем ошибки
            error = stderr.read().decode('utf-8')
            return "", error
        except Exception as e:
            return "", str(e)
    
    def setup_autocomplete(self):
        """Настройка автодополнения"""
        if readline:
            readline.set_completer(self.complete)
            readline.parse_and_bind("tab: complete")
            readline.set_completer_delims(' \t\n`!@#$%^&*()=+[{]}\\|;:\'\",<>?')
    
    def complete(self, text, state):
        """Функция автодополнения"""
        try:
            line = readline.get_line_buffer()
            if line.startswith('cd '):
                return self.complete_path(text, state)
            else:
                return self.complete_command(text, state)
        except:
            return None
    
    def complete_path(self, text, state):
        """Автодополнение путей"""
        try:
            if not hasattr(self, '_path_matches'):
                stdin, stdout, stderr = self.client.exec_command(f'ls -1a {text}* 2>/dev/null')
                paths = stdout.read().decode('utf-8').strip().split('\n')
                self._path_matches = [p for p in paths if p and p.startswith(text.split('/')[-1])]
            
            if state < len(self._path_matches):
                return self._path_matches[state]
        except:
            pass
        
        if state == 0:
            delattr(self, '_path_matches') if hasattr(self, '_path_matches') else None
        return None
    
    def complete_command(self, text, state):
        """Автодополнение команд"""
        commands = ['ls', 'cd', 'pwd', 'cat', 'grep', 'find', 'ps', 'top', 'df', 'free', 'uname', 'whoami']
        matches = [cmd for cmd in commands if cmd.startswith(text)]
        
        if state < len(matches):
            return matches[state]
        return None
    
    def close(self):
        """Закрытие соединения"""
        self.client.close()
        print("Соединение закрыто")

def main():
    ssh = SSHClient()
    
    # Параметры подключения
    hostname = input("Введите IP адрес сервера: ")
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль (или Enter для ключа): ")
    
    if not password:
        key_path = input("Путь к приватному ключу: ")
        connected = ssh.connect(hostname, username, key_filename=key_path)
    else:
        connected = ssh.connect(hostname, username, password=password)
    
    if not connected:
        return
    
    # Интерактивный режим
    try:
        while True:
            command = input(f"{username}@{hostname}:~$ ")
            if command.lower() in ['exit', 'quit']:
                break
            
            output, error = ssh.execute_command(command)
            if output:
                print(output)
            if error:
                print(f"Ошибка: {error}")
    
    except KeyboardInterrupt:
        print("\nВыход...")
    finally:
        ssh.close()

if __name__ == "__main__":
    main()