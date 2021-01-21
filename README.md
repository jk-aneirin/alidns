# alidns
这个程序可以方便地操作阿里云的云解析资源 <br>
Help :
```
Aliyun DNS Record Update Tools.

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
```
该程序在“https://github.com/luoyeah/alidns” 的基础上加了一些功能，如disable DNS记录，添加了线路的相关配置。<br>
感谢luoyeah，如有侵权，请告知！
