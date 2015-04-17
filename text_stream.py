import json, re

class TextStream(object):
    def __init__(self, filePaths):
        self.filePaths = filePaths
        self.curItemIdx = 0

    def open_next_file(self):
        if len(self.filePaths) == 0:
            self.curFile = None
            return

        next_path = self.filePaths.pop(0)
        print next_path
        self.curFile = open(next_path)

    def __iter__(self):
        return self

    def get_next_item(self):
        pass

    def next(self):
        next_item = self.get_next_item()
        if next_item is None:
            raise StopIteration

        return next_item

class JsonStream(TextStream):
    def __init__(self, filePaths):
        super(JsonStream, self).__init__(filePaths)
        self.curItems = []

    def get_next_item(self):
        if isinstance(self.curItems, dict):
            cur_item = self.curItems
            self.open_next_file()
            if self.curFile is not None:
                self.curItems = json.load(self.curFile)
            else:
                return None

        if isinstance(self.curItems, list):
            if self.curItemIdx >= len(self.curItems):
                self.open_next_file()
                if self.curFile is not None:
                    self.curItems = json.load(self.curFile)
                    self.curItemIdx = 0

                    return self.get_next_item()
                else:
                    return None
            cur_item = self.curItems[self.curItemIdx]
            self.curItemIdx += 1


        cur_text = cur_item['text'].encode('ascii', errors='ignore').replace('\\n', ' ')
        scrubbed_text = cur_text.lower().split(' ')
        return scrubbed_text
