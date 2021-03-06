# -*- coding:utf-8 -*-
from __future__ import absolute_import
from flask.ext import script
from flask.ext.assets import ManageAssets
from flask.ext.celery import install_commands as install_celery_commands

import commands

if __name__ == "__main__":
    from main import app_factory
    import config

    manager = script.Manager(app_factory)
    manager.add_option("-c", "--config", dest="config", required=False, default=config.Dev)
    
    manager.add_command("test", commands.Test())
    
    manager.add_command("assets", ManageAssets())
    
    manager.add_command("create_db", commands.CreateDB())
    manager.add_command("drop_db", commands.DropDB())
    
    install_celery_commands(manager)
    
    manager.run()
