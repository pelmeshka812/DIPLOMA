DOCUMENTATION = '''
---
module: create_vm
short_description: Create virtual machine
description: 
requirements:
    - yandexcloud
options:
    get_folder_list:
        description: This module calls the Yandex cloud resource manager service to create virtual machine.
        required: True
author:
    - Alina Ibragimova (@pelmeshka812)
'''
EXAMPLES = '''
- hosts: localhost
  tasks:
    - name: Create virtual machine on YC
      create_cloud:
        iam_token: '{"iam_token":"yZ4fYf6jrnWeXyCg"}'
        folder_id: '{{folder_id}}'
        name:
        description:
        labels:
        zone_id: '{{zone_id}}'
        platform_id: '{{platform_id}}'
        resource_spec: 
        boot_disk_spec:
      register: result

    - debug: var=result
'''
RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the base64mod module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''
import requests
import json
from ansible.module_utils.basic import AnsibleModule


def create_vm(iam_token, folder_id, name, description, labels, zone_id, platform_id, resources_spec, boot_disk_spec):
    api_url = "https://compute.api.cloud.yandex.net/compute/v1/instances"
    headers = {
        'Authorization': 'Bearer ' + iam_token,
        'Content-Type': 'application/x-www-form-urlencoded'

    }
    data = {
        "folderId": folder_id,
        "name": name,
        "description": description,
        "labels": labels,
        "zoneId": zone_id,
        "platformId": platform_id,
        "resourcesSpec": {
            "memory": resources_spec.memory,
            "cores": resources_spec.cores,
            "coreFraction": resources_spec.core_fraction,
            "gpus": resources_spec.grus
        },
        "bootDiskSpec": {
            "deviceName": boot_disk_spec.device_name,
            "autoDelete": boot_disk_spec.auto_delete,
            "diskId": boot_disk_spec.disk_id
        }

    }

    response = requests.post(api_url, headers=headers, data=data)
    result = response.json()
    print(response.status_code)
    print(result)
    if response.status_code == 200:
        result = {"status": "SUCCESS", "data": result['instance']}
        return False, result
    if response.status_code == 404:
        result = {"status": response.status_code, "data": response.json()}
        return False, result


def main():
    fields = {
        "iam_token": {"required": True, "type": "str"},
        "folder_id": {"required": True, "type": "str"},
        "name": {"required": True, "type": "str"},
        "description": {"required": False, "type": "str"},
        "labels": {"required": False, "type": "object"},
        "zone_id": {"required": True, "type": "str"},
        "platform_id": {"required": True, "type": "str"},
        "resources_spec": {"required": True, "type": "object"},
        "boot_disk_spec": {"required": True, "type": "object"},
    }
    module = AnsibleModule(argument_spec=fields)
    is_error, result = create_vm(
        iam_token=module.params['iam_token'],
        folder_id=module.params['folder_id'],
        name=module.params['name'],
        description=module.params['description'],
        labels=module.params['labels'],
        zone_id=module.params[' zone_id'],
        platform_id=module.params['platform_id'],
        resources_spec=module.params['resources_spec'],
        boot_disk_spec=module.params['boot_disk_spec'])
    if not is_error:
        module.exit_json(meta=result)
    else:
        module.fail_json(msg="Error getting folder info", meta=result)


if __name__ == '__main__':
    main()
