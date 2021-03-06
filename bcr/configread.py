import sys
import re
from WorkloadObj import WorkloadObj
from FailureObj import FailureObj

class configread:
    def __init__(self,inp):
        input_file = inp
        self.workload = dict()
        self.host = dict()
        self.client_host = dict()
        self.replica_host = dict()
        self.failure = dict()
        with open(input_file) as f:
            for line in f:
                if line[0] != '#':
                    (key, sep, val) = line.partition('=')
                    key = key.strip()
                    # if the line does not contain '=',
                    # it is invalid and hence ignored
                    if len(sep) != 0:
                        val = val.strip()
                        if line.startswith('test_case_name'):
                            self.test_case_name = val
                        elif line.startswith('t'):
                            self.failure_num = int(val)
                        elif line.startswith('num_client'):
                            self.num_client = int(val)
                        elif line.startswith('client_timeout'):
                            self.client_timeout = int(val)
                        elif line.startswith('head_timeout'):
                            self.head_timeout = int(val)
                        elif line.startswith('nonhead_timeout'):
                            self.nonhead_timeout = int(val)
                        elif line.startswith('hosts'):
                            pattern = re.split(';', val)
                            pattern = [int(x.strip()) for x in pattern]
                            i = 0
                            for x in pattern:
                                self.host[i] = x
                                i = i+1
                        elif line.startswith('client_hosts'):
                            pattern = re.split(';', val)
                            pattern = [int(x.strip()) for x in pattern]
                            i = 0
                            for x in pattern:
                                self.client_host[i] = x
                                i = i+1
                        elif line.startswith('replica_hosts'):
                            pattern = re.split(';', val)
                            pattern = [int(x.strip()) for x in pattern]
                            i = 0
                            for x in pattern:
                                self.replica_host[i] = x
                                i = i+1
                        elif line.startswith('workload'):
                            i = int(re.search(r'\d+', key).group())
                            self.workload[i] = []
                            pattern = re.split(';', val)
                            pattern = [x.strip() for x in pattern]
                            for x in pattern:
                                x = x.replace(")","")
                                x = x.replace("'","")
                                x = x.replace("(", ",")
                                object = re.split(',', x)
                                y = WorkloadObj(object)
                                self.workload[i].append(y)
                        elif line.startswith('failures'):
                            number = re.findall(r'\d+', key)
                            i = int(number[0])
                            j = int(number[1])
                            pattern = re.split(';', val)
                            pattern = [x.strip() for x in pattern]
                            self.failure[(i,j)] = []
                            for x in pattern:
                                number = re.findall(r'\d+', x)
                                client = int(number[0])
                                req = int(number[1])
                                x = x.replace(")","")
                                x = x.replace("(", ",")
                                y = re.split(',',x)
                                cond = y[0].strip()
                                action = y[3].strip()
                                f = FailureObj(cond,client,req,action)
                                self.failure[(i,j)].append(f)
