import os
import string
import yaml
import copy

from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('scenariobuilder', 'templates'))

from scenariobuilder.metadata import build_metadata

def load_role(yaml_dir, hostname, scenario):
    with open(yaml_dir+'/role_mappings.yaml') as yaml_file:
        y = yaml.load(yaml_file.read())
        if hostname not in y:
            print "WARNING: " + hostname + " does not have a role mapped to it"
            return None
        return y[hostname]

def load_class_groups(yaml_dir, role, hostname,scenario):
    with open(yaml_dir+'/scenarios/'+scenario+'.yaml') as yaml_file:
        y = yaml.load(yaml_file.read())
        if role not in y['roles']:
            # Not all roles have class groups, some just have classes
            return []
        if 'class_groups' not in y['roles'][role]:
            return []
        return y['roles'][role]['class_groups']

def build_wait_list(hostname, scenario, yaml_dir, replacements):
    with open(yaml_dir+'/nodes/'+scenario+'.yaml') as yaml_file:
        y = yaml.load(yaml_file.read())
        if 'wait' in y['nodes'][hostname]:
            return map_names_to_ips(y['nodes'][hostname]['wait'], replacements)
        else:
            return None

def map_names_to_ips(hostnames, replacements):
    ips = []
    for hostname in hostnames:
        if 'ci_'+hostname.replace('-', '_') not in replacements:
            ips.append('192.168.123.123')
            print "Node " + hostname + "CI netowrk IP not in metadata, using 192.168.123.123"
        else:
            ips.append(replacements['ci_'+hostname.replace('-', '_')])
    return ips

# Build role == puppet master
# this may get complex if AIO takes over the
# build role but doesn't specify it.

def compose(hostname, yaml_dir, scenario, r):
    replacements = copy.deepcopy(r)
    template = env.get_template('bootstrap.jinja2')

    role = load_role(yaml_dir, hostname, scenario)
    class_groups = load_class_groups(yaml_dir, role, hostname, scenario)

    replacements['wait_nodes'] = build_wait_list(hostname, scenario, yaml_dir, replacements)
    replacements['role'] = role
    replacements['class_groups'] = class_groups
    replacements['hostname'] = hostname

    print replacements

    return template.render(replacements)

def show(n, q, k, args):
    hostname = args.node
    yaml_dir = args.yaml_dir
    scenario = args.scenario

    print compose(hostname, yaml_dir, scenario, build_metadata('./data', '2_role', 'config'))
