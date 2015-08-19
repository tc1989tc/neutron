# Copyright (c) 2015 Eayun, Inc.
# All rights reserved.
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


from neutron.api import extensions
from neutron.api.v2 import attributes as attr
from neutron.common import exceptions as nexception
from neutron.extensions.firewall import FIREWALLS

FW_TARGET_ROUTERS = 'fw_target_routers'


class RouterInUseByFirewall(nexception.InUse):
    message = _("Router %(router_id)s is used by firewalls: %(firewalls)s")


EXTENDED_ATTRIBUTES_2_0 = {
    FIREWALLS: {
        FW_TARGET_ROUTERS: {'allow_post': True, 'allow_put': True,
                            'validate': {'type:uuid_list': None},
                            'convert_to': attr.convert_none_to_empty_list,
                            'default': attr.ATTR_NOT_SPECIFIED,
                            'is_visible': True},
    }
}


class Firewall_target_routers(extensions.ExtensionDescriptor):
    """Extension class supporting firewall target routers."""

    @classmethod
    def get_name(cls):
        return "Firewall Target Routers"

    @classmethod
    def get_alias(cls):
        return "firewall-target-routers"

    @classmethod
    def get_description(cls):
        return "Allow specifying target routers for firewalls"

    @classmethod
    def get_namespace(cls):
        return "https://github.com/eayunstack"

    @classmethod
    def get_updated(cls):
        return "2015-08-18T12:00:00-00:00"

    def get_extended_resources(self, version):
        if version == "2.0":
            return EXTENDED_ATTRIBUTES_2_0
        else:
            return {}
