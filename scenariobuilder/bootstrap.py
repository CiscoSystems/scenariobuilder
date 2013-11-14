import os
import string
import yaml
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('stack-builder', 'templates'))

from metadata import build_metadata

# Load in roles and node list
# Do substitutions based on roles.

# Build role == puppet master
# this may get complex if AIO takes over the
# build role but doesn't specify it.

"""
build-server:
      - 'bash-top'
      - 'fqdn-fix'
      - 'pw-mirror-network'
      - 'apt-packages'
      - 'cloud-init-log'
      - 'git-proxy'
      - 'puppet-modules'
      - 'hiera-config'
      - 'puppet-master-fact'
      - 'puppet-setup'
      - 'puppet-site'
      - 'SIGNAL_stack'

control-server:
      - 'bash-top'
      - 'fqdn-fix'
      - 'pw-mirror-network'
      - 'apt-packages'
      - 'cloud-init-log'
      - 'git-proxy'
      - 'puppet-modules'
      - 'puppet-agent-fact'
      - 'hiera-config'
      - 'puppet-setup'
      - 'WAIT_stack build-server'
      - 'puppet-agent'
      - 'SIGNAL_control'
"""



def compose(hostname, yaml_dir, fragment_dir, scenario, replacements):
    template = env.get_template('bootstrap.jinja2')

    fragments = load_yaml_config(hostname, yaml_dir, fragment_dir, scenario)
    script = build_deploy(fragment_dir, fragments, replacements)

    return  template.render(replacements)

def show(n, q, k, args):
    hostname = args.node
    yaml_dir = args.yaml_dir
    fragment_dir = args.fragment_dir
    scenario = args.scenario

    print compose(hostname, yaml_dir, fragment_dir, scenario, build_metadata('./data', '2_role', 'config'))
