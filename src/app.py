# -*- coding: utf-8 -*-

import os
from flask import  Flask

from router import register_router

import logging

logger = logging.getLogger(__name__)

UPLOAD_FOLDER = 'static/uploads/'

def create_app():
    flask_app = Flask(__name__,)
    flask_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if not os.path.exists(UPLOAD_FOLDER):
        logger.info('Creating upload folder %s', UPLOAD_FOLDER)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    flask_app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    flask_app.config['SECRET_KEY'] ='secret key'
    register_router(flask_app)
    return flask_app


app = create_app()

if __name__ == '__main__':
	
    app.run(host="0.0.0.0", port=9999, debug=False)