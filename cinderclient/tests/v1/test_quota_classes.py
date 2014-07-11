# Copyright (c) 2011 OpenStack Foundation
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
from cinderclient.tests.fixture_data import quota_classes
from cinderclient.tests import utils


class QuotaSetsTest(utils.FixturedTestCase):

    client_fixture_class = client.V1
    data_fixture_class = quota_classes.Fixture

    def test_class_quotas_get(self):
        class_name = 'test'
        self.cs.quota_classes.get(class_name)
        self.assert_called('GET', '/os-quota-class-sets/%s' % class_name)

    def test_update_quota(self):
        q = self.cs.quota_classes.get('test')
        q.update(volumes=2, snapshots=2)
        self.assert_called('PUT', '/os-quota-class-sets/test')

    def test_refresh_quota(self):
        q = self.cs.quota_classes.get('test')
        q2 = self.cs.quota_classes.get('test')
        self.assertEqual(q.volumes, q2.volumes)
        q2.volumes = 0
        self.assertNotEqual(q.volumes, q2.volumes)
        q2.get()
        self.assertEqual(q.volumes, q2.volumes)
