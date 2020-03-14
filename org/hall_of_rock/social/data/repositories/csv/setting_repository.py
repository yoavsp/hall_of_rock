import csv
import os
import shutil
from itertools import chain
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert
from org.hall_of_rock.social.data.mappers import AppSettingMapper
from org.hall_of_rock.social.data.models import AppSettingModel
from org.hall_of_rock.social.data.repositories.csv.file_based_table import FileBasedTable
from org.hall_of_rock.social.data.repositories.interface import SettingRepository
from org.hall_of_rock.social.domain.models import AppSetting


class CSVSettingRepository(SettingRepository, FileBasedTable):
    model = AppSettingModel

    def __init__(self, path: str):
        assert os.path.exists(path)
        self.create_backup(path)
        shutil.copyfile(path, "/".join(path.split("/")))
        self.path = path
        with open(path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            self.settings = [AppSetting(r['name'], r['value']) for r in csv_reader]

    def commit(self):
        self.save_all(self.settings)

    def update(self, appSetting: AppSetting):
        model = [r for r in self.settings if r.name == appSetting.name]
        if len(model):
            model = model[0]
            idx = self.settings.index(model)
            self.settings[idx] = appSetting
            self.commit()

    def save_all(self, app_settings: list):
        if len(app_settings) > 0:
            app_settings_dicts = [p.__dict__ for p in app_settings]
            with open(self.path, 'w')as file:
                writer = csv.DictWriter(file, set(chain.from_iterable([p.keys() for p in app_settings_dicts])))
                writer.writeheader()
                writer.writerows(app_settings_dicts)

    def get_setting_by_name(self, name:str) -> Optional[AppSetting]:
        model = [r for r in self.settings if r.name == name]
        if len(model):
            return model[0]
        return None