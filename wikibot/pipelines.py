import time
from scrapy.exceptions import DropItem, CloseSpider
from engine.index import Index


class WikiPipeline(object):
    documents = {}

    def __init__(self):
        self.start_time = 0
        self.n = 0
        self.k = 0
        self.filename = ""
        self.svd = True

    def process_item(self, item, spider):
        if len(self.documents) < self.n:
            if item["url"] in self.documents:
                raise DropItem("Duplicate item found: %s" % item["url"])
            else:
                self.documents[item["url"]] = item
        else:
            spider.close_down = True

    def open_spider(self, spider):
        print("Web crawling...")
        self.start_time = time.time()

        self.n = spider.n
        self.k = spider.k
        self.filename = spider.filename
        self.svd = spider.svd

    def close_spider(self, spider):
        print("--- %s seconds ---" % (time.time() - self.start_time))

        print("")

        print("Indexing...")
        index = Index(self.documents, self.filename)

        print("")

        print("Creating dictionary...")
        st = time.time()
        index.init_dictionary()
        print("--- %s seconds ---" % (time.time() - st))

        print("")

        print("Creating index...")
        st = time.time()
        index.create_index()
        print("--- %s seconds ---" % (time.time() - st))

        print("")

        print("IDF parsing...")
        st = time.time()
        index.idf()
        print("--- %s seconds ---" % (time.time() - st))

        print("")

        if self.svd:
            print("Delete noise...")
            st = time.time()
            index.delete_noise(self.k)
            print("--- %s seconds ---" % (time.time() - st))

            print("")

        print("Normalizing...")
        st = time.time()
        index.normalize()
        print("--- %s seconds ---" % (time.time() - st))

        print("")

        print("Saving to file...")
        st = time.time()
        index.save()
        print("--- %s seconds ---" % (time.time() - st))

        print("")

        print("Documents: %d" % len(self.documents))
        print("Words in dictionary: %d" % len(index.dictionary))
        print("--- %s seconds ---" % (time.time() - self.start_time))

