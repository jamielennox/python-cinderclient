# Copyright (C) 2013 Hewlett-Packard Development Company, L.P.
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
from cinderclient.tests.fixture_data import volume_backups as data
from cinderclient.tests import utils


class VolumeBackupsTest(utils.FixturedTestCase):

    client_fixture_class = client.V2
    data_fixture_class = data.V2

    def test_create(self):
        self.cs.backups.create('2b695faf-b963-40c8-8464-274008fbcef4')
        self.assert_called('POST', '/backups')

    def test_get(self):
        backup_id = '76a17945-3c6f-435c-975b-b5685db10b62'
        self.cs.backups.get(backup_id)
        self.assert_called('GET', '/backups/%s' % backup_id)

    def test_list(self):
        self.cs.backups.list()
        self.assert_called('GET', '/backups/detail')

    def test_delete(self):
        b = self.cs.backups.list()[0]
        b.delete()
        self.assert_called('DELETE',
                           '/backups/76a17945-3c6f-435c-975b-b5685db10b62')
        self.cs.backups.delete('76a17945-3c6f-435c-975b-b5685db10b62')
        self.assert_called('DELETE',
                           '/backups/76a17945-3c6f-435c-975b-b5685db10b62')
        self.cs.backups.delete(b)
        self.assert_called('DELETE',
                           '/backups/76a17945-3c6f-435c-975b-b5685db10b62')

    def test_restore(self):
        backup_id = '76a17945-3c6f-435c-975b-b5685db10b62'
        self.cs.restores.restore(backup_id)
        self.assert_called('POST', '/backups/%s/restore' % backup_id)

    def test_record_export(self):
        backup_id = '76a17945-3c6f-435c-975b-b5685db10b62'
        self.cs.backups.export_record(backup_id)
        self.assert_called('GET',
                           '/backups/%s/export_record' % backup_id)

    def test_record_import(self):
        backup_service = 'fake-backup-service'
        backup_url = 'fake-backup-url'
        expected_body = {'backup-record': {'backup_service': backup_service,
                                           'backup_url': backup_url}}
        self.cs.backups.import_record(backup_service, backup_url)
        self.assert_called('POST', '/backups/import_record', expected_body)
