#
# First time setup, establishes a connection with hue bridge.
#
# https://github.com/studioimaginaire/phue
#
import os
import os.path
import json
import phue
import hue_bridge_scanner


HUE_CONFIG_PATH = os.path.join(os.getenv("HOME"), '.python_hue')


def connect_to_bridge():
    """
    Attempt to establish a connection with the hue bridge.
    """

    raw_input("press the button on your Hue Bridge before continuing... (press enter to continue)")

    host = hue_bridge_scanner.scan()

    print("discovered hue bridge at %s, connecting..." % host)

    b = phue.Bridge(host)
    b.connect()

    print("success! listing lights:")

    for light in b.lights:
        print("  %s" % light.name)


def configure():
    """
    Perform first time hue setup (using the phue library).
    This involves scanning the network for a hue bridge
    and registering with it. Configuration is saved to ~/.python_hue.
    """

    if os.path.exists(HUE_CONFIG_PATH):
        print("found phue config at: %s" % HUE_CONFIG_PATH)

        with open(HUE_CONFIG_PATH, "r") as fd:
            try:
                data = json.load(fd)

                if len(data.keys()) == 0:
                    print("no bridge found in config, running first-time setup...")
                    connect_to_bridge()

                elif len(data.keys()) == 1:
                    host = data.keys()[0]

                    print("found bridge in config: %s, attempting to connect..." % host)

                    b = phue.Bridge(host)
                    b.connect()

                    print("success! listing lights:")

                    for light in b.lights:
                        print("  %s" % light.name)

                else:
                    print("found multiple bridges in config! you'll need to fix this yourself %s" % data.keys())

            except ValueError:
                print("[!] %s contained invalid json; you might want to delete it and try again.\n\trm %s"
                      % (HUE_CONFIG_PATH, HUE_CONFIG_PATH))
                exit(1)
    else:
        print("no phue config found at '%s' running first-time setup..." % HUE_CONFIG_PATH)
        connect_to_bridge()


if __name__ == '__main__':
    configure()
