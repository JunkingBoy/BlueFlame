class CaseDbTemplate:
    def __init__(self, **data):
        self.pid = data['pid']
        self.uid = data['uid']
        self.case_type = data['case_type']
        self.case_detail = data['case_detail']
        self.case_row_hash = data['case_row_hash']
