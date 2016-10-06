# Copyright 2016 Cloudbase Solutions Srl
# All Rights Reserved.

from webob import exc

from oslo_log import log as logging

from coriolis.api import wsgi as api_wsgi
from coriolis.api.v1.views import replica_view
from coriolis import constants
from coriolis import exception
from coriolis.replicas import api
from coriolis.providers import factory

LOG = logging.getLogger(__name__)


class ReplicaController(api_wsgi.Controller):
    def __init__(self):
        self._replica_api = api.API()
        super(ReplicaController, self).__init__()

    def show(self, req, id):
        replica = self._replica_api.get_replica(
            req.environ["coriolis.context"], id)
        if not replica:
            raise exc.HTTPNotFound()

        return replica_view.single(req, replica)

    def index(self, req):
        return replica_view.collection(
            req, self._replica_api.get_replicas(
                req.environ['coriolis.context'],
                include_tasks_executions=False))

    def detail(self, req):
        return replica_view.collection(
            req, self._replica_api.get_replicas(
                req.environ['coriolis.context'],
                include_tasks_executions=True))

    def _validate_create_body(self, body):
        try:
            replica = body["replica"]

            origin = replica["origin"]
            destination = replica["destination"]

            export_provider = factory.get_provider(
                origin["type"], constants.PROVIDER_TYPE_EXPORT, None)
            export_provider.validate_connection_info(
                origin.get("connection_info", {}))

            import_provider = factory.get_provider(
                destination["type"], constants.PROVIDER_TYPE_IMPORT, None)
            import_provider.validate_connection_info(
                destination.get("connection_info", {}))

            import_provider.validate_target_environment(
                destination.get("target_environment", {}))

            return origin, destination, replica["instances"]
        except Exception as ex:
            LOG.exception(ex)
            if hasattr(ex, "message"):
                msg = ex.message
            else:
                msg = str(ex)
            raise exception.InvalidInput(msg)

    def create(self, req, body):
        origin, destination, instances = self._validate_create_body(body)
        return replica_view.single(req, self._replica_api.create(
            req.environ['coriolis.context'], origin, destination, instances))

    def delete(self, req, id):
        try:
            self._replica_api.delete(req.environ['coriolis.context'], id)
            raise exc.HTTPNoContent()
        except exception.NotFound as ex:
            raise exc.HTTPNotFound(explanation=ex.msg)


def create_resource():
    return api_wsgi.Resource(ReplicaController())