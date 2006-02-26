

from kiwiviews import PythonSlaveDelegate

class PGDSlaveDelegate(PythonSlaveDelegate):

    def __init__(self, app):
        self.app = app
        self.main_window = app.main_window
        super(PGDSlaveDelegate, self).__init__()

    def get_session_manager(self):
        try:
            return self.app.session_manager
        except:
            return

    session_manager = property(get_session_manager)

    def update_state(self, state):
        pass

