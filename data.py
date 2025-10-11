

class Data:
    def __init__(self, sn=None, pb=None, rev=None, err=None, date=None, trace={}, file_path=[]):
        self.sn = sn
        self.pb = pb
        self.rev = rev
        self.err = err
        self.date = date
        self.trace = trace
        self.file_path = file_path

    def __repr__(self):
        trace_str = ""
        for hu in self.trace:
            trace_str = trace_str + f"HU: {hu} / {self.trace[hu]}\n"
        return f"SN: {self.sn}, PB: {self.pb} {self.rev}, Date: {self.date}, / Error: {self.err}, File: {self.file_path}\n" + trace_str

    #test
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
        self.file_path.extend(other.file_path)

    def add_error(self, error):
        if self.err:
            self.err = self.err + " / " + error
        else:
            self.err = error
    
    def to_text(self):
        text = f"Serial number: {self.sn}, Project: {self.pb} / {self.rev}, Time stamp: {self.date}\n"
        for hu in self.trace:
            text = text + f"HU: {hu} - {self.trace[hu]}\n"
        text = text + "Extracted from files:\n"
        for path in self.file_path:
            text = text + path + "\n"
        return text


#when to use super()??
class Trace(Data):
    def __init__(self, ref=set(), pn=None, lc=None):
        self.ref = ref
        self.pn = pn
        self.lc = lc
    
    def __repr__(self):
        from functions import ref_to_str
        return f"PN: {self.pn} / Lot Code: {self.lc} / References: {ref_to_str(self.ref)}"
    
    def update(self, other):
        self.ref.update(other.ref)