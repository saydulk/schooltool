#
# SchoolTool - common information systems platform for school administration
# Copyright (c) 2009 Shuttleworth Foundation
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
"""
Unit tests for common widgets.
"""
import unittest

import zope.component
import zope.interface
from zope.testing import doctest
from zope.interface.verify import verifyObject
from zope.publisher.browser import TestRequest

import z3c.form.interfaces
from z3c import form

from schooltool.schoolyear.ftesting import schoolyear_functional_layer
import schooltool.skin.widgets
from schooltool import skin
from schooltool.app.browser.testing import setUp, tearDown


def setUpAppAbsoluteURL():
    from schooltool.app.interfaces import ISchoolToolApplication
    from zope.traversing.browser.interfaces import IAbsoluteURL
    from zope.publisher.interfaces.http import IHTTPRequest
    class App(object):
        pass
    zope.component.provideAdapter(
        lambda ignored: App(),
        adapts=(None, ), provides=ISchoolToolApplication)
    zope.component.provideAdapter(
        lambda app, request: lambda: request.getApplicationURL(),
        adapts=(App, IHTTPRequest), provides=IAbsoluteURL)


class FormRequest(TestRequest):
    zope.interface.implements(
        form.interfaces.IFormLayer,
        skin.skin.ISchoolToolLayer,
        )


def doctest_HTMLFragmentWidget():
    """Tests for HTMLFragmentWidget.

        >>> widget = skin.widgets.HTMLFragmentWidget()
        >>> verifyObject(skin.widgets.IHTMLFragmentWidget, widget)
        True

    """


def doctest_FckeditorWidget_FCKConfig():
    """Tests for FckeditorWidget and FCKConfig.

        >>> setUpAppAbsoluteURL()

    We'll need a field first.

        >>> from zope.html.field import HtmlFragment
        >>> schema_field = HtmlFragment(__name__='html', title=u"Fragment")

    Let's build a widget bound to the field.

        >>> zope.component.provideAdapter(skin.widgets.FckeditorFieldWidget)

        >>> request = FormRequest()
        >>> widget = zope.component.getMultiAdapter(
        ...     (schema_field, request), form.interfaces.IFieldWidget)

        >>> print widget
        <FckeditorWidget 'html'>

        >>> verifyObject(skin.widgets.IFckeditorWidget, widget)
        True

    Widget initially has no config set, so it cannot render the FCK editor
    javascript setup.

        >>> print widget.config
        None

        >>> widget.script
        Traceback (most recent call last):
        ...
        TypeError: ('Could not adapt', None, <...IFCKConfig>)

    Config will be set during widget update, as a computed widget value.

        >>> zope.component.provideAdapter(
        ...     skin.widgets.Fckeditor_config, name='config')

        >>> value = zope.component.getMultiAdapter(
        ...     (widget.context, widget.request,
        ...      widget.form, widget.field, widget),
        ...     form.interfaces.IValue, name='config')

        >>> print value
        <ComputedValue <schooltool.skin.widgets.FCKConfig object at ...>>

        >>> verifyObject(skin.widgets.IFCKConfig, value.get())
        True

        >>> widget.update()

        >>> print widget.config
        <schooltool.skin.widgets.FCKConfig object at ...>

    Now we can render the javascript.

        >>> print widget.script
        <script type="text/javascript" language="JavaScript">
            var oFCKeditor... = new FCKeditor(
                "html", 430, 300, "schooltool");
            oFCKeditor...BasePath = "/@@/fckeditor/";
            oFCKeditor...Config["CustomConfigurationsPath"] =
                "http://127.0.0.1/@@/editor_config.js";
            oFCKeditor....ReplaceTextarea();
        </script>

    Let's set the widget value.

        >>> widget.update()

        >>> widget.value
        u''

        >>> request = FormRequest(
        ...     form={widget.name: '<strong>All hail hypnotoad!</strong>'})

        >>> widget = zope.component.getMultiAdapter(
        ...     (schema_field, request), form.interfaces.IFieldWidget)

        >>> widget.update()
        >>> print widget.value
        <strong>All hail hypnotoad!</strong>

    We also have a different configuration for add and edit forms.

        >>> zope.component.provideAdapter(
        ...     skin.widgets.Fckeditor_addform_config, name='config')
        >>> zope.component.provideAdapter(
        ...     skin.widgets.Fckeditor_editform_config, name='config')

        >>> widget.form = form.form.AddForm(None, request)
        >>> widget.update()
        >>> print widget.config
        <schooltool.skin.widgets.EditFormFCKConfig object at ...>

        >>> verifyObject(skin.widgets.IFCKConfig, widget.config)
        True

        >>> widget.form = form.form.EditForm(None, request)
        >>> widget.update()
        >>> print widget.config
        <schooltool.skin.widgets.EditFormFCKConfig object at ...>

    """


def test_suite():
    optionflags = (doctest.NORMALIZE_WHITESPACE |
                   doctest.ELLIPSIS |
                   doctest.REPORT_ONLY_FIRST_FAILURE)
    suite = doctest.DocTestSuite(optionflags=optionflags,
                                 setUp=setUp, tearDown=tearDown)
    suite.layer = schoolyear_functional_layer
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
