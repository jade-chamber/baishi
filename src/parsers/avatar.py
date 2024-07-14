import os

class Avatar:
    def __init__(self, fs) -> None:
        self.fs = fs
        self.avatar_names = self.fs.read_parser_json("avatars")
        self.costume_names = self.fs.read_parser_json("costumes")
        self._parse_in()
        pass

    def _parse_in(self) -> bool:
        all_files = self.fs.read_folder([self.fs.datain, "GameObject"])
        avatar_files = [x for x in all_files if x.split("_")[0] == "Avatar"]
        for avatar in avatar_files:
            if self.fs.get_field(['parsing', 'use_excels']) == True:
                pass
            else:
                parsed = self.json_parse(avatar)
                if not parsed:
                    print(f"[!] Failed to parse {avatar}")
                    continue

                self._act_upon(parsed)
        pass

    def _act_upon(self, info) -> bool:
        match info['action']:
            case "delete":
                print(f"[i] Deleting {info['file_name']}")
                self.fs.in_rm(f"GameObject/{info['file_name']}")
            case "move":
                print(f"[i] Moving {info['name']}")
                
                # First make folder
                folder = os.path.join(*info['base'], info['name'], *info['inside'])
                self.fs.out_mkdir(folder)

                # Then move the files
                src = os.path.join(self.fs.datain, "GameObject", f"{info['file_name']}")
                for file in self.fs.read_folder(src):
                    self.fs.out_move(os.path.join(src, file), folder)
                
                # Clean up
                self.fs.in_rm(f"GameObject/{info['file_name']}")
            
            case "name_error":
                print(f"[!] {info['name']} does not exist in json")
                pass

            case "name_malformed":
                print(f"[!] {info['name']} is not a valid name")
                pass

            case _:
                print(f"[!] Unknown action {info['action']}")
                return False

    def json_parse(self, name) -> dict:
        avatar = name.split('_')
        if len(avatar) < 3:
            return {
                "action": "name_malformed",
                "file_name": "_".join(avatar),
                "name": " ".join(avatar)
            }
        if any(x in avatar for x in ['Edit', 'Manekin', 'Remote']):
            return {
                "action": "delete",
                "file_name": "_".join(avatar)
            }
        
        avatar_name = avatar[3].split("Costume")[0]

        if avatar_name not in self.avatar_names:
                return {
                    "action": "name_error",
                    "file_name": "_".join(avatar),
                    "name": avatar[3]
                }
        
        if "Costume" in avatar[3]:
            costume_name = avatar[3].split("Costume")[1]
            if costume_name not in self.costume_names[avatar_name]:
                return {
                    "action": "name_error",
                    "file_name": "_".join(avatar),
                    "name": costume_name
                }
            return {
                "action": "move",
                "file_name": "_".join(avatar),
                "base": ["Character", "Playable"],
                "name": self.avatar_names[avatar_name]['name'],
                "inside": ["Model", self.costume_names[avatar_name][costume_name]['name']]
            }
        else:
            return {
                "action": "move",
                "file_name": "_".join(avatar),
                "base": ["Character", "Playable"],
                "name": self.avatar_names[avatar[3]]['name'],
                "inside": ["Model", "Default"]
            }
        