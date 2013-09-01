'''
Transform View
==============

.. versionadded:: 1.8

.. warning::

    This code is still experimental, and its API is subject to change in a
    future version.

The :class:`~kivy.uix.listview.TransformView` widget provides a
scrollable/pannable viewport that is clipped at the scrollview's bounding box,
which contains a single item view instance.

:class:`~kivy.uix.listview.TransformView` implements :class:`AbstractView` as a
vertical scrollable list. :class:`AbstractView` has one property, adapter.
:class:`~kivy.uix.listview.TransformView` sets adapter to
:class:`~kivy.adapters.transformadapter.TransformAdapter`, or a subclass.

'''

__all__ = ('TransformView', )

from kivy.adapters.args_converters import list_item_args_converter
from kivy.adapters.transformadapter import TransformAdapter
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.lang import Builder

from kivy.properties import ObjectProperty

from kivy.uix.abstractview import AbstractView
from kivy.uix.listview import ListItemLabel


Builder.load_string('''
<TransformView>:
    container: container
    scrollview: scrollview
    ScrollView:
        id: scrollview
        pos: root.pos
        GridLayout:
            id: container
            cols: 1
            size_hint_y: None
''')


class TransformView(AbstractView, EventDispatcher):
    ''':class:`~kivy.uix.listview.TransformView` is a primary high-level
    widget, handling the common task of presenting an item in a scrolling list.

    The adapter property comes via the mixed in
    :class:`~kivy.uix.abstractview.AbstractView` class.

    .. versionadded:: 1.8

    '''

    container = ObjectProperty(None)
    '''The container is a :class:`~kivy.uix.gridlayout.GridLayout` widget held
    within a :class:`~kivy.uix.scrollview.ScrollView` widget.  (See the
    associated kv block in the Builder.load_string() setup). The item view
    instance is managed and provided by the adapter.  The container is cleared
    with a call to clear_widgets() when the data view is rebuilt by the
    populate() method.

    :data:`container` is an :class:`~kivy.properties.ObjectProperty`,
    default to None.
    '''

    def __init__(self, **kwargs):

        if 'adapter' not in kwargs:

            if 'data' not in kwargs:
                raise Exception(('TransformView: without adapter, '
                                 'must provide data arg.'))

            cls = kwargs.pop('cls', ListItemLabel)
            args_converter = \
                    kwargs.pop('args_converter', list_item_args_converter)

            adapter = TransformAdapter(args_converter=args_converter,
                                           cls=cls,
                                           data=kwargs['data'])

            kwargs['adapter'] = adapter

        super(TransformView, self).__init__(**kwargs)

        if self.adapter:
            self.adapter.bind(on_data_change=self.data_changed)

        self._trigger_populate = Clock.create_trigger(self._spopulate, -1)
        self._trigger_reset_spopulate = \
            Clock.create_trigger(self._reset_spopulate, -1)

        self.container.bind(minimum_height=self.container.setter('height'))

        self.bind(size=self._trigger_populate,
                  pos=self._trigger_populate,
                  adapter=self.adapter_changed)

    def adapter_changed(self, *args):

        if self.adapter:
            self.adapter.bind(on_data_change=self.data_changed)

            self._trigger_populate()

    def _spopulate(self, *args):
        self.populate()

    def _reset_spopulate(self, *args):
        self.populate()

    def populate(self):

        container = self.container

        # Clear the view.
        container.clear_widgets()

        item_view = self.adapter.get_view(0)
        container.add_widget(item_view)

    def data_changed(self, *args):
        self.populate()

    def get_selection(self):
        '''A convenience method to call to the adapter for the all of the
        selected items.

        .. versionadded:: 1.8

        '''
        return self.adapter.get_selection() if self.adapter else None

    def get_first_selected(self):
        '''A convenience method to call to the adapter for the first selected
        item.

        .. versionadded:: 1.8

        '''
        return self.adapter.get_first_selected() if self.adapter else None

    def get_last_selected(self):
        '''A convenience method to call to the adapter for the last selected
        item.

        .. versionadded:: 1.8

        '''
        return self.adapter.get_last_selected() if self.adapter else None
