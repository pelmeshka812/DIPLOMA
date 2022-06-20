DOCUMENTATION = '''
---
module: get_zone_list
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
        pageSize: 
        pageToken:
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


def get_zone_list(iam_token,  pageSize, pageToken):
    api_url = "https://compute.api.cloud.yandex.net/compute/v1/zones"
    headers = {
        'Authorization': 'Bearer ' + iam_token,
        'Content-Type': 'application/x-www-form-urlencoded'

    }
    params = {
        "pageSize": pageSize,
        "pageToken": pageToken
    }

    response = requests.get(api_url, headers=headers, params=params)
    result = response.json()
    print(response.status_code)
    print(result)
    if response.status_code == 200:
        result = {"status": "SUCCESS", "data": result['zones']}
        return False, result
    if response.status_code == 404:
        result = {"status": response.status_code, "data": response.json()}
        return False, result


def main():
    fields = {
        "iam_token": {"required": True, "type": "str"},
        "pageSize": {"required": False, "type": "str"},
        "pageToken": {"required": False, "type": "str"}
    }
    module = AnsibleModule(argument_spec=fields)
    is_error, result = get_zone_list(
        iam_token=module.params['iam_token'],
        pageSize=module.params['pageSize'],
        pageToken=module.params['pageToken'])
    if not is_error:
        module.exit_json(meta=result)
    else:
        module.fail_json(msg="Error getting zone list", meta=result)


if __name__ == '__main__':
    main()
