DOCUMENTATION = '''
---
module: create_disk
short_description: Create disk
description: 
requirements:
    - yandexcloud
options:
    create_disk:
        description: This module calls the Yandex cloud resource manager service to create disk.
        required: True
author:
    - Alina Ibragimova (@pelmeshka812)
'''
EXAMPLES = '''
- hosts: localhost
  tasks:
    - name: Create disk on YC
      create_disk:
        iam_token: '{{iam_token}}'
        organization_id: '{{organization_id}}'
        name:
        description:
        labels:
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


def create_disk(iam_token, name, description, labels, organization_id):
    api_url = "https://compute.api.cloud.yandex.net/compute/v1/disks"
    headers = {
        'Authorization': 'Bearer ' + iam_token,
        'Content-Type': 'application/x-www-form-urlencoded'

    }
    data = {
        "name": name,
        "description": description,
        "labels": labels,
        "organizationId": organization_id

    }

    response = requests.post(api_url, headers=headers, data=data)
    result = response.json()
    print(response.status_code)
    print(result)
    if response.status_code == 200:
        result = {"status": "SUCCESS", "data": result['folder']}
        return False, result
    if response.status_code == 404:
        result = {"status": response.status_code, "data": response.json()}
        return False, result


def main():
    fields = {
        "iam_token": {"required": True, "type": "str"},
        "organization_id": {"required": True, "type": "str"},
        "name": {"required": True, "type": "str"},
        "description": {"required": False, "type": "str"},
        "labels": {"required": False, "type": "object"},
    }
    module = AnsibleModule(argument_spec=fields)
    is_error, result = create_disk(
        iam_token=module.params['iam_token'],
        organization_id=module.params['organization_id'],
        name= module.params['name'],
        description=module.params['description'],
        labels=module.params['labels'])
    if not is_error:
        module.exit_json(meta=result)
    else:
        module.fail_json(msg="Error getting folder info", meta=result)


if __name__ == '__main__':
    main()
