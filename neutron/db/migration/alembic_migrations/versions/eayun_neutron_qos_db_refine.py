# Copyright 2015 OpenStack Foundation
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
#

"""eayun_neutron_qos_db_refine

Revision ID: eayun_neutron_qos_db_refine
Revises: eayun_fw_target_router
Create Date: 2015-12-11 12:00:00.000000

"""
from neutron.db.migration.alembic_migrations import eayun_qos_db_refine_ops


# revision identifiers, used by Alembic.
revision = 'eayun_neutron_qos_db_refine'
down_revision = 'eayun_fw_target_router'


def upgrade():
    eayun_qos_db_refine_ops.upgrade()


def downgrade():
    eayun_qos_db_refine_ops.downgrade()
