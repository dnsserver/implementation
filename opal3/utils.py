from werkzeug.utils import find_modules, import_string
from flask import _app_ctx_stack as stack


def register_blueprints(app):
    """
    Register all blueprint modules
    Reference: Armin Ronacher, "Flask for Fun and for Profit" PyBay 2016.
    """
    for name in find_modules('opal3.blueprints'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)
    return None


def register_teardowns(app):
    @app.teardown_appcontext
    def close_db(error):
        """Closes the blueprints again at the end of the request."""
        print("teardown called.")
        ctx = stack.top
        if ctx is not None:
            if hasattr(ctx, 'sqlite3_opal'):
                ctx.sqlite3_opal.close()
