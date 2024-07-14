import os
import json
import shutil

class FS:
    def __init__(self) -> None:
        self.root = os.path.abspath(os.curdir)
        self.data = os.path.join(self.root, 'data')
        self.datain = os.path.join(self.data, 'in')
        self.dataout = os.path.join(self.data, 'out')
        self.names = os.path.join(self.data, 'names')
        self.excels = os.path.join(self.names, 'excels')
        self.config = self.get_config()
        pass

    def get_config(self) -> dict:
        with open(os.path.join(self.data, 'config.json'), 'r') as f:
            return json.load(f)
    
    def get_field(self, path) -> str|int|bool:
        target = self.config
        for key in path:
            if key not in target:
                return None
            target = target[key]
        return target

    def set_config(self, path, value) -> None:
        target = self.config
        
        for key in path[:-1]:
            if key not in target:
                target[key] = {}
            target = target[key]

        target[path[-1]] = value
    
    def write_config(self, config) -> bool:
        with open(os.path.join(self.data, 'config.json'), 'w') as f:
            try:
                json.dump(config, f, indent=4)
                return True
            except:
                return False
    
    def read_parser_json(self, path) -> dict:
        with open(os.path.join(self.names, f"{path}.json"), 'r') as f:
            return json.load(f)

    def read_folder(self, path:str|list) -> list:
        if isinstance(path, list):
            path = os.path.join(*path)
        return os.listdir(path)

    def make_base(self, path:list) -> bool:
        try:
            os.makedirs(os.path.join(*path))
            return True
        except:
            return False
    
    def in_rm(self, path:str) -> bool:
        try:
            shutil.rmtree(os.path.join(self.datain, path), ignore_errors=True)
            return True
        except:
            return False
        

    def out_mkdir(self, path) -> bool:
        print(f"[i] Making {path}")
        try:
            os.makedirs(os.path.join(self.dataout, path), exist_ok=True)
            return True
        except:
            print(f"[!] Failed to make {path}")
            return False
    

    def out_move(self, src, dst) -> bool:
        # print(f"[i] Moving {src} to {dst}")
        try:
            shutil.move(src, os.path.join(self.dataout, dst))
            return True
        except:
            print(f"[!] Failed to move {src} to {dst}")
            return False