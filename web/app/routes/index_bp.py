import asyncio
from flask import Blueprint, render_template, current_app
from flask_caching import Cache
from ..common.odoo_api import IndexAPI

index = Blueprint('index', __name__)
cache = Cache(current_app)


@cache.cached()
def get_info():
    return asyncio.run(IndexAPI.info())


@index.route('/')
def home():
    info = get_info()
    return render_template('index.html', info=info)

