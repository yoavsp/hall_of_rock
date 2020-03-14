from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert
from org.hall_of_rock.social.data.mappers import AppSettingMapper
from org.hall_of_rock.social.data.models import AppSettingModel
from org.hall_of_rock.social.data.repositories.interface import SettingRepository
from org.hall_of_rock.social.domain.models import AppSetting


class RDBMSettingRepository(AppSettingMapper, SettingRepository):
    model = AppSettingModel

    def __init__(self, host, port):
        engine = create_engine('postgresql://postgres:postgres@{}:{}/hall_of_rock'.format(host, port))
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def update(self, appSetting: AppSetting):
        model = self.session.query(self.model).filter(self.model.name == appSetting.name).first()
        model.value = appSetting.value
        self.session.commit()

    def save_all(self, appSettings: list):
        res = self.session.execute(insert(AppSettingModel.__table__).on_conflict_do_update(),
                             [dict(name=p.name, value=p.value)
                              for p in appSettings])
        self.session.commit()
        return res

    def get_setting_by_name(self, name:str) -> AppSetting :
        return self.modelToDto(self.session.query(AppSettingModel).filter(AppSettingModel.name == name).first())