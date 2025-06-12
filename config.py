import os

class Config:
    DEBUG = os.environ.get('FLASK_DEBUG', default=True)
    SECRET_KEY = os.environ.get('SECRET_KEY', default='supersecretkey')
    HUGGINGFACEHUB_API_TOKEN = os.environ.get('HUGGINGFACEHUB_API_TOKEN', default='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')
