import asyncio
from typing import Final
from flask import Blueprint, request, redirect, flash, session, render_template
from ..common.odoo_api import ServiceAPI
from ..common.messages import Categories, ServicePackMessage
from .users_bp import login_required

MAXIMUM_IMAGE_FACE: Final[int] = 4

services = Blueprint('services', __name__, url_prefix='/services')


@services.route('/register', methods=['POST'])
@login_required
def register_service():
    service_quantity = int(request.form.get('service_quantity'))
    service_id = int(request.form.get('service_id'))
    if not service_quantity:
        flash(ServicePackMessage.ServiceQuantityRequired.value, Categories.Error.value)
        return redirect('/')
    elif not service_id:
        flash(ServicePackMessage.ServiceIdRequired.value, Categories.Error.value)
        return redirect('/')
    elif 'face_image[]' not in request.files:
        flash(ServicePackMessage.FileImageFacesRequired.value, Categories.Error.value)
        return redirect('/')
    elif len(request.files.getlist('face_image[]')) > MAXIMUM_IMAGE_FACE:
        flash(ServicePackMessage.Maximum3ImagesFace.value, Categories.Error.value)
        return redirect('/')
    elif 'license_plate_image[]' not in request.files:
        flash(ServicePackMessage.FileImageLicensePlateRequired.value, Categories.Error.value)
        return redirect('/')
    elif len(request.files.getlist('license_plate_image[]')) != service_quantity:
        flash(ServicePackMessage.QuantityImageNotMatchQuantityPack.value.format(service_quantity, service_quantity),
              Categories.Error.value)
        return redirect('/')
    face_data = [{
        'face_binary': file.read(),
        'face_name': file.filename.split('.')[0].capitalize()
    } for file in request.files.getlist('face_image[]')]
    image_license_plate_bytes = [file.read() for file in request.files.getlist('license_plate_image[]')]
    asyncio.run(ServiceAPI.register_service(uid=session['user']['__uid'],
                                            quantity=service_quantity,
                                            service_id=service_id,
                                            image_face_bytes=face_data,
                                            image_license_plate_bytes=image_license_plate_bytes))
    return redirect('/users/profile')
