def wsgi(self):
    from .app import app
    return app
