import pickle

import requests
import logging
import aiohttp
from typing import Dict, Any, Optional, List
from markupsafe import Markup
from os import environ

_logger = logging.getLogger(__name__)


class OdooAPI:
    ODOO_SERVER_DOMAIN = environ.get('ODOO_SERVER_DOMAIN')

    @staticmethod
    async def make_request(url: str, method: str, data: Optional[Dict[str, Any]] = None, **kwargs):
        try:
            async with aiohttp.ClientSession() as session:
                if method == 'GET':
                    async with session.get(url=url, **kwargs) as response:
                        return await response.json()
                else:
                    async with session.post(url=url, data=data, **kwargs) as response:
                        return await response.json()
        except Exception as e:
            _logger.exception(e)

    @staticmethod
    def check_response(response):
        if response:
            if response.get('status') and response.get('status') == 200:
                return response.get('data')
            return response.get('result')
        return None


class ServiceAPI:

    @staticmethod
    async def register_service(uid: int, quantity: int, service_id: int, image_face_bytes: (bytes, bytearray),
                               image_license_plate_bytes: (bytes, bytearray)):
        try:
            url = '{}/odoo-api/spp/service/register?uid={}&quantity={}&service_id={}'.format(
                OdooAPI.ODOO_SERVER_DOMAIN, uid, quantity, service_id
            )
            bufferer_image = pickle.dumps(dict(image_face_bytes=image_face_bytes,
                                               image_license_plate_bytes=image_license_plate_bytes))
            response = await OdooAPI.make_request(url=url, method='POST', data=bufferer_image,
                                                  headers={'Content-type': 'application/octet-stream'})
            return OdooAPI.check_response(response)
        except Exception as e:
            _logger.exception(e)


class IndexAPI:

    @staticmethod
    async def info() -> Optional[Dict[str, Dict[str, Any]]]:
        try:
            url = f'{OdooAPI.ODOO_SERVER_DOMAIN}/odoo-api/spp/index/info'
            response = await OdooAPI.make_request(url=url, method='GET')
            return OdooAPI.check_response(response)
        except Exception as e:
            _logger.exception(e)


class UserAPI:

    @staticmethod
    async def sign_in(email: str, password: str):
        try:
            url = f'{OdooAPI.ODOO_SERVER_DOMAIN}/web/session/authenticate'
            data = dict(params=dict(db='odoo-16-spp-dev-2023-09-07', login=email, password=password))
            response = await OdooAPI.make_request(url=url, method='GET', json=data)
            return OdooAPI.check_response(response)
        except Exception as e:
            _logger.exception(e)

    @staticmethod
    async def sign_out():
        try:
            url = f'{OdooAPI.ODOO_SERVER_DOMAIN}/odoo-api/spp/user/sign_out'
            response = await OdooAPI.make_request(url=url, method='POST')
            return OdooAPI.check_response(response)
        except Exception as e:
            _logger.exception(e)

    @staticmethod
    async def sign_up(login: str, password: str, fullname: str):
        try:
            url = f'{OdooAPI.ODOO_SERVER_DOMAIN}/odoo-api/spp/user/sign_up'
            data = dict(login=login, password=password, name=fullname)
            response = await OdooAPI.make_request(url=url, method='POST', json=data)
            return OdooAPI.check_response(response)
        except Exception as e:
            _logger.exception(e)

    @staticmethod
    async def profile(uid):
        try:
            url = f'{OdooAPI.ODOO_SERVER_DOMAIN}/odoo-api/spp/user/profile?uid={uid}'
            response = await OdooAPI.make_request(url=url, method='POST')
            return OdooAPI.check_response(response)
        except Exception as e:
            _logger.exception(e)


class Address:

    @staticmethod
    def get_provinces():
        try:
            response = requests.get(url=f'{OdooAPI.ODOO_SERVER_DOMAIN}/odoo-api/spp/get-provinces')
            data = response.json().get('data')
            return data
        except Exception as e:
            _logger.exception(e)