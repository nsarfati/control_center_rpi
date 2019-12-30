from qnapstats import QNAPStats


class QnapSummary:
    __qnap = None

    def __init__(self, config):
        self.__qnap = QNAPStats(config['qnap']['ip'], config['qnap']['port'],
                                config['qnap']['user'], config['qnap']['pass'])

    def get_stats(self):
        system_status = self.__qnap.get_system_stats()
        hdd_health = self.__qnap.get_smart_disk_health()

        return {
            'temperature': {
                'cpu': system_status['cpu']['temp_c'],
                'hdd1': hdd_health['0:1']['temp_c'],
                'hdd2': hdd_health['0:2']['temp_c'],
                'system:': system_status['system']['temp_c']
            },
            'health': {
                'system': self.__qnap.get_system_health(),
                'hdd1': hdd_health['0:1']['health'],
                'hdd2': hdd_health['0:2']['health']
            },
            'usage': {
                'cpu': system_status['cpu']['usage_percent'],
                'memory': system_status['memory']['free'] / system_status['memory']['total'] * 100,
                'hdd': self.__calculate_hdd_usage(hdd_health, self.__qnap.get_volumes())
            }
        }

    def __calculate_hdd_usage(self, hdd_info, volumes):
        free_size = 0

        for v in volumes.values():
            free_size += v['free_size']

        return self.__convert_bytes_to_tb(free_size) / float(hdd_info['0:1']['capacity'].split(' ')[0]) * 100

    def __convert_bytes_to_tb(self, size):
        return size / 1024 / 1024 / 1024 / 1024;
