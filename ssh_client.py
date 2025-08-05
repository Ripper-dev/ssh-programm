import paramiko
import sys
from typing import Optional

class SSHClient:
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
    
    def connect(self, hostname: str, username: str, password: Optional[str] = None, 
                key_filename: Optional[str] = None, port: int = 22) -> bool:
        """Подключение к SSH серверу"""
        try:
            self.client.connect(
                hostname=hostname,
                username=username,
                password=password,
                key_filename=key_filename,
                port=port,
                timeout=10
            )
            print(f"✓ Подключен к {hostname}:{port}")
            return True
        except Exception as e:
            print(f"✗ Ошибка подключения к {hostname}: {e}")
            return False
    
    def execute_command(self, command: str) -> tuple:
        """Выполнение команды на удаленном сервере"""
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            return output, error
        except Exception as e:
            return "", str(e)
    
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