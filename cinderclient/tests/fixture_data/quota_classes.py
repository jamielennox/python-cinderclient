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

import json

from cinderclient.tests.fixture_data import base


class Fixture(base.Fixture):

    base_url = 'os-quota-class-sets'

    def setUp(self):
        super(Fixture, self).setUp()
        self.stub_id('test')

    def stub_id(self, id):
        self.requests.register_uri('GET', self.url(id), json={
            'quota_class_set': {'class_name': id,
                                'metadata_items': [],
                                'volumes': 1,
                                'snapshots': 1,
                                'gigabytes': 1}})

        def put(request, context):
            body = json.loads(request.body.decode('utf-8'))
            assert list(body) == ['quota_class_set']
            assert 'class_name' in body['quota_class_set']
            return {'quota_class_set': {'class_name': id,
                                        'metadata_items': [],
                                        'volumes': 2,
                                        'snapshots': 2,
                                        'gigabytes': 1}}
        self.requests.register_uri('PUT', self.url(id), json=put)
