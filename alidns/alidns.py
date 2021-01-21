#!/usr/bin/env python

'''Aliyun DNS Record Update Tools.

Usage:
 alidns config  <key> <key-secret> <domain>
 alidns clean
 alidns list
 alidns add     [-r=<record>] [-v=<ip>] [-t=<type>] [--ttl=<ttl>] [-l=<line>]
 alidns delete  [-r=<record>] [-v=<ip>] [-t=<type>] [-l=<line>]
 alidns status  [-r=<record>] [-t=<type>] [-l=<line>] [-s=<status>]

Commands:
 config         Config Key key-secret and domain.
 clean          Clean config.
 list           List all DNS records.
 add            Add DNS record.
 delete         Delete DNS record.
 status         Disable or enable DNS record.

Arguments:
 -r=<record>                                   Host record.
 -v=<ip>                                       Host ip.
 -t=<type>                                     Record type.
 --ttl=<ttl>                                   Record ttl.
 -s=<disable|enable>                           Record status.
 -l=<default|mobile|unicom|telecom|oversea>    DNS effective line.

Examples:
 alidns config 12341234 12341234 forks.club
 alidns add -r www -v 127.0.0.1 -t A --ttl 600 -l telecom
 alidns status -r www -s disable
'''

from docopt import docopt
import json
import os
import sys

from aliyunsdkcore import client
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest \
        import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DeleteDomainRecordRequest \
        import DeleteDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest \
        import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest \
        import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109.SetDomainRecordStatusRequest \
        import SetDomainRecordStatusRequest


class Alidns(object):
    def __init__(self, key, key_secret, domain):
        '''init'''
        self.__domain = domain
        self.__bs = client.AcsClient(key, key_secret, 'cn-hangzhou')
        self.__print = ''
        self.__records = self.query()

    def query(self):
        '''Query all dns records.'''
        req = DescribeDomainRecordsRequest()
        req.set_accept_format('json')
        req.set_DomainName(self.__domain)
        js = json.loads(self.__bs.do_action_with_exception(req).decode())
        ret = {}
        strs = ''
        for x in js['DomainRecords']['Record']:
            RR = x['RR']
            Type = x['Type']
            Value = x['Value']
            RecordId = x['RecordId']
            TTL = x['TTL']
            Line = x['Line']
            Status = x['Status']
            strs = strs + '[*]%8s.%s -> %-16s;  %-8s;%-8s;%d;%-8s\n' % \
                          (RR, self.__domain, Value, Type, Line, TTL, Status)
            ret[RecordId] = [RR, Value, Type, TTL, Line]
        self.__print = strs
        return ret

    def list(self, update=True):
        '''Print query results.'''
        if update:
            self.query()
        print(self.__print)

    def __update_record(self, record_id, record, value,
                        record_type, ttl, line):
        '''Update record.'''
        req = UpdateDomainRecordRequest()
        req.set_RecordId(record_id)
        req.set_accept_format('json')
        req.set_RR(record)
        req.set_Type(record_type)
        req.set_TTL(ttl)
        req.set_Line(line)
        req.set_Value(value)
        self.__bs.do_action_with_exception(req)
        print('[+]%s.%s -> %s;%s;%d' % (record, self.__domain, value,
                                        record_type, ttl))

    def __add_record(self, record, value, record_type, ttl, line):
        '''Add record.'''
        req = AddDomainRecordRequest()
        req.set_accept_format('json')

        req.set_DomainName(self.__domain)
        req.set_RR(record)
        req.set_Type(record_type)
        req.set_TTL(ttl)
        req.set_Line(line)
        req.set_Value(value)
        self.__bs.do_action_with_exception(req)
        print('[+]%8s.%s -> %-16s;  %-8s;%s;%s' %
              (record, self.__domain, value, record_type, ttl, line))

    def __get_record_id(self, record, record_type, line):
        '''Get record id'''
        if not record_type:
            record_type = "A"
        if not line:
            line = "default"

        req = DescribeDomainRecordsRequest()
        req.set_accept_format('json')
        req.set_DomainName(self.__domain)
        req.set_RRKeyWord(record)
        req.set_SearchMode("advanced")
        req.set_Type(record_type)
        req.set_Line(line)
        js = json.loads(self.__bs.do_action_with_exception(req).decode())
        if len(js['DomainRecords']['Record']) == 0:
            return ''
        return js['DomainRecords']['Record'][0]['RecordId']

    def __is_exist(self, record, record_type, line):
        '''Record exist?'''
        record_id = self.__get_record_id(record, record_type, line)
        if not record_id:
            return False
        for i in self.__records:
            if record_id == i:
                return True
        return False

    def add(self, record, value, record_type, ttl, line):
        '''Add record'''
        if not value:
            print("Please input value")
            sys.exit()
        if not record:
            print("Please input record")
            sys.exit()
        if not line:
            line = 'default'

        if self.__is_exist(record, record_type, line):
            record_id = self.__get_record_id(record, record_type, line)
            if not record_type:
                record_type = self.__records[record_id][2]
            if not ttl:
                ttl = self.__records[record_id][3]
            else:
                ttl = int(ttl)

            if self.__records[record_id][1] != value:
                self.__update_record(record_id, record, value,
                                     record_type, ttl, line)
            elif self.__records[record_id][3] != ttl:
                self.__update_record(record_id, record, value,
                                     record_type, ttl, line)
            else:
                pass
        else:
            if not record_type:
                record_type = 'A'
            if not ttl:
                ttl = 600

            self.__add_record(record, value, record_type, ttl, line)
        self.list()

    def __delete_record(self, record_id):
        '''delete record'''
        req = DeleteDomainRecordRequest()
        req.set_RecordId(record_id)
        self.__bs.do_action_with_exception(req)

    def __update_record_status(self, record, record_id, status):
        '''Update record.'''
        req = SetDomainRecordStatusRequest()
        req.set_accept_format('json')
        req.set_RecordId(record_id)
        req.set_Status(status)
        self.__bs.do_action_with_exception(req)

        if status == "disable":
            print('[x]%s.%s has been disabled' % (record, self.__domain))
        else:
            print('[]%s.%s has been enabled' % (record, self.__domain))

    def update_record_status(self, record, record_type, line, status):
        if not record:
            print("Please input record")
            sys.exit()
        if not status:
            print("Please input status")
            sys.exit()
        if not line:
            line = 'default'
        if not record_type:
            record_type = 'A'
        if not self.__is_exist(record, record_type, line):
            print('[!]%s.%s is not existed' % (record, self.__domain))
            sys.exit()
        else:
            record_id = self.__get_record_id(record, record_type, line)
            self.__update_record_status(record, record_id, status)

    def delete(self, record, record_type, line):
        '''Delete record'''
        if not record:
            print("Please input record")
            sys.exit()
        if not line:
            line = 'default'
        if not record_type:
            record_type = 'A'

        if self.__is_exist(record, record_type, line):
            record_id = self.__get_record_id(record, record_type, line)
            self.__delete_record(record_id)
            print('[-]%s.%s has been deleted' % (record, self.__domain))
        else:
            print('[!]%s.%s is not existed' % (record, self.__domain))
        self.list()


def main():
    '''Parse arguments with docopt.'''
    args = docopt(__doc__)
    if args['config']:
        with open(get_credential_file(), 'w') as f:
            f.write('{} {} {}'.format(args['<key>'],
                    args['<key-secret>'], args['<domain>']))
        Alidns(args['<key>'], args['<key-secret>'], args['<domain>']).list()
    elif args['clean']:
        os.remove(get_credential_file())
    else:
        if os.path.exists(get_credential_file()):
            key = ''
            key_secret = ''
            domain = ''
            with open(get_credential_file(), 'r') as f:
                s = f.read().split()
                key = s[0]
                key_secret = s[1]
                domain = s[2]
            ali = Alidns(key, key_secret, domain)
            if args['list']:
                ali.list()
            elif args['add']:
                ali.add(args['-r'], args['-v'], args['-t'],
                        args['--ttl'], args['-l'])
            elif args['delete']:
                ali.delete(args['-r'], args['-t'], args['-l'])
            elif args['status']:
                ali.update_record_status(args['-r'], args['-t'],
                                         args['-l'], args['-s'])
            else:
                print(__doc__)
        else:
            print('[!]Need config,use [alidns config] command.')


def get_credential_file():
    """Get credential file path."""
    parent = None
    parent = os.environ['HOME'] + '/.alidns/'
    if not os.path.isdir(parent):
        os.mkdir(parent)
    return parent + 'alidns'


if __name__ == '__main__':
    main()
