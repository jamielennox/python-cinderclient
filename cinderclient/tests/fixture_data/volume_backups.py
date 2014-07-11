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

BACKUP_ID = '76a17945-3c6f-435c-975b-b5685db10b62'
BASE_URI = 'http://localhost:8776'
TENANT_ID = '0fa851f6668144cf9cd8c8419c1646c1'


def _self_href(base_uri, tenant_id, backup_id):
    return '%s/v1/%s/backups/%s' % (base_uri, tenant_id, backup_id)


def _bookmark_href(base_uri, tenant_id, backup_id):
    return '%s/%s/backups/%s' % (base_uri, tenant_id, backup_id)


def _stub_backup(id, base_uri=BASE_URI, tenant_id=TENANT_ID):
    return {
        'id': BACKUP_ID,
        'name': 'backup',
        'links': [
            {
                'href': _self_href(id, base_uri, tenant_id),
                'rel': 'self'
            },
            {
                'href': _bookmark_href(id, base_uri, tenant_id),
                'rel': 'bookmark'
            }
        ]
    }


def _stub_backup_full(id, base_uri=BASE_URI, tenant_id=TENANT_ID):
    bak = _stub_backup(id, base_uri, tenant_id)

    bak['description'] = 'nightly backup'
    bak['volume_id'] = '712f4980-5ac1-41e5-9383-390aa7c9f58b'
    bak['container'] = 'volumebackups'
    bak['object_count'] = 220
    bak['size'] = 10
    bak['availability_zone'] = 'az1'
    bak['created_at'] = '2013-04-12T08:16:37.000000'
    bak['status'] = 'available'

    return bak


class V1(base.Fixture):

    base_url = 'backups'

    def setUp(self):
        super(V1, self).setUp()
        self.backups = []
        self.requests.register_uri('GET', self.url('detail'),
                                   json={'backups': self.backups})

        self.register(BACKUP_ID)
        self.register('d09534c6-08b8-4441-9e87-8976f3a8f699')
        self.restore(1234)

        self.requests.register_uri('POST', self.url(), status_code=202,
                                   json={'backup': _stub_backup(BACKUP_ID)})

    def restore(self, id):
        restore = {'volume_id': '712f4980-5ac1-41e5-9383-390aa7c9f58b'}
        self.requests.register_uri('POST', self.url(id, 'restore'),
                                   json={'restore': restore})

    def register(self, id):
        bak = _stub_backup_full(id)
        self.backups.append(bak)
        self.requests.register_uri('GET', self.url(id), json={'backup': bak})
        self.requests.register_uri('DELETE', self.url(id), status_code=202)
        self.restore(id)


class V2(V1):

    def setUp(self):
        super(V2, self).setUp()

        self.export_record(1234)
        self.requests.register_uri('POST', self.url('import_record'),
                                   json={'backup': _stub_backup(BACKUP_ID)})

    def export_record(self, id):
        record = {'backup-record': {'backup_service': 'fake-backup-service',
                                    'backup_url': 'fake-backup-url'}}
        self.requests.register_uri('GET', self.url(id, 'export_record'),
                                   json=record)

    def register(self, id):
        super(V2, self).register(id)
        self.export_record(id)
