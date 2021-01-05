import random


class ProxiesMiddleware:

    def process_request(self, request, spider):
        if random.getrandbits(1):
            request.meta['proxy'] = 'https://159.75.19.163:10086'
