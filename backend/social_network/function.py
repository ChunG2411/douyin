from social_network import settings
import os

def get_absolute_media_path(relative_path: str) -> str:
    absolute_path_to_project = str(settings.MEDIA_ROOT)
    relative_path = relative_path.replace('media/', '').replace('/', '\\')
    return os.path.join(absolute_path_to_project, relative_path)