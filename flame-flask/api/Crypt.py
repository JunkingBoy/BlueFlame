from flask import Blueprint, Response, jsonify
from typing import Dict, Any

from utils.CryptUtils import set_aes_key

import base64
import os

crypt: object = Blueprint('crypt', __name__)

@crypt.route('/getAESKey', methods=['GET'])
def getAES() -> Response:
    key: bytes = os.urandom(32)
    set_aes_key(key=key)
    
    return jsonify({
        'aes_key': base64.b64encode(key).decode('utf-8')
    })
