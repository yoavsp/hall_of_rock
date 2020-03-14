from sqlalchemy import Table

from org.hall_of_rock.social.data.models import PostModel, AppSettingModel
from org.hall_of_rock.social.domain.models import Post, AppSetting


class PostMapper:
    def dtoToModel(self, post: Post) -> PostModel :
        model = PostModel()
        model.id = post.id
        model.message = post.message
        model.created_time = post.created_time
        model.full_picture = post.full_picture
        return model

    def modelToDto(self, model: PostModel) -> Post :
        return Post(model.id, model.created_time, model.message, model.full_picture)


class AppSettingMapper:
    def dtoToModel(self, appSetting: AppSetting) -> AppSettingModel :
        model = PostModel()
        model.name = appSetting.name
        model.value = appSetting.value

        return model

    def modelToDto(self, model: AppSettingModel) -> AppSetting :
        return AppSetting(model.name, model.value)
