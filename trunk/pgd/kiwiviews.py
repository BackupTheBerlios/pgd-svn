
import gtk


from kiwi.proxies import Proxy
from kiwi.ui.delegates import Delegate, SlaveDelegate
from kiwi.ui.views import SlaveView, BaseView

class PythonViewMixin(object):

    def __init__(self):
        # defeat class.widgets
        self.widgets = []
        self._proxied_widgets = set()

    def create_toplevel_widget(self):
        """Override to create and return the top level container."""
        return gtk.VBox()

    def add_widget(self, attribute, widget, model_attribute=None):
        """Name a widget and make it available to kiwi."""
        if model_attribute is not None:
            widget.set_property('model-attribute', model_attribute)
            self._proxied_widgets.add(attribute)
        setattr(self, attribute, widget)
        # needed to get over the class variable widgets
        self.widgets.append(attribute)
        return widget

    def attach_slaves(self):
        """Override to insert post-initialisation slave attachment."""

    def set_model(self, model):
        """Set the model and create a proxy."""
        self.python_model = model
        self.python_proxy = Proxy(self, model=model, widgets=self._proxied_widgets)


class PythonSlaveDelegate(SlaveDelegate, PythonViewMixin):
    def __init__(self, toplevel=None, **kw):
        PythonViewMixin.__init__(self)
        if toplevel is None:
            toplevel = self.create_toplevel_widget()
        SlaveDelegate.__init__(self, toplevel=toplevel, **kw)
        self.attach_slaves()
        
class PythonView(BaseView, PythonViewMixin):
    def __init__(self, toplevel=None, *args, **kw):
        PythonViewMixin.__init__(self)
        if toplevel is None:
            toplevel = self.create_toplevel_widget()
        BaseView.__init__(self, toplevel=toplevel, *args, **kw)


class PythonDelegate(Delegate, PythonViewMixin):
    def __init__(self, toplevel=None, **kw):
        PythonViewMixin.__init__(self)
        if toplevel is None:
            toplevel = self.create_toplevel_widget()
        Delegate.__init__(self, toplevel=toplevel, **kw)
        self.attach_slaves()


