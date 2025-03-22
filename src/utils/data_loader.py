import tempfile
import zipfile
import os
import json
from pathlib import Path

class TemporaryFileManager:
    """Gère le chargement et la suppression automatique des fichiers temporaires."""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        self.files_index = {}
        self.loaded_files = {}

    def load_zip_to_temp(self, zip_file):
        """Extrait un fichier ZIP et indexe les fichiers JSON dans un dossier temporaire."""
        with zipfile.ZipFile(zip_file) as z:
            z.extractall(self.temp_dir)
            for root, _, files in os.walk(self.temp_dir):
                for file in files:
                    self.files_index[file] = os.path.join(root, file)
        return self.temp_dir
    
    def load_file(self, file_name):
        """Charge n'importe quel fichier temporaire en mémoire."""
        if file_name in self.files_index:
            with open(self.files_index[file_name], 'r', encoding='utf-8') as f:
                data = f.read()
                self.loaded_files[file_name] = data
                return data
        return None
    
    def load_json(self, json_name):
        """Charge un fichier JSON en mémoire si disponible."""
        if json_name in self.files_index:
            with open(self.files_index[json_name], 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.loaded_files[json_name] = data
                return data
        return None

    def unload_file(self, file_name):
        """Décharge un fichier de la mémoire si chargé."""
        if file_name in self.loaded_files:
            del self.loaded_files[file_name]

    def unload_all(self):
        """Décharge tous les fichiers de la mémoire."""
        self.loaded_files.clear()
    
    def cleanup(self):
        """Supprime tous les fichiers temporaires et vide les indices."""
        for file_path in self.files_index.values():
            os.remove(file_path)
        os.rmdir(self.temp_dir)
        self.files_index.clear()
        self.loaded_files.clear()


class InstagramMessageLoader:
    """Charge et gère les conversations Instagram à partir des fichiers JSON."""
    
    def __init__(self, file_manager: TemporaryFileManager):
        self.file_manager = file_manager

    def load_conversations(self):
        """Charge toutes les conversations trouvées dans les fichiers temporaires et les renvoie."""
        conversations = {}
        for json_name in self.file_manager.files_index.keys():
            if json_name.startswith('message_') and json_name.endswith('.json'):
                data = self.file_manager.load_json(json_name)
                if data:
                    conversations[json_name] = data
        return conversations

    def load_conversation(self, json_name):
        """Charge une conversation spécifique et la renvoie."""
        return self.file_manager.load_json(json_name)

    def unload_conversation(self, json_name):
        """Décharge une conversation de la mémoire."""
        self.file_manager.unload_file(json_name)

    def unload_all_conversations(self):
        """Décharge toutes les conversations de la mémoire."""
        self.file_manager.unload_all()
