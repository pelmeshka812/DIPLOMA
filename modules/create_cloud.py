DOCUMENTATION = '''
---
module: create_cloud
short_description: Create cloud 
description: 
requirements:
    - yandexcloud
options:
    get_folder_list:
        description: This module calls the Yandex cloud resource manager service to create cloud.
        required: True
author:
    - Alina Ibragimova (@pelmeshka812)
'''
EXAMPLES = '''
- hosts: localhost
  tasks:
    - name: Getting folders info from YC
      create_cloud:
        iam_token: '{"iam_token":"yZ4fYf6jrnWeXyCg"}'
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


def create_cloud(iam_token, organization_id, name, description, labels):
    api_url = "https://resource-manager.api.cloud.yandex.net/resource-manager/v1/clouds"
    headers = {
        'Authorization': 'Bearer ' + iam_token,
        'Content-Type': 'application/x-www-form-urlencoded'

    }
    data = {
       "organizationId": organization_id,
       "name": name,
       "description": description,
       "labels":labels
     }

    response = requests.post(api_url, headers=headers, data=data)
    result = response.json()
    print(response.status_code)
    print(result)
    if response.status_code == 200:
        result = {"status": "SUCCESS", "data": result['cloud']}
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
    is_error, result = create_cloud(
        iam_token=module.params['iam_token'],
        organization_id=module.params['organization_id'],
        name=module.params['name'],
        description=module.params['description'],
        labels=module.params['labels'])
    if not is_error:
        module.exit_json(meta=result)
    else:
        module.fail_json(msg="Error getting folder info", meta=result)


if __name__ == '__main__':
    main()
