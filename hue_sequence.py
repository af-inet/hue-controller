#
# Performs a light show with the hue,
# synchronized to the beat of music picked up through the microphone.
#
import time
import random
import phue
import beat_tracker


def get_lights(bridge):
    """
    Returns a filtered list of lights from the bridge.
    """

    target_names = [
        "Console Lamp",
        "Bedroom Table Lamp",
        "Kitchen light",
    ]

    targets = [light for light in bridge.lights if light.name in target_names]

    if len(targets) != len(target_names):
        print("%s: not found ... %s" % (target_names, targets))
        exit(1)

    return targets


def random_temp():
    """
    Returns a random valid temperature value.
    """
    temp_min = 154
    temp_max = 500
    temp_interval = 1
    # `range`s are exclusive [min, max)
    return random.randrange(temp_min, temp_max + 1, temp_interval)


def main():
    """
    Synchronize the hue lights (while alternating their color / intensity) with the tempo of the music.
    """

    # connect to the hue bridge
    bridge = phue.Bridge()
    bridge.connect()  # throw an exception if connection was not established

    tracker = beat_tracker.BeatTracker()
    tracker.start()
    try:

        # obtain a list of lights to control
        lights = get_lights(bridge)

        x = 0
        ids = [l.light_id for l in lights]

        while True:

            time_between_beats = (60.0 / tracker.tempo)

            combos = [
                [1,     0],
                [1,   254],
                [1,     0],
                [500, 254],
            ]
            x = (x + 1) % 4

            temp, _brightness = combos[x]

            adjust = int(_brightness * (int(tracker.volume / 1500.0) * 2))

            if tracker.volume < 1000:
                adjust = 0

            brightness = int(min(adjust, 254))
            on = bool(tracker.volume > 800)
            command = {"ct": temp, "bri": brightness, "transitiontime": 1, "on": on}
            bridge.set_light(ids, command)

            if time_between_beats > 1:
                time.sleep(1)
            else:
                time.sleep(time_between_beats)

    finally:
        tracker.stop()


if __name__ == '__main__':
    main()