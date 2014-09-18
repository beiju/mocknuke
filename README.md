mocknuke
========

A simulated nuclear reactor plant computer for RBE 2001 at WPI. Includes a console that mimics the field control system.

Usage
-----

* Clone the repository and `cd` into its directory
* In `bluetooth.py`, find the `connect` function and change the port (and baud rate if needed). Things like this are why this is pre-alpha software.
* Change the `bot` variable at the top of the `Packet` class to your bot's number.
* Start the console with `python main.py`

Commands
--------

Commands work like a primitive version of shell commands. The available commands are:

* `connect` (or `c`): (Re)establish a Bluetooth connection with the Arduino.
* `supply`: Set the availability of the supply tubes. See below for how to specify the tubes to modify.
* `storage`: Set the availability of the storage tubes. See below for how to specify the tubes to modify.
* `stop`: Send the stop packet. If a number is provided it will be the destination of the packet, otherwise the destination will be your bot.
* `resume` (or `res`): Send the resume packet. If a number is provided it will be the destination of the packet, otherwise the destination will be your bot.
* `ignore_hb` (or `ignorehb` or `ih`): Set whether MockNuke should print out every heartbeat packet it recieves. Accepts `yes`/`no` or `on`/`off`, or no input to toggle the setting.

Specifying Tubes
----------------

There are two syntaxes for specifying which tubes to modify, modeled after the *nix `chmod` utility. 

The "symbolic" syntax uses `+` and `-` to set a tube as available or unavailble using its number (from `0` to `3`). So `supply +0` marks the first supply tube as avilable, and `storage -3` marks the last storage tube as unavailable.

The "absolute" syntax uses a 4-digit binary number to specify the state of all the tubes at once. The tubes are listed in order with the first tube in the leftmost position. This is _not_ a bitmask where the `n`th digit controls the state of the `n`th tube. For example, `supply 0101` marks the first and third supply tubes as available and the other two unavailable.

Future
------

This project has the potential to become a generic terminal to imitate any bluetooth communication system, but its code needs a thorough restructuring before that is possible. It is also severely lacking in documentation. Future development is not guaranteed but contributions are welcome.

Support
-------

If you're a WPI student looking to use this project, especially but not exclusively for RBE 2001, I'd be very happy to answer any questions you have. I know the limitations of working in the RBE lab and I'd like to support anyone who's trying to make it better. You can contact me through Github or my WPI email (my username is `jwpryor`).
