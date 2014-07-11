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
from cinderclient.tests.fixture_data import quotas
from cinderclient.tests import utils


class QuotaSetsTest(utils.FixturedTestCase):

    client_fixture_class = client.V1
    data_fixture_class = quotas.Fixture

    def test_tenant_quotas_get(self):
        tenant_id = 'test'
        self.cs.quotas.get(tenant_id)
        self.assert_called('GET', '/os-quota-sets/%s?usage=False' % tenant_id)

    def test_tenant_quotas_defaults(self):
        tenant_id = 'test'
        self.cs.quotas.defaults(tenant_id)
        self.assert_called('GET', '/os-quota-sets/%s/defaults' % tenant_id)

    def test_update_quota(self):
        q = self.cs.quotas.get('test')
        q.update(volumes=2)
        q.update(snapshots=2)
        self.assert_called('PUT', '/os-quota-sets/test')

    def test_refresh_quota(self):
        q = self.cs.quotas.get('test')
        q2 = self.cs.quotas.get('test')
        self.assertEqual(q.volumes, q2.volumes)
        self.assertEqual(q.snapshots, q2.snapshots)
        q2.volumes = 0
        self.assertNotEqual(q.volumes, q2.volumes)
        q2.snapshots = 0
        self.assertNotEqual(q.snapshots, q2.snapshots)
        q2.get()
        self.assertEqual(q.volumes, q2.volumes)
        self.assertEqual(q.snapshots, q2.snapshots)

    def test_delete_quota(self):
        tenant_id = 'test'
        self.cs.quotas.delete(tenant_id)
        self.assert_called('DELETE', '/os-quota-sets/test')
