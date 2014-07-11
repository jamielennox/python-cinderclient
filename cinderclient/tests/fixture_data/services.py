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

from datetime import datetime

import json
from six.moves.urllib import parse as urlparse

from cinderclient.tests.fixture_data import base

# FIXME(jamielennox): use timeutils from oslo
FORMAT = '%Y-%m-%d %H:%M:%S'


def _service_from_request(request):
    body = json.loads(request.body.decode('utf-8'))
    return {'host': body['host'], 'binary': body['binary']}, body


def time(*args):
    return datetime(*args).strftime(FORMAT)


class Fixture(base.Fixture):

    base_url = 'os-services'

    def setUp(self):
        super(Fixture, self).setUp()

        def get(request, context):
            url_parts = urlparse.urlparse(request.url)
            qs = urlparse.parse_qs(url_parts.query)

            host = qs.get('host', None)
            binary = qs.get('binary', None)
            services = [
                {
                    'binary': 'cinder-volume',
                    'host': 'host1',
                    'zone': 'cinder',
                    'status': 'enabled',
                    'state': 'up',
                    'updated_at': time(2012, 10, 29, 13, 42, 2)
                },
                {
                    'binary': 'cinder-volume',
                    'host': 'host2',
                    'zone': 'cinder',
                    'status': 'disabled',
                    'state': 'down',
                    'updated_at': time(2012, 9, 18, 8, 3, 38)
                },
                {
                    'binary': 'cinder-scheduler',
                    'host': 'host2',
                    'zone': 'cinder',
                    'status': 'disabled',
                    'state': 'down',
                    'updated_at': time(2012, 9, 18, 8, 3, 38)
                },
            ]
            if host:
                services = filter(lambda i: i['host'] == host[0], services)
            if binary:
                services = filter(lambda i: i['binary'] == binary[0], services)
            return {'services': services}
        self.requests.register_uri('GET', self.url(), json=get)

        def enable(request, context):
            svc, body = _service_from_request(request)
            svc['status'] = 'enabled'
            return svc
        self.requests.register_uri('PUT', self.url('enable'), json=enable)

        def disable(request, context):
            svc, body = _service_from_request(request)
            svc['status'] = 'disabled'
            return svc
        self.requests.register_uri('PUT', self.url('disable'), json=disable)

        def disable_log_reason(request, context):
            svc, body = _service_from_request(request)
            svc['status'] = 'disabled'
            svc['disabled_reason'] = body['disabled_reason']
            return svc
        self.requests.register_uri('PUT', self.url('disable-log-reason'),
                                   json=disable_log_reason)
