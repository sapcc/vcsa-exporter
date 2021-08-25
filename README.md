# vcsa-exporter

This is an exporter using [vCenter Server Appliance (Management) API](https://code.vmware.com/apis/60/vcenter-server-appliance-management) via REST. 
Idea is, to have different collectors for the different REST paths, since their output is very different (and therefore the parsing).

Current collectors:
* `vmon/service`: vCSA service health states.
* `logging/forwarding`: Checks the log forwarding to syslog hosts.

## Running the exporter

The exporter is supporting master password (mpw). If you aren't using it, you can specify a dedicated pw, which will take precedence. Let's give an example with a dedicated password:

```
python3 exporter.py -a vcenter.json  -o 9010 -u "username" -p "password"
```

You can use the given Dockerfile to build and use the docker container for an easy rampup

```
make
docker run -it vcsa-exporter:0.1 sh
```

We are using [atlas](https://github.com/sapcc/atlas) to have the `vcenter.json` served automatically; built from netbox. However, you can assemlbe the file on your own too:

```json
[
    {
        "targets": [
            "10.10.10.15"
        ],
        "labels": {
            "job": "vcenter",
            "metrics_label": "vcenter",
            "role": "virtual-appliance",
            "server_id": "1",
            "server_name": "some-vcenter.localdomain",
            "state": "Active"
        }
    }

]
```

## Adding a collector

A new collector has to go to `collectors/`. Respective API call goes to `rest.yaml`.
Maybe this is going to be supplemented by some endpoint discovery in future, feel free to add it if you love to have it.

Foo
