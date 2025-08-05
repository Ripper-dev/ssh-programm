import json
import os
from typing import List, Dict

class ServerConfig:
    def __init__(self):
        self.config_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'sshlite')
        self.config_file = os.path.join(self.config_dir, 'servers.json')
        os.makedirs(self.config_dir, exist_ok=True)
        self.servers = self.load_config()
    
    def load_config(self) -> List[Dict]:
        """Загрузка конфигурации серверов"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_config(self):
        """Сохранение конфигурации"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.servers, f, indent=2, ensure_ascii=False)
    
    def add_server(self, name: str, hostname: str, username: str, 
                   password: str = None, key_path: str = None, port: int = 22):
        """Добавление сервера в конфигурацию"""
        server = {
            "name": name,
            "hostname": hostname,
            "username": username,
            "port": port
        }
        if password:
            server["password"] = password
        if key_path:
            server["key_path"] = key_path
        
        self.servers.append(server)
        self.save_config()
    
    def get_servers(self) -> List[Dict]:
        """Получение списка серверов"""
        return self.servers