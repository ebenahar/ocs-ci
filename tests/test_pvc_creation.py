import os
import logging
import ocs.defaults as defaults
import yaml
import oc.openshift_ops
from ocs import exceptions
from ocs import ocp
from utility import utils, templating
from ocsci.enums import TestStatus


log = logging.getLogger(__name__)

PVC_YAML = os.path.join("templates/ocs-deployment", "PersistentVolumeClaim.yaml")
TEMP_YAML_FILE = 'test.yaml'
VOLUME_DELETED = 'persistentvolume "{volume_name}" deleted'

OCP = oc.openshift_ops.OCP()


def create_pv(**kwargs):
    """
    Create a new Persistent Volume
    """
    from ipdb import set_trace;set_trace()
    file_y = templating.generate_yaml_from_jinja2_template_with_data(
        PVC_YAML, **kwargs
    )
    with open(TEMP_YAML_FILE, 'w') as yaml_file:
        yaml.dump(file_y, yaml_file, default_flow_style=False)
        log.info(f"Creating new Persistent Volume")
    assert OCP.v1_service_list.create(yaml_file=TEMP_YAML_FILE)
    # return OCP.wait_for_resource_status(kwargs['pvc_name'], 'Available')


def run(**kwargs):
    """
    A simple function to exercise a resource creation through api-client
    """

    pvc_data = {}
    pvc_name = 'my-pvc1'
    pvc_data['pvc_name'] = pvc_name
    pvc_data['pv_size'] = '3Gi'
    assert create_pv(**pvc_data)
    # assert verify_pv_exist(pv_name)
    # assert delete_pv(pv_name)
    # assert not verify_pv_exist(pv_name)
    # utils.delete_file(TEMP_YAML_FILE)
    # return TestStatus.PASSED
