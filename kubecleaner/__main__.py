""" Kubernetes cleaner.

Usage:
  kubecleaner [-n <namespace>] [--dry] jobs <name>

Commands:
  jobs  Delete completed jobs

Global options:
  -h --help     Show this screen.
  -n NAMESPACE  K8S namespace [default: default]
  --dry         Run without deletion
"""

import logging

from docopt import docopt
import kubernetes

from kubecleaner.jobs import cleanup_jobs

logger = logging.getLogger('kubecleaner')


def setup():
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('kubernetes.client.rest').setLevel(logging.INFO)

    try:
        kubernetes.config.load_incluster_config()
    except kubernetes.config.config_exception.ConfigException:
        kubernetes.config.load_kube_config()


def main():
    args = docopt(__doc__)
    setup()

    if args['jobs']:
        cleanup_jobs(namespace=args['-n'],
                     name=args['<name>'],
                     dry=args['--dry'])

if __name__ == '__main__':
    main()
