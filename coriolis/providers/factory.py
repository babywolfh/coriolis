from coriolis import constants
from coriolis import exception
from coriolis.providers import azure
from coriolis.providers import openstack
from coriolis.providers import vmware_vsphere


EXPORT_PROVIDERS = {
    constants.PLATFORM_VMWARE_VSPHERE: vmware_vsphere.ExportProvider,
    constants.PLATFORM_OPENSTACK: openstack.ExportProvider
}

IMPORT_PROVIDERS = {
    constants.PLATFORM_OPENSTACK: openstack.ImportProvider,
    constants.PLATFORM_AZURE_RM: azure.ImportProvider
}


def get_provider(platform_name, provider_type, event_handler):
    if provider_type == constants.PROVIDER_TYPE_EXPORT:
        cls = EXPORT_PROVIDERS.get(platform_name)
    elif provider_type == constants.PROVIDER_TYPE_IMPORT:
        cls = IMPORT_PROVIDERS.get(platform_name)

    if not cls:
        raise exception.NotFound("Provider not found: %s" % platform_name)
    return cls(event_handler)
