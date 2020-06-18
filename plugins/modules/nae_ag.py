#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

#     def createPreChange(self, ag_name,name,description,interactive_flag,changes):

ANSIBLE_METADATA = {'metadata_version': '1.1', 'status': ['preview'],
                    'supported_by': 'certified'}

DOCUMENTATION = \
    r'''
---
module: nae_ag
short_description: Manage assurance groups.
description:
- Manage Assurance Groups on Cisco NAE fabrics.
version_added: '2.4'
options:
  name:
    description:
    - The name of the assurance group.
    type: str
    required: yes
    aliases: [ fab_name ]
  description:
    description:
    - Description for the assurance group  analysis.
    type: str
    required: no
    aliases: [ descr ]
  state:
    description:
    - Use C(present) or C(absent) for adding or removing.
    - Use C(query) for listing an object or multiple objects.
    - Use C(modify) when editing config.
    type: str
    choices: [ absent, present, query, modify ]
    default: present
    
author:
- Shantanu Kulkarni (@shan_kulk)
'''

EXAMPLES = \
    r'''
- name: View all assurance groups
  nae_ag:
    host: nae
    port: 8080
    username: Admin
    password: 1234
    state: query
- name: View Assurance Group Configuration
  nae_ag:
    host: nae
    port: 8080
    username: Admin
    password: 1234
    state: query
    name: AG1
- name: Create Offline Assurance Group
  nae_ag:
    host: nae
    port: 8080
    username: Admin
    password: 1234
    state: present
    name: AG1
'''

RETURN = \
    '''
resp:
    description: Return payload
    type: str
    returned: always
'''

import requests
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.nae.plugins.module_utils.nae import NAEModule, nae_argument_spec
# from ansible.module_utils.network.aci.nae import NAEModule, \
    # nae_argument_spec
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def main():
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    result = dict(changed=False,resp='')
    argument_spec = nae_argument_spec()
    argument_spec.update(  # Not required for querying all objects
        name=dict(type='str', aliases=['name']),
        description=dict(type='str'),
        validate_certs=dict(type='bool', default=False),
        state=dict(type='str', default='present', choices=['absent',
                   'present', 'query', 'modify']),
        )

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True,
                           required_if=[['state', 'absent', ['name']],
                           ['state', 'present', ['name']]])

    description = module.params.get('description')
    state = module.params.get('state')
    name = module.params.get('name')
    nae = NAEModule(module)

    if state == 'query' and name:
        ag = nae.get_assurance_group(name)
        if ag is None:
            module.exit_json(msg='No such Assurance Group exists', **nae.result)
        nae.result['Result'] = ag
        module.exit_json(**nae.result)
    elif state == 'query' and not name:
        nae.get_all_assurance_groups()
        nae.result['Result'] = nae.assuranceGroups
        module.exit_json(**nae.result)
    elif state == 'absent' and name:
        nae.deleteAG()
        result['changed'] = True
        module.exit_json(**nae.result)
    elif state == 'present' and name:
        nae.newOfflineAG()
        result['changed'] = True
        module.exit_json(**nae.result)




    module.fail_json(msg='Incorrect params passed', **self.result)


if __name__ == '__main__':
    main()

