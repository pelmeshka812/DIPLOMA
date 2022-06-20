DOCUMENTATION = '''
---
module: get_cloud_list
short_description: Getting clouds info
requirements:
    - yandexcloud
options:
    get_cloud_list:
        description: This module calls the Yandex cloud resource manager service to get a list of available clouds.
        required: True
author:
    - Alina Ibragimova (@pelmeshka812)
'''
EXAMPLES = '''
- hosts: localhost
  tasks:
    - name: Getting clouds info from YC
      get_cloud_list:
        iam_token: 
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


def get_cloud_list(iam_token):
    api_url = "https://resource-manager.api.cloud.yandex.net/resource-manager/v1/clouds"
    headers = {
        'Authorization': 'Bearer ' + iam_token,
        'Content-Type': 'application/x-www-form-urlencoded'

    }

    response = requests.get(api_url, headers=headers)
    result = response.json()
    print(response.status_code)
    print(result)
    if response.status_code == 200:
        result = {"status": "SUCCESS", "data": result['clouds']}
        return False, result
    if response.status_code == 404:
        result = {"status": response.status_code, "data": response.json()}
        return False, result


def main():
    fields = {
        "iam_token": {"required": True, "type": "str"}
    }
    module = AnsibleModule(argument_spec=fields)
    is_error, result = get_cloud_list(iam_token=module.params['iam_token'])
    if not is_error:
        module.exit_json(meta=result)
    else:
        module.fail_json(msg="Error getting cloud list", meta=result)


if __name__ == '__main__':
    main()
