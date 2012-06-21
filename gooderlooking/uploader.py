from flaskext.uploads import (UploadSet, configure_uploads, patch_request_class, IMAGES)

photos = UploadSet('photos', IMAGES)

def init_app(app):
    configure_uploads(app, photos)
    patch_request_class(app, 32 * 1024 * 1024)  # 32 megabytes