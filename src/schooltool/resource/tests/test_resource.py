#
# SchoolTool - common information systems platform for school administration
# Copyright (c) 2005 Shuttleworth Foundation
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
Unit tests for resources
"""
import unittest
import doctest

from zope.interface.verify import verifyObject

from schooltool.testing.util import run_unit_tests


def doctest_ResourceContainer():
    """Tests for ResourceContainer

        >>> from schooltool.resource.interfaces import IResourceContainer
        >>> from schooltool.resource.resource import ResourceContainer
        >>> c = ResourceContainer()
        >>> verifyObject(IResourceContainer, c)
        True

    Let's make sure it acts like a proper container should act

        >>> from zope.container.tests.test_btree import TestBTreeContainer
        >>> class Test(TestBTreeContainer):
        ...    def makeTestObject(self):
        ...        return ResourceContainer()
        >>> run_unit_tests(Test)
    """


def doctest_Resource():
    r"""Tests for Resource

        >>> from schooltool.resource.interfaces import IResource
        >>> from schooltool.resource.resource import Resource
        >>> resource = Resource()
        >>> verifyObject(IResource, resource)
        True

    Resources can have titles and descriptions too

        >>> blender = Resource(title='Blender', description="It's broken.")
        >>> blender.title
        'Blender'
        >>> blender.description
        "It's broken."

        >>> blender.notes
        u''

    """


def doctest_Location():
    r"""Test for Location

        >>> from schooltool.resource.interfaces import ILocation
        >>> from schooltool.resource.resource import Location
        >>> room = Location()
        >>> verifyObject(ILocation, room)
        True

    Locations have several standard peices of information associated with
    them:

        >>> room.capacity

    """


def doctest_Equipment():
    r"""Test for Equipment

        >>> from schooltool.resource.interfaces import IEquipment
        >>> from schooltool.resource.resource import Equipment
        >>> projector = Equipment()
        >>> verifyObject(IEquipment, projector)
        True

    In addition to standard attributes, equipment also has the following
    attributes:

        >>> projector.manufacturer
        u''
        >>> projector.model
        u''
        >>> projector.serialNumber
        u''
        >>> projector.purchaseDate
    """


def doctest_ResourceDemographics():
    r"""Test Resource Demographics objects and adapters

        >>> from schooltool.resource import interfaces, resource

    First we need to set up a mock app and register its adapter:

        >>> from zope.component import provideAdapter
        >>> from zope.interface import implements
        >>> from schooltool.app.interfaces import ISchoolToolApplication

        >>> class MockSchoolToolApplication(dict):
        ...     implements(ISchoolToolApplication)
        >>> app = MockSchoolToolApplication()
        >>> provideAdapter(lambda context: app, (None,), ISchoolToolApplication)

    We need to do what the AppInit adapter would otherwise do:

        >>> resource.ResourceInit(app)()
        >>> resource.RESOURCE_DEMO_FIELDS_KEY in app
        True
        >>> resource.RESOURCE_DEMO_DATA_KEY in app
        True

    There's an adapter for the resource demo fields container:

        >>> provideAdapter(resource.getDemographicsFields)
        >>> dfs = interfaces.IDemographicsFields(app)
        >>> interfaces.IDemographicsFields.providedBy(dfs)
        True
        >>> len(dfs)
        0

    We'll add some demo fields to the container, some that are limited to a
    specific resource type or types:

        >>> dfs['ID'] = resource.TextFieldDescription("ID", "Identifier")
        >>> dfs['square_feet'] = resource.TextFieldDescription("square_feet",
        ...     "Square Feet", limit_resource_types=['location'])
        >>> dfs['warranty'] = resource.TextFieldDescription("warranty",
        ...     "Warranty", limit_resource_types=['equiptment'])
        >>> dfs['creation_date'] = resource.DateFieldDescription(
        ...      "creation_date", "Creation Date",
        ...      limit_resource_types=['location', 'equiptment'])

    When we pass the filter_resource_type method a resource_type that does not
    belong  to any of the limit_resource_types lists, then it will only return
    those fields that have empty limit_resource_types lists.

        >>> [f.__name__ for f in dfs.filter_resource_type('anything')]
        [u'ID']

    When we pass 'location', it picks up the additional fields that are for
    location type resources.

        >>> [f.__name__ for f in dfs.filter_resource_type('location')]
        [u'ID', u'square_feet', u'creation_date']

    When we pass 'equiptment', it picks up the additional fields that are for
    equiptment type resources.

        >>> [f.__name__ for f in dfs.filter_resource_type('equiptment')]
        [u'ID', u'warranty', u'creation_date']

    Finally there's an adapter that adapts a resource it's demo data:

        >>> provideAdapter(resource.getResourceDemographics)

    Now we will create a resource and see what we get when we adapt it to
    IDemographics:

        >>> sample = resource.Resource('Sample Resource')
        >>> sample.__name__ = 'sample'
        >>> demos = interfaces.IDemographics(sample)
        >>> interfaces.IDemographics.providedBy(demos)
        True
        >>> len(demos)
        0
    """

def test_suite():
    return unittest.TestSuite([
                doctest.DocTestSuite(optionflags=doctest.ELLIPSIS),
           ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
