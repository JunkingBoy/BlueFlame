'''
Author: Lucifer
Data: Do not edit
LastEditors: Lucifer
LastEditTime: 2024-07-18 01:12:35
Description: 
'''
from flask import Blueprint, request, Response
from flask_jwt_extended import jwt_required

from utils.CommonResponse import R
from service.UserService import get_user_id

bp = Blueprint("plan", __name__)

bp.route('/plan/create', methods=['POST'])
jwt_required()
def create_plan() -> Response:
    return R.ok('create plan success!')