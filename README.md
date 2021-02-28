# dnsmasq-leases-ui

This tool provides a web based ui for leases file of the famous DNS/DHCP daemon [dnsmasq](http://thekelleys.org.uk/dnsmasq/doc.html).

# How to run

## Standalone

After cloning the repository run `python dnsmasq-leases-ui.py`

## Docker

```
docker run -d \
        --name pispot-web-ui \
        -p 80:5000 \
        -e "DOCKER_HOST=$(ip -4 a show wlan0 | grep -Po 'inet \K[\d.]+')" \
        -v /var/lib/misc/dnsmasq.leases:/var/lib/misc/dnsmasq.leases:ro  \
        --name dnsmasq-leases-ui \
        --restart unless-stopped \
        dnsmasq-leases-ui:latest
```

# How to use

For both variants there are two options to access it:
* Human readable HTML: `http://<hostname or ip>:80`
* JSON Representation: `http://<hostname or ip>:80/api` 
* JSON Representation (speed): `http://<hostname or ip>:80/api/speed` 

# Credits

Dockerfile by https://github.com/xakraz
