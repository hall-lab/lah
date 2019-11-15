import csv, re

edge_splitter = re.compile("\s+")

class HaplotigIterator():

    required_headers = set(["hid", "rid"])
    @staticmethod
    def validate_headers(headers):
        missing = HaplotigIterator.required_headers - set(headers)
        if missing:
            raise Exception("Missing required headers: {}".format(" ".join(missing)))

    def __init__(self, headers, in_fn):
        self.validate_headers(headers)
        self.headers = headers
        self.in_f = open(in_fn, "r")
        self.dialect = csv.Sniffer().sniff(self.in_f.read(1024))
        self.in_f.seek(0)
        self.prev = next(csv.DictReader([self.in_f.readline()], fieldnames=self.headers, dialect=self.dialect))
        self.prev["file_pos"] = 0

    def __del__(self):
        if hasattr(self, "in_f"):
            self.in_f.close()

    def __iter__(self):
        return self

    def __next__(self):
        if not self.prev:
            raise StopIteration()

        hid = self.prev["hid"]
        file_pos = self.prev["file_pos"]
        rids = set([self.prev["rid"]])
        self.prev = None
        while True:
            line = self.in_f.readline()
            if not line:
                break

            hap = next(csv.DictReader([line], fieldnames=self.headers, dialect=self.dialect))
            if hap["hid"] != hid:
                hap["file_pos"] = self.in_f.tell()
                self.prev = hap
                break
            else:
                rids.add(hap["rid"])

        if len(rids) > 0:
            return {"hid": hid, "file_pos": file_pos, "rids": rids}
        else:
            raise StopIteration()

#-- HaplotigIterator
