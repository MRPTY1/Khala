import random


class V2rayNMiddleware:

    def process_request(self, request, spider):
        request.meta['proxy'] = 'https://127.0.0.1:10809'
