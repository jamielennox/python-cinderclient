# Copyright (C) 2013 eBay Inc.
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
from cinderclient.tests.fixture_data import qos
from cinderclient.tests import utils


class QoSSpecsTest(utils.FixturedTestCase):

    client_fixture_class = client.V1
    data_fixture_class = qos.Fixture

    def test_create(self):
        specs = dict(k1='v1', k2='v2')
        self.cs.qos_specs.create('qos-name', specs)
        self.assert_called('POST', '/qos-specs')

    def test_get(self):
        self.cs.qos_specs.get(qos.QOS_ID1)
        self.assert_called('GET', '/qos-specs/%s' % qos.QOS_ID1)

    def test_list(self):
        self.cs.qos_specs.list()
        self.assert_called('GET', '/qos-specs')

    def test_delete(self):
        self.cs.qos_specs.delete(qos.QOS_ID1)
        self.assert_called('DELETE',
                           '/qos-specs/1B6B6A04-A927-4AEB-810B-B7BAAD49F57C?'
                           'force=False')

    def test_set_keys(self):
        body = {'qos_specs': dict(k1='v1')}
        self.cs.qos_specs.set_keys(qos.QOS_ID1, body)
        self.assert_called('PUT', '/qos-specs/%s' % qos.QOS_ID1)

    def test_unset_keys(self):
        body = {'keys': ['k1']}
        self.cs.qos_specs.unset_keys(qos.QOS_ID1, body)
        self.assert_called('PUT', '/qos-specs/%s/delete_keys' % qos.QOS_ID1)

    def test_get_associations(self):
        self.cs.qos_specs.get_associations(qos.QOS_ID1)
        self.assert_called('GET', '/qos-specs/%s/associations' % qos.QOS_ID1)

    def test_associate(self):
        type_id = '4230B13A-7A37-4E84-B777-EFBA6FCEE4FF'
        self.cs.qos_specs.associate(qos.QOS_ID1, type_id)
        self.assert_called('GET', '/qos-specs/%s/associate?vol_type_id=%s'
                           % (qos.QOS_ID1, type_id))

    def test_disassociate(self):
        type_id = '4230B13A-7A37-4E84-B777-EFBA6FCEE4FF'
        self.cs.qos_specs.disassociate(qos.QOS_ID1, type_id)
        self.assert_called('GET', '/qos-specs/%s/disassociate?vol_type_id=%s'
                           % (qos.QOS_ID1, type_id))

    def test_disassociate_all(self):
        self.cs.qos_specs.disassociate_all(qos.QOS_ID1)
        self.assert_called('GET', '/qos-specs/%s/disassociate_all'
                           % qos.QOS_ID1)
