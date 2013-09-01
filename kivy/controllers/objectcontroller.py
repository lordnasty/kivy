'''
ObjectController
----------------

The ObjectController class holds a single Controller in the data property. This
Controller can be anything, including a collection.

The default update() method for setting data will set any single Controllers to
data, and will set the first item of a list to data.

Methods in an Controller controller can transform the data item in various ways
to build an API for it.

.. versionadded:: 1.8

'''
import collections

from kivy.controllers.controller import Controller
from kivy.controllers.utils import parse_binding
from kivy.controllers.utils import bind_binding

__all__ = ('ObjectController', )


class ObjectController(Controller):
    '''
    data, which is defined as an ObjectProperty in the Controller superclass,
    can be any Controller, including a list, a dict, etc. transform is a
    TransformProperty, which by default will operated on a sibling property
    called data.  The transform TransformProperty has a default func as a
    lambda that simply sets the item, with no transform applied. Set
    transform.func if a transform should be applied.
    '''
    # data is an ObjectProperty, defined in Controller

    def __init__(self, **kwargs):

        data_binding, kwargs = parse_binding('data', kwargs)

        super(ObjectController, self).__init__(**kwargs)

        if data_binding:
            bind_binding(self, data_binding)

    def update_subject_from_first_item(self, *args):
        # Set data as the first item.
        d = args[1]
        if isinstance(d, collections.Iterable):
            if d:
                self.subject = d[0]

    def update_data_from_first_item(self, *args):
        # Set data as the first item.
        d = args[1]
        if isinstance(d, collections.Iterable):
            if d:
                self.data = d[0]
