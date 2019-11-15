import csv, re

edge_splitter = re.compile("\s+")

class HaplotigIterator():

    required_headers = set(["hid", "rid"])
    @staticmethod
    def validate_headers(headers):
        missing = HaplotigIterator.required_headers - set(headers)
        if missing:
            raise Exception("Missing required headers: {}".format(" ".join(missing)))

    def __init__(self, headers, in_fn, pos=0):
        self.validate_headers(headers)
        self.headers = headers
        self.in_f = open(in_fn, "r")
        self.dialect = csv.Sniffer().sniff(self.in_f.read(1024))
        self.in_f.seek(pos)
        hap = next(csv.DictReader([self.in_f.readline()], fieldnames=self.headers, dialect=self.dialect))
        if not bool(hap):
            raise("Failed to find first haplotype at poisition {}!".format(pos))
        self.previous_hap = {
            "hid": hap["hid"],
            "rids": set([hap["rid"]]),
            "file_pos": pos,
        }

    def __del__(self):
        if hasattr(self, "in_f"):
            self.in_f.close()

    def __iter__(self):
        return self

    def __next__(self):
        if not bool(self.previous_hap):
            raise StopIteration()

        current_hap = self.previous_hap
        self.previous_hap = None
        while True:
            file_pos = self.in_f.tell()
            line = self.in_f.readline()
            if not line:
                break

            hap = next(csv.DictReader([line], fieldnames=self.headers, dialect=self.dialect))
            if hap["hid"] != current_hap["hid"]:
                self.previous_hap = {
                    "hid": hap["hid"],
                    "rids": set([hap["rid"]]),
                    "file_pos": file_pos,
                }
                break
            else:
                current_hap["rids"].add(hap["rid"])

        if current_hap:
            return current_hap
        raise StopIteration()

#-- HaplotigIterator
