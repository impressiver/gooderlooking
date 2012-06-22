from flask import Flask, current_app
from flask.ext.assets import Environment, Bundle
from webassets.version import Version, has_placeholder, VersionIndeterminableError


environment = Environment()


def register_bundles(config):
    for key, scripts in config['ASSETS_SCRIPTS'].iteritems():
        bundle = Bundle(*scripts, filters='jsmin, gzip', output='min/scripts/' + key + '.%(version)s.js')
        environment.register(key + '.js', bundle)
    
    for key, styles in config['ASSETS_STYLES'].iteritems():
        bundle = Bundle(*styles, filters='datauri, cssmin', output='min/styles/' + key + '.%(version)s.css')
        environment.register(key + '.css', bundle)
        
class BuildVersion(Version):
    """Uses the MD5 hash of the content as the version.

    By default, only the first 8 characters of the hash are used, which
    should be sufficient. This can be changed by passing the appropriate
    ``length`` value to ``__init__`` (or ``None`` to use the full hash).

    You can also customize the hash used by passing the ``hash`` argument.
    All constructors from ``hashlib`` are supported.
    """

    id = 'build'

    @classmethod
    def make(cls, length=None):
        args = [int(length)] if length else []
        return cls(*args)

    def determine_version(self, bundle, env, hunk=None):
        if not hunk:
            if not has_placeholder(bundle.output):
                raise VersionIndeterminableError(
                    'output target does not have a %(version)s placeholder')
                    
        return str(current_app.config['BUILD'])