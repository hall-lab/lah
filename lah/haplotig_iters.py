import csv, re

edge_splitter = re.compile("\s+")

class HaplotigIterator():

    required_headers = set(["rg_id", "rid"])
    @staticmethod
    def validate_headers(headers):
        missing = HaplotigIterator.required_headers - set(headers)
        if missing:
            raise Exception("Missing required headers: {}".format(" ".join(missing)))

    def __init__(self, headers, in_fn):
        self.validate_headers(headers)
        self.in_f = open(in_fn, "r")
        dialect = csv.Sniffer().sniff(self.in_f.read(1024))
        self.in_f.seek(0)
        self.reader = csv.DictReader(self.in_f, fieldnames=headers, dialect=dialect)
        self.prev = next(self.reader)

    def __del__(self):
        if hasattr(self, "in_f"):
            self.in_f.close()

    def __iter__(self):
        return self

    def __next__(self):
        if not self.prev:
            raise StopIteration()

        rg_id = self.prev["rg_id"]
        rids = [self.prev["rid"]]
        self.prev = None
        while True:
            try:
                rg = next(self.reader)
            except StopIteration: # EOF
                break
            if rg["rg_id"] != rg_id: # save read group, break to return haplotig
                self.prev = rg
                break
            else:
                rids.append(rg["rid"])

        if len(rids) > 0:
            rids.sort()
            return {"rg_id": rg_id, "rids": rids}
        else:
            raise StopIteration()

#-- HaplotigIterator
