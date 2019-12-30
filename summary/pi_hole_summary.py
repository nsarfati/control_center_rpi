from mac_vendor_lookup import MacLookup
from getmac import get_mac_address

import pihole


class PiHoleSummary:

    __mac_vendors = None

    def __init__(self, config):
        self.__ph = pihole.PiHole(config['pi-hole']['ip'])
        self.__ph.authenticate(config['pi-hole']['pass'])
        self.__ph.refresh()
        self.__mac_vendors = MacLookup()
        self.__mac_vendors.loop.run_until_complete(self.__mac_vendors.async_lookup.load_vendors())

    def get_stats(self):
        return {
            "status": self.__ph.status,
            "blocked_ads_percentage": float(self.__ph.ads_percentage),
            "total_blocked": int(self.__ph.blocked.replace(',', '')),
            "total_queries": int(self.__ph.total_queries.replace(',', '')),
            "top_devices": self.__get_device_manufacturers(self.__ph.top_devices)
        }

    def __get_device_manufacturers(self, devices):
        vendors = []

        for d in devices.keys():
            ip_addr = d.split('|')[-1]
            mac_addr = get_mac_address(ip=ip_addr)
            v = ip_addr

            try:
                v = self.__mac_vendors.lookup(mac_addr)[0:8]
            except Exception as e:
                pass

            vendors.append(v)

        return vendors
