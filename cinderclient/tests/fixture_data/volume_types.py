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


class Fixture(base.Fixture):

    base_url = 'types'

    def setUp(self):
        super(Fixture, self).setUp()
        self.types = []
        self.requests.register_uri('GET', self.url(),
                                   json={'volume_types': self.types})

        self.requests.register_uri('POST', self.url(), status_code=202,
                                   json={'volume_type': {'id': 3,
                                                         'name': 'test-type-3',
                                                         'extra_specs': {}}})

        self.register(1, 'test-type-1')
        self.register(2, 'test-type-2')

        self.requests.register_uri('POST', self.url(1, 'extra_specs'),
                                   json={'extra_specs': {'k': 'v'}})
        self.requests.register_uri('DELETE', self.url(1, 'extra_specs', 'k'),
                                   status_code=204)

    def register(self, id, name, extra_specs=None):
        typ = {'id': id, 'name': name, 'extra_specs': extra_specs or {}}
        self.types.append(typ)

        self.requests.register_uri('GET', self.url(id),
                                   json={'volume_type': typ})
        self.requests.register_uri('DELETE', self.url(id), status_code=202)
