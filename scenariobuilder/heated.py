#!/usr/bin/env python
"""
    stack-builder.heated
    ~~~~~~~~~~~~~~~~~~~
    
    This module is reponsible for creating VMs on the target cloud,
    and pushing the appropriate metadata and init scripts to them

"""
import bootstrap
import yaml

from datetime import datetime
from metadata import build_metadata

def heat(args):
    data_path = args.data_path
    scenario = args.scenario

    t = datetime.now()
    test_id = ''.join(map(str, [t.year, t.month, t.day, t.hour, t.minute, t.second, t.microsecond]))

    with open(data_path + '/nodes/heat/bootstrap.sh') as user_data_raw_file:
      user_data_raw = user_data_raw_file.read()

    with open(data_path + '/nodes/heat/' + scenario + '.yaml') as heat_template:
      heat_yaml = yaml.load(heat_template.read())
   
    for resource_set,details_set in heat_yaml['resources'].items():
        if details_set['type'] == 'OS::Nova::Server':
            if 'wait_nodes' in details_set['properties']['metadata']:
                for wait_node in details_set['properties']['metadata']['wait_nodes'].split(' '):
                    details_set['properties']['metadata']['NODE_' + wait_node] = { 'get_attr': [ wait_node, 'first_address' ] }

    # config is a dictionary updated from env vars and user supplied
    # yaml files to serve as input to hiera and build scripts
    initial_config_meta = build_metadata(data_path, scenario, 'config')
    hiera_config_meta =  build_metadata(data_path, scenario, 'user')
    global_config_meta =  build_metadata(data_path, scenario, 'global')

    for node,details in heat_yaml['resources'].items():
        if details['type'] == 'OS::Nova::Server':
            role = bootstrap.load_role(data_path, node, scenario)
            class_groups = bootstrap.load_class_groups(data_path, role, node, scenario)
            details['properties']['metadata']['role'] = role
            details['properties']['user_data'] = user_data_raw
            details['properties']['metadata']['class_groups'] = ' '.join(class_groups)
            for config, value in initial_config_meta.items():
                details['properties']['metadata'][config] = value 
            for user, value in hiera_config_meta.items():
                details['properties']['metadata']['OS_USER_'+user] = value 
            for glob, value in global_config_meta.items():
                details['properties']['metadata']['OS_GLOB_'+glob] = value 

    with open('heat.yaml', 'w' ) as temp_file:
        temp_file.write(str(yaml.dump(heat_yaml)))
