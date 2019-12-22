### About

This is an addon for [qToggleServer](https://github.com/qtoggle/qtoggleserver).

It provides Eqiva eQ-3 bluetooth thermostat support for qToggleServer.


### Install

Install using pip:

    pip install qtoggleserver-eq3bt


### Usage

##### `qtoggleserver.conf:`
``` javascript
...
ports = [
    ...
    {
        driver = "qtoggleserver.eq3bt.ports.Temperature"
        address = "00:1A:22:AA:BB:CC"
        peripheral_name = "livingroom"
    }
    {
        driver = "qtoggleserver.eq3bt.ports.Boost"
        address = "00:1A:22:AA:BB:CC"
        peripheral_name = "livingroom"
    }
    ...
]
...
```
