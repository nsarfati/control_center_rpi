import speedtest
import humanreadable as hr


class InternetSpeed:

    __config = None

    def __init__(self, config):
        self.__config = config

    def get_speed(self):
        speed_test = speedtest.Speedtest()

        speed_test.get_servers(self.__config['isp']['servers'])
        speed_test.get_best_server()
        speed_test.download(threads=self.__config['isp']['threads'])
        speed_test.upload(threads=self.__config['isp']['threads'], pre_allocate=False)
        result = speed_test.results.dict()

        return {
            'download_speed_mb': "{0:.2f} Mb/s ".format(hr.BitPerSecond("{} bps".format(result['download'])).mega_bps),
            'upload_speed_mb': "{0:.2f} Mb/s".format(hr.BitPerSecond("{} bps".format(result['upload'])).mega_bps),
            "ping_ms": "{0:.2f} ms".format(result['ping'])
        }
