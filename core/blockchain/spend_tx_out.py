import sys

from bitcoin import SelectParams
from bitcoin.core import lx


# python can be wrote directly only if has it a result comparing to Java
param_1 = sys.argv[1]

if sys.version_info.major < 3:
    sys.stderr.write("Sorry, Python 3.x required by this example.\n")
    sys.exit(1)

SelectParams('mainnet')

# tx_id = lx('76a914f438720d15e2ce8e5b290c94f7cb987d7b227deb88ac')
tx_id = lx(param_1)
print(tx_id)
