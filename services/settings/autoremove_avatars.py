from home.models import ystu_account
from django.conf import settings
import os


def deletePhotos():
    used_photos = ystu_account.objects.all()
    listUsedPhotos = []
    media_root = settings.MEDIA_ROOT
    for i in used_photos:
        listUsedPhotos.append(str(i.avatar_image))

    for path, y, files in os.walk(media_root, 'avatars'):
        for file in files:
            file_path = os.path.join(path, file)
            relative_path = str(os.path.relpath(file_path, media_root)).replace('\\', "/")
            # print(relative_path)
            # print(listUsedPhotos[1])
            # print(relative_path in listUsedPhotos)
            if relative_path not in listUsedPhotos:
                os.remove(file_path)
                #print('del')

