#!/usr/bin/env python2.7

import subprocess
import cumulus.chassis
from ansible.module_utils.basic import *

def main():
    module = AnsibleModule(argument_spec=dict())

    # Get BGP neighbor information
    output = subprocess.check_output(["/usr/bin/net", "show", "bgp", "neighbor", "json"])
    neighInfo = json.loads(output)

    # Make sure we are running on a chassis
    try:
        chassis = cumulus.chassis.probe()
    except (ImportError, RuntimeError, AssertionError) as e:
        module.fail_json(changed=False, msg="Unable to determine chassis type: %s" % (e,))

    # Does each fabric port have an established BGP session?
    failIntfs = []
    for fabNum in xrange(chassis.GetNumFabIntfs()):
        fabIntf = "fp%d" % fabNum
        if neighInfo.get(fabIntf, {}).get("bgpState") != "Established":
            failIntfs.append(fabIntf)

    if failIntfs:
        module.fail_json(changed=False, msg="Fabric interfaces have not established BGP: " + " ".join(failIntfs))

    module.exit_json(changed=False, msg="BGP is established on all fabric interfaces")

if __name__ == '__main__':
    main()
