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
- name: Create a address vpc
  yc_vpc_address:
    folderId: "..."
    name: "..."
    description: "This is your address on vpc"
    labels: yes
    externalIpv4AddressSpec: no
    requirements: no
    state: present
  register: result
- name: Delete that address on vpc
  yc_vpc_address:
     folderId: "..."
    name: "..."
    state: absent
  register: result
'''

from ansible.module_utils.basic import *
import requests


def balancer_present(data, iam_token):
    del data['state']
    api_url = "https://load-balancer.api.cloud.yandex.net/load-balancer/v1/networkLoadBalancers"
    headers = {
        'Authorization': 'Bearer ' + iam_token
    }
    result = requests.post(api_url, json.dumps(data), headers=headers)

    if result.status_code == 200:
        return False, True, result.json()
    if result.status_code == 422:
        return False, False, result.json()

    meta = {"status": result.status_code, 'response': result.json()}
    return True, False, meta


def balancer_absent(data):
    headers = {
        'Authorization': 'Bearer'
    }
    api_url = "https://load-balancer.api.cloud.yandex.net/load-balancer/v1/networkLoadBalancers/"+data
    result = requests.delete(api_url, headers=headers)
    print(type(data))
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
        "network_load_balancer_id": {"required": True, "type": "str"},
        "state": {
            "default": "present",
            "choices": ['present', 'absent'],
            "type": 'str'
        },
    }
    choice_map = {
        "present": balancer_present,
        "absent": balancer_absent,
    }

    module = AnsibleModule(argument_spec=fields)
    is_error, has_changed, result = choice_map.get(
        module.params['state'])(module.params)

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Error deleting repo", meta=result)


if __name__ == '__main__':
    main()
