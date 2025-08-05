from ssh_client import SSHClient
from config import ServerConfig

def show_menu():
    print("\n=== SSH Клиент ===\nАвтор: dxddy/dante\n")
    print("1. Подключиться к серверу")
    print("2. Показать сохраненные серверы")
    print("3. Добавить сервер в конфигурацию")
    print("4. Выход")
    return input("Выберите опцию: ")

def connect_to_server():
    config = ServerConfig()
    servers = config.get_servers()
    
    if servers:
        print("\nСохраненные серверы:")
        for i, server in enumerate(servers, 1):
            print(f"{i}. {server['name']} ({server['hostname']})")
        print(f"{len(servers) + 1}. Ввести данные вручную")
        
        choice = input("Выберите сервер: ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(servers):
                server = servers[choice - 1]
                ssh = SSHClient()
                
                if 'password' in server:
                    connected = ssh.connect(server['hostname'], server['username'], 
                                          password=server['password'], port=server['port'])
                else:
                    connected = ssh.connect(server['hostname'], server['username'], 
                                          key_filename=server.get('key_path'), port=server['port'])
                
                if connected:
                    interactive_session(ssh, server['username'], server['hostname'])
                return
        except ValueError:
            pass
    
    # Ручной ввод
    hostname = input("IP адрес сервера: ")
    username = input("Имя пользователя: ")
    password = input("Пароль (Enter для ключа): ")
    
    ssh = SSHClient()
    if password:
        connected = ssh.connect(hostname, username, password=password)
    else:
        key_path = input("Путь к ключу: ")
        connected = ssh.connect(hostname, username, key_filename=key_path)
    
    if connected:
        interactive_session(ssh, username, hostname)

def interactive_session(ssh: SSHClient, username: str, hostname: str):
    print(f"\nИнтерактивная сессия с {hostname}")
    print("Введите 'exit' для выхода")
    
    try:
        while True:
            command = input(f"{username}@{hostname}:~$ ")
            if command.lower() in ['exit', 'quit']:
                break
            
            output, error = ssh.execute_command(command)
            if output:
                print(output.strip())
            if error:
                print(f"Ошибка: {error.strip()}")
    
    except KeyboardInterrupt:
        print("\nВыход из сессии...")
    finally:
        ssh.close()

def add_server():
    config = ServerConfig()
    
    name = input("Название сервера: ")
    hostname = input("IP адрес: ")
    username = input("Имя пользователя: ")
    port = input("Порт (22): ") or "22"
    
    auth_type = input("Тип авторизации (1-пароль, 2-ключ): ")
    
    if auth_type == "1":
        password = input("Пароль: ")
        config.add_server(name, hostname, username, password=password, port=int(port))
    else:
        key_path = input("Путь к ключу: ")
        config.add_server(name, hostname, username, key_path=key_path, port=int(port))
    
    print("Сервер добавлен!")

def show_servers():
    config = ServerConfig()
    servers = config.get_servers()
    
    if not servers:
        print("Нет сохраненных серверов")
        return
    
    print("\nСохраненные серверы:")
    for server in servers:
        print(f"- {server['name']}: {server['username']}@{server['hostname']}:{server['port']}")

def main():
    while True:
        choice = show_menu()
        
        if choice == "1":
            connect_to_server()
        elif choice == "2":
            show_servers()
        elif choice == "3":
            add_server()
        elif choice == "4":
            print("До свидания!")
            break
        else:
            print("Неверный выбор")

if __name__ == "__main__":
    main()