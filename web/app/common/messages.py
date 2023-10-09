from typing import Final
from enum import Enum


class Categories(Enum):
    Error: Final[str] = 'error'
    Success: Final[str] = 'success'
    Warning: Final[str] = 'warning'


class UserMessage(Enum):
    LoginRequired: Final[str] = 'You need to login first'
    EmailRequired: Final[str] = 'The email field is required'
    PasswordRequired: Final[str] = 'The password field is required'
    FullnameRequired: Final[str] = 'The fullname field is required'
    LoginFailed: Final[str] = 'Sign in failed. Email or Password wrong'
    LoginSuccess: Final[str] = 'Sign in successfully'


class LicensePlateMessage(Enum):
    RecognizeFailed: Final[str] = 'OCR failed. D\'ont recognize license plate'
    LocalCodeInvalid: Final[str] = 'OCR failed. Local code invalid'
    CharacterSeriesInvalid: Final[str] = 'OCR failed. Registration character series invalid'
    LengthRegistrationInvalid: Final[str] = 'OCR failed. Length registration number invalid'
    RegistrationNumberInvalid: Final[str] = 'OCR failed. Registration number invalid'


class ServicePackMessage(Enum):
    ServiceQuantityRequired: Final[str] = 'The service quantity field is required'
    ServiceIdRequired: Final[str] = 'The service id field is required'
    FileImageFacesRequired: Final[str] = 'The image face field is required'
    FileImageLicensePlateRequired: Final[str] = 'The license plate field is required'
    Maximum3ImagesFace: Final[str] = 'Only allowed to upload a maximum of 3 face images'
    QuantityImageNotMatchQuantityPack: Final[str] = 'Package only applies to {} slots equivalent to {} license plate images'
