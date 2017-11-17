import json

class Input:
    def __init__(self):
        pass
    def readFromFile(self):
        with open('sample.json') as json_data:
            self.data_raw = json.load(json_data)

    def fromString(self, str_data):
        self.data_raw = json.loads(str_data)

    def processPredictData(self, str_data):
        data_raw = json.loads(str_data)
        print str_data + "data"
        print data_raw
        ip = self.encodeState(data_raw["state"], data_raw["player"])
        return ip

    def save_to_file(self, str_data):
        new_data_raw = json.loads(str_data)
        try:
            self.readFromFile()
        except:
            self.data_raw = []
            print "except called"

        with open('sample.json', 'wr') as json_data:
            data_to_write = self.data_raw + new_data_raw

            json.dump(data_to_write, json_data)

    def encodeState(self, state, current):
        encoded = []
        # for i in state :
        #     if i == '':
        #         encoded.append(1)
        #     elif i == current:
        #         encoded.append(2)
        #     else:
        #         encoded.append(3)

        for i in state :
            if i == '':
                encoded.append(1)
                encoded.append(0)
                encoded.append(0)
            elif i == current:
                encoded.append(0)
                encoded.append(1)
                encoded.append(0)
            else:
                encoded.append(0)
                encoded.append(0)
                encoded.append(1)
        return encoded
    def encodeOutput(self, move):
        output = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        output[move] = 1
        return output

    def processData(self):
        raw = self.data_raw
        if raw == None:
            print "raw data not found"
            return
        data = []
        for i in raw :
                item = {}
                item["input"] = self.encodeState(i["state"], i["player"])
                item["class"] = self.encodeOutput(i["move"])
                data.append(item)
        self.data = data
        print data
    def getData(self):
        x = []
        y = []
        for i in self.data:
            x.append(i["input"])
            y.append(i["class"])
        return (x, y)
