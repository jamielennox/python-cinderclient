# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from cinderclient.tests.fixture_data import client
from cinderclient.tests.fixture_data import volume_types as data
from cinderclient.v1 import volume_types
from cinderclient.tests import utils


class TypesTest(utils.FixturedTestCase):

    client_fixture_class = client.V1
    data_fixture_class = data.Fixture

    def test_list_types(self):
        tl = self.cs.volume_types.list()
        self.assert_called('GET', '/types')
        for t in tl:
            self.assertIsInstance(t, volume_types.VolumeType)

    def test_create(self):
        t = self.cs.volume_types.create('test-type-3')
        self.assert_called('POST', '/types')
        self.assertIsInstance(t, volume_types.VolumeType)

    def test_set_key(self):
        t = self.cs.volume_types.get(1)
        t.set_keys({'k': 'v'})
        self.assert_called('POST',
                           '/types/1/extra_specs',
                           {'extra_specs': {'k': 'v'}})

    def test_unsset_keys(self):
        t = self.cs.volume_types.get(1)
        t.unset_keys(['k'])
        self.assert_called('DELETE', '/types/1/extra_specs/k')

    def test_delete(self):
        self.cs.volume_types.delete(1)
        self.assert_called('DELETE', '/types/1')
