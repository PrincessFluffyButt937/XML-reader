def ref_key(ref):
    #creates key to for sorted()
    j = 0
    for i in range(0, len(ref)):
        if not ref[i].isdigit():
            j = i
        else:
            break
    key = ref[j:]
    while len(key) < 5:
        key = "0" + key
    return key

def ref_to_str(ref_set):
    #converts set of references to sorted string
    ref_list = sorted(list(ref_set), key=lambda ref: ref_key(ref))
    return str(ref_list).strip("[]").replace("'", "")


class Data:
    def __init__(self, sn=None, pb=None, rev=None, date=None, trace={}, file_path=set()):
        self.sn = sn
        self.pb = pb
        self.rev = rev
        self.date = date
        self.trace = trace
        self.file_path = file_path
        #ommit filepaths?

    def __repr__(self):
        trace_str = ""
        for hu in self.trace:
            trace_str = trace_str + f"HU: {hu} / {self.trace[hu]}\n"
        return f"SN: {self.sn}, PB: {self.pb} {self.rev}, Date: {self.date}\n" + trace_str

    def add_trace(self, hu, trace_obj):
        if not hu or not trace_obj:
            return
        if not self.trace:
            self.trace[hu] = trace_obj
        else:
            if hu in self.trace:
                self.trace[hu].update(trace_obj)
            else:
                self.trace[hu] = trace_obj
    
    def update(self, other):
        self.file_path.update(other.file_path)
    
    def to_text(self):
        text = f"Serial number: {self.sn}, Project: {self.pb} / {self.rev}, Time stamp: {self.date}\n"
        for hu in self.trace:
            text = text + f"HU: {hu} - {self.trace[hu]}\n"
        return text
    
    def origin(self):
        text = "Extracted from files:\n"
        for path in self.file_path:
            text = text + path + "\n"
        return text
        
    def to_text_complete(self):
        return self.to_text() + self.origin()


#when to use super()??
class Trace(Data):
    def __init__(self, ref=set(), pn=None, lc=None):
        self.ref = ref
        self.pn = pn
        self.lc = lc
    
    def __repr__(self):
        return f"PN: {self.pn} / Lot Code: {self.lc} / References: {ref_to_str(self.ref)}"
    
    def update(self, other):
        self.ref.update(other.ref)