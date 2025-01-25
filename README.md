I wrote this because my mmx node/farmer host often freezes up (every 36 - 72 hours).  Its a hardware issue that i cant fix and I don't want to spend any money on mmx farming (just yet).  This script is my solution.

this script monitors mmx logs.  When the harvester is disconnected from the node/farmer it sends telegram message of status.  it checks to see if the host is up. Then it attempts to powercycle the node/ farmer host to force reboot.  the powercycle is done with a tplink kasa outlet and home assistant intergration.


