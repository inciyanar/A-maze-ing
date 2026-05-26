from typing import Any, TextIO
import sys
import os

class ConfigParser:

    def __init__(self, config_path: str):
        self.config_path: str = config_path
        self.data: dict[str, Any] = {}  # Ayarları bir sözlükte tutacağız

    def parsing(self) -> None:
        if not os.path.exists(self.config_path):  # dosya var mı kontrolü
            raise FileNotFoundError(
                f"Hata: Yapılandırma dosyası bulunamadı: '{self.config_path}'"
            )
        file: TextIO = open(self.config_path, 'r', encoding="utf-8")  # bi dosyayı binary vs de her türlü okusun diye utf-8 diyoruz
        try:  # dosyayı okurken ayırırken vs hata alırsak diye işlemleri try bloğu içinde yapıcaz
            data: str = file.read()
            lines: list[str] = data.splitlines()
            for item in lines:
                item = item.strip()
                if not item or item[0] == '#':  # boş ya da yorum olan satırları geçiyoruz direkt
                    continue
                if "=" not in item:
                    raise ValueError(
                        f"Value Error in {self.config_path}: Invalid syntax on line -> '{item}' (Missing '=')"
    )
                splversion = item.split('=', 1)  # ilk eşittirden itibaren ayırmalıymışız bir satırda 2 eşittir varsa falan çökmemesi için
                key = splversion[0].strip()
                value = splversion[1].strip()
                self.data[key] = value
        finally:
            # Yukarıdaki (örneğin ValueError) bir hata oluşursa 
            # en son 'finally' bloğuna uğrar ve dosyayı kapatır. Subjectte uyarmış
            file.close()
            for key, value in self.data.items():
                print(f"{key}: {value}")

    def check_data(self) -> None:
        mandatory_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
        for key in mandatory_keys:
            if key not in self.data:
                raise KeyError(f"Configuration Error: Mandatory key '{key}' is missing!")  # Zorunlu key'ler datada yoksa hata fırlatıp kapattık
        validated_data: dict[str, Any] = {}  # demin str olarak depolamıştık aslında, şimdi formatlıycaz
        # formatlarken type error alırsak diye try blokları kullanıyoruz, zaten str olanları try içine almaya gerek yok
        validated_data["OUTPUT_FILE"] = self.data["OUTPUT_FILE"]  # ör: zaten str
        try:
            validated_data["WIDTH"] = int(self.data["WIDTH"])
            validated_data["HEIGHT"] = int(self.data["HEIGHT"])
        except ValueError:
            raise ValueError("Configuration Error: WIDTH and HEIGHT must be integers!")

        try:
            entry_parts = self.data["ENTRY"].split(",")
            exit_parts = self.data["EXIT"].split(",")
            validated_data["ENTRY"] = (int(entry_parts[0]), int(entry_parts[1]))
            validated_data["EXIT"] = (int(exit_parts[0]), int(exit_parts[1]))
        except (ValueError, IndexError):
            raise ValueError("Configuration Error: ENTRY and EXIT must be in 'x,y' integer format!")
            # içinde virgül yoksa da int değilse de ok bi mesaj modül 3'te de böyle yapmıştım okidir i think
        # entry ve exit maze içinde mi diye kontrol ediyorum bi de maze dim>0 mı diye
        width = validated_data["WIDTH"]
        height = validated_data["HEIGHT"]
        entry = validated_data["ENTRY"]
        maze_exit = validated_data["EXIT"]

        if width <= 0 or height <= 0:
            raise ValueError("Configuration Error: Maze dimensions must be greater than 0!")
        if not (0 <= entry[0] < width and 0 <= entry[1] < height):
            raise ValueError("Configuration Error: ENTRY coordinates are out of maze bounds!")
        if not (0 <= maze_exit[0] < width and 0 <= maze_exit[1] < height):
            raise ValueError("Configuration Error: EXIT coordinates are out of maze bounds!")
        
        # Perfect kontrolünden emin olamadım bool bir tip olması için ne 
        # yapmak lazım diye ama böyle diyince oluyo galiba
        if self.data["PERFECT"] == "True":
            validated_data["PERFECT"] = True
        elif self.data["PERFECT"] == "False":
            validated_data["PERFECT"] = False
        else:
            raise ValueError("Configuration Error: PERFECT must be bool!")
        # Eğer gelen metin "True" ise True (bool), "False" ise False (bool)
        # olur, ikisi de değilse hata fırlatır diye düşündüm ama büyük harf
        # küçük harf duyarlılığımızı bilemiyorum...
        # hatasız geldiysem self.datayı güncelleyebilirim.
        self.data = validated_data