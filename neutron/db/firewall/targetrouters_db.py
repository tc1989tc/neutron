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

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm import exc

from neutron.db import common_db_mixin as base_db
from neutron.db import model_base
from neutron.db import l3_db
from neutron.db.firewall import firewall_db
from neutron.extensions.firewall import FIREWALLS
from neutron.extensions import firewall_target_routers as fw_tr_ext
from neutron.openstack.common import log as logging

LOG = logging.getLogger(__name__)


class FirewallRouterBinding(model_base.BASEV2):
    firewall_id = sa.Column(sa.String(36),
                            sa.ForeignKey('firewalls.id', ondelete='CASCADE'),
                            primary_key=True)
    router_id = sa.Column(sa.String(36),
                          sa.ForeignKey('routers.id', ondelete='CASCADE'),
                          primary_key=True)
    firewalls = orm.relationship(
        firewall_db.Firewall,
        backref=orm.backref(fw_tr_ext.FW_TARGET_ROUTERS,
                            lazy='joined', cascade='delete'))


class FirewallTargetRoutersMixin(base_db.CommonDbMixin):
    """Mixin class for firewall target routers."""

    def _extend_firewall_dict_target_routers(self, firewall_res, firewall_db):
        fw_target_routers = [
            binding.router_id for binding
            in firewall_db[fw_tr_ext.FW_TARGET_ROUTERS]]
        firewall_res[fw_tr_ext.FW_TARGET_ROUTERS] = fw_target_routers
        return firewall_res

    firewall_db.Firewall_db_mixin.register_dict_extend_funcs(
        FIREWALLS, ['_extend_firewall_dict_target_routers'])

    def check_router_in_use(self, context, router_id):
        mq = self._model_query(context, FirewallRouterBinding)
        firewalls = [
            binding.firewall_id for binding
            in mq.filter_by(router_id=router_id)
        ]
        if firewalls:
            raise fw_tr_ext.RouterInUseByFirewall(
                router_id=router_id,
                firewalls=firewalls)

    def _process_create_firewall_target_routers(self, context,
                                                firewall_id, router_ids):
        with context.session.begin(subtransactions=True):
            for router_id in router_ids:
                try:
                    self._get_by_id(context, l3_db.Router, router_id)
                except exc.NoResultFound:
                    LOG.warn(_('Router %s cannot be found'), router_id)
                    continue
                firewall_router_binding_db = FirewallRouterBinding(
                    firewall_id=firewall_id,
                    router_id=router_id)
                context.session.add(firewall_router_binding_db)

    def _get_target_routers(self, context, firewall_id):
        mq = self._model_query(context, FirewallRouterBinding)
        return [db.router_id for db in mq.filter_by(firewall_id=firewall_id)]

    def _delete_target_routers(self, context, firewall_id):
        mq = self._model_query(context, FirewallRouterBinding)
        with context.session.begin(subtransactions=True):
            mq.filter(
                FirewallRouterBinding.firewall_id == firewall_id
            ).delete()
