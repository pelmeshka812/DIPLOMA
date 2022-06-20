DOCUMENTATION = '''
---
module: get_folder_list
short_description: Getting folders info
description: 
requirements:
    - yandexcloud
options:
    get_folder_list:
        description: This module calls the Yandex cloud resource manager service to get a list of available folders.
        required: True
author:
    - Alina Ibragimova (@pelmeshka812)
'''
EXAMPLES = '''
- hosts: localhost
  tasks:
    - name: Getting folders info from YC
      get_folder_list:
        iam_token: '{{iam_token}}'
        cloud_id: '{{cloud_id}}'
        pageSize:
        pageToken:
        filter:
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


def get_folder_list(iam_token, cloud_id, pageSize, pageToken, filter):
    api_url = "https://resource-manager.api.cloud.yandex.net/resource-manager/v1/folders"
    headers = {
        'Authorization': 'Bearer ' + iam_token,
        'Content-Type': 'application/x-www-form-urlencoded'

    }
    params = {
        "cloud_id": cloud_id,
        "pageSize": pageSize,
        "pageToken": pageToken,
        "filter": filter
    }

    response = requests.get(api_url, headers=headers, params=params)
    result = response.json()
    print(response.status_code)
    print(result)
    if response.status_code == 200:
        result = {"status": "SUCCESS", "data": result['folders']}
        return False, result
    if response.status_code == 404:
        result = {"status": response.status_code, "data": response.json()}
        return False, result


def main():
    fields = {
        "iam_token": {"required": True, "type": "str"},
        "cloud_id": {"required": True, "type": "str"},
        "pageSize": {"required": False, "type": "str"},
        "pageToken": {"required": False, "type": "str"},
        "filter": {"required": False, "type": "str"}
    }
    module = AnsibleModule(argument_spec=fields)
    is_error, result = get_folder_list(
        iam_token=module.params['iam_token'],
        cloud_id=module.params['cloud_id'],
        pageSize=module.params['pageSize'],
        pageToken=module.params['pageToken'],
        filter=module.params['filter'])
    if not is_error:
        module.exit_json(meta=result)
    else:
        module.fail_json(msg="Error getting folder list", meta=result)


if __name__ == '__main__':
    main()
