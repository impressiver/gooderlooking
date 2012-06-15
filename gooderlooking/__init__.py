from main import app_factory
import config

# uWSGI callable entrypoint
app = app_factory(config.Dev)