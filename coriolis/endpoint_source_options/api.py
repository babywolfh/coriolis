# Copyright 2019 Cloudbase Solutions Srl
# All Rights Reserved.

from coriolis.conductor.rpc import client as rpc_client


class API(object):
    def __init__(self):
        self._rpc_client = rpc_client.ConductorClient()

    def get_endpoint_source_options(
            self, ctxt, endpoint_id, env=None, option_names=None):
        return self._rpc_client.get_endpoint_source_options(
            ctxt, endpoint_id, env, option_names)
