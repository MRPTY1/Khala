from io import BytesIO
from warcio import WARCWriter, StatusAndHeaders


class WarcWriterPipeline:

    def open_spider(self, spider):
        self.output = open(f'D:/{spider.name}.warc.gz', 'wb')

    def close_spider(self, spider):
        self.output.close()

    def process_item(self, item, spider):
        writer = WARCWriter(self.output, gzip=True)
        headers_list = item['headers']

        http_headers = StatusAndHeaders('200 OK', headers_list, protocol='HTTP/1.0')

        record = writer.create_warc_record(item['url'], 'response',
                                           payload=BytesIO(item['content']),
                                           http_headers=http_headers)

        writer.write_record(record)
        return item
