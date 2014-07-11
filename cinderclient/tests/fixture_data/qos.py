# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from cinderclient.tests.fixture_data import base

BASE_URI = 'http://localhost:8776'
TENANT_ID = '0fa851f6668144cf9cd8c8419c1646c1'
QOS_ID1 = '1B6B6A04-A927-4AEB-810B-B7BAAD49F57C'
QOS_ID2 = '0FD8DD14-A396-4E55-9573-1FE59042E95B'


def _stub_qos_full(id=QOS_ID1, base_uri=BASE_URI,
                   tenant_id=TENANT_ID, name='fake-name', specs=None):
    return {
        'qos_specs': {
            'id': id,
            'name': name,
            'consumer': 'back-end',
            'specs': specs or {},
        },
        'links': {
            'href': '%s/%s/backups/%s' % (base_uri, tenant_id, id),
            'rel': 'bookmark'
        }
    }


class Fixture(base.Fixture):

    base_url = 'qos-specs'

    def setUp(self):
        super(Fixture, self).setUp()

        get_all = [_stub_qos_full(name='name-1'),
                   _stub_qos_full(id=QOS_ID2)]
        self.requests.register_uri('GET', self.url(),
                                   json={'qos_specs': get_all})

        self.requests.register_uri('POST', self.url(),
                                   status_code=202,
                                   json=_stub_qos_full(name='qos-name'))

        self.stub_id(QOS_ID1)

    def stub_id(self, id):
        self.requests.register_uri('GET', self.url(id),
                                   json=_stub_qos_full(id=id))

        self.requests.register_uri('PUT', self.url(id), status_code=202)
        self.requests.register_uri('PUT', self.url(id, 'delete_keys'),
                                   status_code=202)
        self.requests.register_uri('DELETE', self.url(id), status_code=202)
        self.requests.register_uri('GET', self.url(id, 'associate'),
                                   status_code=202)
        self.requests.register_uri('GET', self.url(id, 'disassociate'),
                                   status_code=202)
        self.requests.register_uri('GET', self.url(id, 'disassociate_all'),
                                   status_code=202)

        associations = {'qos_associations': [
            {
                'associations_type': 'volume_type',
                'name': 'type1',
                'id': '4230B13A-7A37-4E84-B777-EFBA6FCEE4FF',
            },
            {
                'associations_type': 'volume_type',
                'name': 'type2',
                'id': '4230B13A-7A37-4E84-B777-EFBA6FCEE4FF',
            }
        ]}
        self.requests.register_uri('GET', self.url(id, 'associations'),
                                   status_code=202,
                                   json=associations)
