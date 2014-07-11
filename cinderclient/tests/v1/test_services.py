# Copyright (c) 2013 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from cinderclient.tests.fixture_data import client
from cinderclient.tests.fixture_data import services as services_fixture
from cinderclient.tests import utils
from cinderclient.v1 import services


class ServicesTest(utils.FixturedTestCase):

    client_fixture_class = client.V1
    data_fixture_class = services_fixture.Fixture

    def test_list_services(self):
        svs = self.cs.services.list()
        self.assert_called('GET', '/os-services')
        self.assertEqual(len(svs), 3)
        [self.assertIsInstance(s, services.Service) for s in svs]

    def test_list_services_with_hostname(self):
        svs = self.cs.services.list(host='host2')
        self.assert_called('GET', '/os-services?host=host2')
        self.assertEqual(len(svs), 2)
        [self.assertIsInstance(s, services.Service) for s in svs]
        [self.assertEqual(s.host, 'host2') for s in svs]

    def test_list_services_with_binary(self):
        svs = self.cs.services.list(binary='cinder-volume')
        self.assert_called('GET', '/os-services?binary=cinder-volume')
        self.assertEqual(len(svs), 2)
        [self.assertIsInstance(s, services.Service) for s in svs]
        [self.assertEqual(s.binary, 'cinder-volume') for s in svs]

    def test_list_services_with_host_binary(self):
        svs = self.cs.services.list('host2', 'cinder-volume')
        self.assert_called('GET',
                           '/os-services?host=host2&binary=cinder-volume')
        self.assertEqual(len(svs), 1)
        [self.assertIsInstance(s, services.Service) for s in svs]
        [self.assertEqual(s.host, 'host2') for s in svs]
        [self.assertEqual(s.binary, 'cinder-volume') for s in svs]

    def test_services_enable(self):
        s = self.cs.services.enable('host1', 'cinder-volume')
        values = {"host": "host1", 'binary': 'cinder-volume'}
        self.assert_called('PUT', '/os-services/enable', values)
        self.assertIsInstance(s, services.Service)
        self.assertEqual(s.status, 'enabled')

    def test_services_disable(self):
        s = self.cs.services.disable('host1', 'cinder-volume')
        values = {"host": "host1", 'binary': 'cinder-volume'}
        self.assert_called('PUT', '/os-services/disable', values)
        self.assertIsInstance(s, services.Service)
        self.assertEqual(s.status, 'disabled')

    def test_services_disable_log_reason(self):
        s = self.cs.services.disable_log_reason(
            'host1', 'cinder-volume', 'disable bad host')
        values = {"host": "host1", 'binary': 'cinder-volume',
                  "disabled_reason": "disable bad host"}
        self.assert_called('PUT', '/os-services/disable-log-reason', values)
        self.assertTrue(isinstance(s, services.Service))
        self.assertEqual(s.status, 'disabled')
