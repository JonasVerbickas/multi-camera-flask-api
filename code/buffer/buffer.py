class Buffer:
    def __init__(self, size):
        self.size = size
        self.buffer = []

    def add(self, to_add):
        if len(self.buffer) < self.size:
            self.buffer.insert(0, to_add)
        else:
            curr_item = to_add
            for i in range(self.size):
                next_item = self.buffer[i]
                self.buffer[i] = curr_item
                curr_item = next_item

    def get(self, index):
        return self.buffer[index]

    def getList(self):
        return self.buffer
