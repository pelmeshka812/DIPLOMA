#!/usr/bin/python
# from examples.scripts.test.library import get_iam

DOCUMENTATION = '''
---
module: yc_vpc_address
short_description: Manage your address on virtual private cloud

author:
    - Ibragimova Alina (@pelmeshka812)
'''

EXAMPLES = '''
- hosts: localhost
  tasks:
    - name: Create disk on YC
      folder_present:
        iam_token: '{{iam_token}}'
        folder_id: '{{folder_id}}'
        name:
        description:
        labels:
        state: present
      register: result

    - debug: var=result
- name: Delete that address on vpc
  yc_vpc_address:
     folderId: "..."
    name: "..."
    state: absent
  register: result
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
from ansible.module_utils.basic import *
import requests


def folder_present(data, iam_token):
    del data['state']
    api_url = "https://resource-manager.api.cloud.yandex.net/resource-manager/v1/folders"
    headers = {
        'Authorization': 'Bearer ' + iam_token
    }
    result = requests.post(api_url, json.dumps(data), headers=headers)

    if result.status_code == 200:
        return False, True, result.json()
    if result.status_code == 422:
        return False, False, result.json()

    # default: something went wrong
    meta = {"status": result.status_code, 'response': result.json()}
    return True, False, meta


def folder_absent(folderId, iam_token):
    headers = {
        'Authorization': 'Bearer ' + iam_token}
    api_url = "https://resource-manager.api.cloud.yandex.net/resource-manager/v1/folders/" +folderId
    result = requests.delete(api_url, headers=headers)

    if result.status_code == 204:
        return False, True, {"status": "SUCCESS"}
    if result.status_code == 404:
        result = {"status": result.status_code, "data": result.json()}
        return False, False, result
    else:
        result = {"status": result.status_code, "data": result.json()}
        return True, False, result


def main():
    fields = {
        "iam_token": {"required": True, "type": "str"},
        "folderId": {"required": True, "type": "str"},
        "name": {"required": True, "type": "str"},
        "description": {"required": False, "type": "str"},
        "labels": "object",
        "externalIpv4AddressSpec": {
            "address": {"required": False, "type": "str"},
            "zoneId": {"required": False, "type": "str"},
            "requirements": {
                "ddosProtectionProvider": {"required": False, "type": "str"},
                "outgoingSmtpCapability": {"required": False, "type": "str"}
            }
        },
        "state": {
            "default": "present",
            "choices": ['present', 'absent'],
            "type": 'str'
        },
    }
    choice_map = {
        "present": folder_present,
        "absent": folder_absent,
    }

    module = AnsibleModule(argument_spec=fields)
    is_error, has_changed, result = choice_map.get(
        module.params['state'])(module.params)

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Error", meta=result)


if __name__ == '__main__':
    main()
