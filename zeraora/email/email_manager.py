__all__ = [
    'check_path', 'get_table_data', 'decode_match', 'decode_field',
    'TencentMailReceiveService', 'TencentMailSendService', 'EmailManager'
]

import re
import os
import csv
import imaplib
import smtplib
import email.parser
import warnings
import platform
from typing import Any, Union
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import decode_header, Header


def check_path(folder_path: str, filename: str = None, exist_check: bool = True, error_info: str = None) -> str:
    """检查路径
    可指定是否检查存在性，可自定义错误信息

    Args:
        folder_path:    字符串类型 -> 文件夹路径，不包含文件名 -> 必需
        filename:       字符串类型 -> 文件名，非绝对路径 -> 非必需
        exist_check:    布尔值类型 -> 是否进行存在检查 -> 非必需，默认开启检查
        error_info:     字符串类型 -> 自定义错误信息 -> 非必需
    Returns:
        path: str: 路径
    """

    from pathlib import Path
    # 要求检查存在性，并存在文件名
    if exist_check and filename:
        if not os.path.exists(Path(folder_path).joinpath(filename)):
            base_error_info = "{} 文件不存在，请检查，或仅需拼凑路径，可设置 exist_check 为False。{}"
            if error_info:
                error_info = base_error_info.format(filename, f"自定义错误信息:{error_info}")
                raise FileNotFoundError(error_info)
            else:
                raise FileNotFoundError(base_error_info.format(filename))
        else:
            return str(Path(folder_path).joinpath(filename))

    # 要求检查存在性，不存在文件名
    elif exist_check and not filename:
        if not os.path.exists(Path(folder_path)):
            base_error_info = "{} 文件夹不存在，请检查路径，或者仅需要拼凑路径的情况下，可指定 exist_check 为False。{}"
            if error_info:
                error_info = base_error_info.format(folder_path, f"自定义错误信息:{error_info}")
                raise FileNotFoundError(error_info)
            else:
                raise FileNotFoundError(base_error_info.format(folder_path))
        else:
            return str(Path(folder_path))
    # 不要求检查存在性，并存在文件名
    elif not exist_check and filename:
        if folder_path[-1] != "\\" or folder_path[-1] != "/":
            if platform.system().lower() == 'windows':
                folder_path += "\\"
            if platform.system().lower() == 'linux':
                folder_path += "/"
            return folder_path + filename
    # 不要求检查存在性，不存在文件名
    else:
        if folder_path[-1] != "\\" or folder_path[-1] != "/":
            if platform.system().lower() == 'windows':
                folder_path += "\\"
            if platform.system().lower() == 'linux':
                folder_path += "/"
            return folder_path


def get_table_data(table) -> (list, list):
    """获取表格数据
    将会获取到表格头部与表格内容

    Args:
        table: bs4表格标签迭代器类型 -> 包含表格所有信息

    Returns:
        headers:    列表类型 -> 表格头部信息
        rows:       列表类型 -> 表格所有行内容
    """
    # 获取表格头部
    headers = [th.text.strip() for th in table.find("tr").find_all("th")]
    # 获取表格内容
    rows = []
    # 遍历表格内容
    for tr in table.find_all("tr"):
        cells = []
        tds = tr.find_all("td")
        if len(tds) == 0:
            # 跳过空行
            continue
        elif len(tds) > 0:
            # 获取行内容
            [cells.append(td.text.strip()) for td in tds if td.text.strip()]
            rows.append(cells)
    return headers, list(filter(None, rows))


def decode_match(match: re.Match) -> str:
    """16进制编码解码

    Args:
        match: 字节类型 -> 匹配信息 -> 必需
    Returns:
        decode_result: 字符串类型 -> 解码结果
    """
    encoded_s = match.group()
    byte_values = []
    for i in range(0, len(encoded_s), 2):
        if not re.match(rb'\\x[a-fA-F0-9]{2}', encoded_s[i:i + 2]):
            # 当匹配到的内容不为16进制编码时，直接返回原值
            return match.group()
        # 由于为字符串类型，因此需要做16进制转换
        byte_values.append(int(encoded_s[i:i + 2], 16))
    return bytes(byte_values).decode('gb18030')


def decode_field(infos: Union[Header, str], default: str = "null", charset: str = None) -> str:
    """检查字段

    Args:
        infos:      标头值字符串类型 -> 信息集合，集合中第一个参数为头部信息，即要解码的信息，第二个参数为编码，存在为空，或未知的可能性 -> 必需
        default:    字符串类型 -> 默认返回信息，若无法进行解码，可选择自定义信息返回 -> 非必需
        charset:    字符串类型 -> 编码格式，由于infos中并非一定能获得编码格式，可自行添加默认解码格式 -> 非必需
    Returns
        decode_result: 字符串类型 -> 解码信息
    """
    info = ""
    if infos:
        # 返回格式为 (decoded_string, charset) 的数据对序列
        infos = decode_header(infos)
        # 当列表大于1时，存在多个集合
        if len(infos) > 1:
            for i in infos:
                # 判断是否为字节类型
                if i and isinstance(i[0], bytes):
                    info_i, code_i = i[0], i[1]
                    if not code_i:
                        if charset:
                            info += info_i.decode(charset)
                        else:
                            info += info_i.decode("gb18030")
                    elif code_i and code_i != "unknown-8bit":
                        info += info_i.decode(code_i)
                    else:
                        if charset:
                            info += info_i.decode(charset)
                        else:
                            info += info_i.decode("gb18030")
                else:
                    info += i[0]
            return info
        elif len(infos) == 1:
            if isinstance(infos[0][0], bytes):
                info, code = infos[0][0], infos[0][1]
                if not code:
                    if charset:
                        return info.decode(charset)
                    else:
                        return info.decode("gb18030")
                elif code and code != "unknown-8bit":
                    return info.decode(code)
                else:
                    if charset:
                        return info.decode(charset)
                    else:
                        return info.decode("gb18030")
            else:
                return str(infos[0][0])
    else:
        return default


class TencentMailReceiveService:
    """腾讯 IMAP 邮箱接收服务

    Args:
        imap: IMAP4类 -> 邮箱接收客户端 -> 必需
    """

    def __init__(self, imap: imaplib.IMAP4):
        self.imap = imap
        self.all_mail = None

    def get_email_amount(self):
        """获取邮件数量

        Args: None

        Returns:
            email_amount: 整数类型 -> 邮件总数
        """
        self.imap.select()
        status, email_list = self.imap.search(None, 'ALL')
        assert status == "OK", "获取邮件数量失败"
        email_list = email_list[0].split()
        return len(email_list)

    def get_all_mail(
            self,
            email_file_down_path: str = None,
            down_appendix: bool = False,
            email_info_table_save: bool = False
    ) -> dict:
        """获取所有邮件

        Args:
            email_file_down_path:   字符串类型 -> 邮箱文件保存路径,不包含文件名 -> 非必需
            down_appendix:          布尔值类型 -> 是否下载附件 -> 非必需
            email_info_table_save:  布尔值类型 -> 是否下载信息中的表格 -> 非必需

        Returns:
            mail_info: 字典类型 -> 邮件信息字典
        """
        from tqdm import tqdm
        from bs4 import BeautifulSoup
        from zeraora.constants.times import Months, Weeks, TimeZones
        email_amount = self.get_email_amount()
        mail_info = {
            x + 1: {"Subject": "", "From": "", "To": "", "Date": "", "Date_Detail": "", "Body": "", "Appendix": Any}
            for x in range(email_amount)}
        for i in tqdm(range(1, email_amount + 1)):
            status, email_content = self.imap.fetch(str(i), '(RFC822)')
            assert status == "OK", f"获取第{i}封邮件失败"
            for response_part in email_content:
                if isinstance(response_part, tuple):
                    # 解析邮件内容
                    email_parser = email.parser.BytesFeedParser()
                    email_parser.feed(response_part[1])
                    msg = email_parser.close()
                    if "<" in decode_field(msg["From"]) and ">" in decode_field(msg["From"]):
                        from_info = decode_field(msg["From"])
                        from_name = from_info[0:-1].split("<")[0].replace('"', '')
                        from_email = from_info[0:-1].split("<")[1]
                    else:
                        from_info = decode_field(msg["From"])
                        from_name = None
                        from_email = from_info.replace("<", "").replace(">", "")
                    to_info = decode_field(msg["To"])
                    subject_info = decode_field(msg["Subject"], "无主题")
                    _date_info = datetime.strptime(msg["Date"].split(" (")[0], '%a, %d %b %Y %H:%M:%S %z') \
                        if "(" in msg["Date"] and ")" in msg["Date"] \
                        else datetime.strptime(msg["Date"], '%a, %d %b %Y %H:%M:%S %z')
                    week = Weeks[_date_info.strftime("%A")]
                    month = Months[_date_info.strftime("%B")]
                    time_zone = TimeZones(_date_info.strftime("%z")).description
                    date_info = _date_info.strftime(f'%Y%m%d%H%M%S')
                    date_detail_info = _date_info.strftime(f'%Y年{month}%d日{week} %H点%M分%S秒 时区: %z {time_zone}')
                    body_info = "null"
                    appendix_info = "null"
                    if not msg.is_multipart():
                        content_type = msg.get_content_type()
                        if content_type == 'text/html':
                            with warnings.catch_warnings(record=True) as w:
                                warnings.simplefilter("always")
                                try:
                                    decoded = re.sub(
                                        rb'\\x[a-fA-F0-9]{2}',
                                        decode_match,
                                        msg.get_payload(decode=True)
                                    ).decode("gb18030")
                                except ValueError:
                                    decoded = re.sub(
                                        rb'\\x[a-fA-F0-9]{2}',
                                        decode_match,
                                        msg.get_payload(decode=True)
                                    ).decode("utf-8", errors="ignore")
                                body_match = re.sub(' +', ' ', BeautifulSoup(decoded, 'lxml').get_text(" ", strip=True))
                                body_info = re.sub('\n+', '\n', body_match)
                                if w and issubclass(w[-1].category, UserWarning) \
                                        and "MarkupResemblesLocatorWarning" in str(w[-1].message):
                                    body_match = re.sub(' +', ' ', BeautifulSoup(
                                        decoded, 'html.parser').get_text(" ", strip=True))
                                    body_info = re.sub('\n+', '\n', body_match)
                            if not body_info or body_info == (from_name + from_email if from_name else from_email):
                                body_info = "null"

                    else:
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if content_type == 'text/html':
                                with warnings.catch_warnings(record=True) as w:
                                    warnings.simplefilter("always")
                                    body_match = re.sub(' +', ' ', BeautifulSoup(part.get_payload(decode=True),
                                                                                 'lxml').get_text(" ", strip=True))
                                    body_info = re.sub('\n+', '\n', body_match)
                                    if w and issubclass(w[-1].category, UserWarning) and \
                                            "MarkupResemblesLocatorWarning" in str(w[-1].message):
                                        body_match = re.sub(' +', ' ', BeautifulSoup(
                                            part.get_payload(decode=True),
                                            'html.parser').get_text(" ", strip=True))
                                        body_info = re.sub('\n+', '\n', body_match)

                                if not body_info or body_info == (from_name + from_email if from_name else from_email):
                                    body_info = "null"
                            appendix_name = part.get_filename()
                            if appendix_name:
                                if part.get_content_charset():
                                    appendix_info = decode_field(appendix_name, charset=part.get_content_charset())
                                    if down_appendix:
                                        attach_data = part.get_payload(decode=True)
                                        self.down_appendix(
                                            email_file_down_path=email_file_down_path,
                                            appendix_info=appendix_info,
                                            payload=attach_data)
                                else:
                                    appendix_name = part.get("Content-Type")
                                    appendix_info = decode_field(appendix_name)
                                    if down_appendix:
                                        attach_data = part.get_payload(decode=True)
                                        self.down_appendix(
                                            email_file_down_path=email_file_down_path,
                                            appendix_info=appendix_info,
                                            payload=attach_data)

                                    match_result = re.search(r'name="(.+?)"', repr(appendix_info), flags=re.I)
                                    appendix_info = match_result.group(1) if match_result else appendix_info
                                    if "\\n" in appendix_info:
                                        appendix_info = appendix_info.split("\\n")[-1].strip()
                            if email_info_table_save and part.get_payload(decode=True):
                                try:
                                    decoded = re.sub(
                                        rb'\\x[a-fA-F0-9]{2}',
                                        decode_match,
                                        part.get_payload(decode=True)
                                    ).decode("gb18030")
                                except ValueError:
                                    decoded = re.sub(
                                        rb'\\x[a-fA-F0-9]{2}',
                                        decode_match,
                                        part.get_payload(decode=True)
                                    ).decode("utf-8", errors="ignore")
                                soup = BeautifulSoup(decoded, 'html.parser')
                                if not email_file_down_path:
                                    raise ValueError("未指定 email_file_down_path 变量, 请指定文件保存路径")
                                email_file_down_path = check_path(folder_path=email_file_down_path)
                                tables = soup.find_all('table')
                                if tables:
                                    for table in tables:
                                        headers, rows = get_table_data(table)
                                        file = check_path(
                                            folder_path=email_file_down_path,
                                            filename=f"{from_email}_{subject_info}_{date_info}.csv",
                                            exist_check=False
                                        )
                                        if headers:
                                            with open(file, mode='w') as csv_file:
                                                writer = csv.writer(csv_file)
                                                writer.writerow(headers)
                                                for row in rows:
                                                    writer.writerow(row)
                                                csv_file.close()
                                        else:
                                            with open(file, mode='w') \
                                                    as csv_file:
                                                writer = csv.writer(csv_file)
                                                for row in rows:
                                                    writer.writerow(row)
                                                csv_file.close()

                    mail_info[i] = {
                        "Subject": subject_info,
                        "From": from_info,
                        "To": to_info,
                        "Date": date_info,
                        "Date_Detail": date_detail_info,
                        "Body": body_info,
                        "Appendix": appendix_info}
        self.all_mail = mail_info
        return mail_info

    def filter_mail(
            self,
            _from: str = None,
            _to: str = None,
            _subject: str = None,
            _start_date: str = None,
            _end_date: str = None,
            _date: str = None,
            _appendix: str = None,
            _keyword: str = None,
            is_exact_query: bool = False,
            is_case_sensitive: bool = False,
    ):
        """筛选邮件
        可通过发件人,接收人,主题,起止时间,指定日期,附件名称,关键字进行查询,同时可以选择是否进行精确查询以及区分大小写

        Args:
            _from:              字符串类型 -> 发件人 -> 非必需
            _to:                字符串类型 -> 收件人 -> 非必需
            _subject:           字符串类型 -> 主题名 -> 非必需
            _start_date:        字符串类型 -> 开始时间 -> 非必需
            _end_date:          字符串类型 -> 结束时间 -> 非必需
            _date:              字符串类型 -> 指定日期 -> 非必需
            _appendix:          字符串类型 -> 附件名称 -> 非必需
            _keyword:           字符串类型 -> 关键字 -> 非必需
            is_exact_query:     布尔值类型 -> 是否精确查询,默认模糊查询 -> 非必需
            is_case_sensitive:  布尔值类型 -> 是否区分大小写,默认不区分 -> 非必需
        """
        if not is_case_sensitive:
            _from = _from.lower() if _from else None
            _to = _to.lower() if _to else None
            _subject = _subject.lower() if _subject else None
            _appendix = _appendix.lower() if _appendix else None
            _keyword = _keyword.lower() if _keyword else None

        if is_exact_query:
            if not _from and not _to and not _subject and not ((_start_date and _end_date) or _date) and not _appendix:
                raise Exception("筛选参数为空，请输入参数")
            if _start_date or _end_date:
                if not (_start_date and _end_date):
                    raise Exception("请检查开始和结束时间是否已指定")
                if (_start_date or _end_date) and _date:
                    raise Exception("请选择指定时间段或某一天")
            if self.all_mail:
                all_mail = self.all_mail
            else:
                all_mail = self.get_all_mail()
            if not is_case_sensitive:
                if _from:
                    all_mail = {k: v for k, v in all_mail.items()
                                if v[k]["From"].lower() == _from
                                or v["From"].lower() in _from
                                or _from in v["From"].lower()}
                if _to:
                    all_mail = {k: v for k, v in all_mail.items()
                                if v["To"].lower() == _to
                                or v["To"].lower() in _to
                                or _to in v["To"].lower()}
                if _subject:
                    all_mail = {k: v for k, v in all_mail.items()
                                if v["Subject"].lower() == _subject
                                or v["Subject"].lower() in _subject
                                or _subject in v["Subject"].lower()}
                if _appendix:
                    all_mail = {k: v for k, v in all_mail.items()
                                if v["Appendix"].lower() == _appendix
                                or v["Appendix"].lower() in _appendix
                                or _appendix in v["Appendix"].lower()}
            else:
                if _from:
                    all_mail = {k: v for k, v in all_mail.items()
                                if v[k]["From"] == _from
                                or v["From"] in _from
                                or _from in v["From"]}
                if _to:
                    all_mail = {k: v for k, v in all_mail.items()
                                if v["To"] == _to
                                or v["To"] in _to
                                or _to in v["To"]}
                if _subject:
                    all_mail = {k: v for k, v in all_mail.items()
                                if v["Subject"] == _subject
                                or v["Subject"] in _subject
                                or _subject in v["Subject"]}
                if _appendix:
                    all_mail = {k: v for k, v in all_mail.items()
                                if v["Appendix"] == _appendix
                                or v["Appendix"] in _appendix
                                or _appendix in v["Appendix"]}
            if _start_date:
                all_mail = {k: v for k, v in all_mail.items() if v["Date"] < _start_date}
            if _end_date:
                all_mail = {k: v for k, v in all_mail.items() if v["Date"] > _end_date}
            if _date:
                all_mail = {k: v for k, v in all_mail.items() if v["Date"] == _date}
        else:
            if not _keyword:
                raise Exception("请指定关键字")
            if self.all_mail:
                all_mail = self.all_mail
            else:
                all_mail = self.get_all_mail()

            all_mail = {
                k: v for k, v in all_mail.items()
                for k_item in v
                if v[k_item] and (v[k_item] == _keyword or _keyword in v[k_item] or v[k_item] in _keyword)
            }
            if not is_case_sensitive:
                if _from:
                    all_mail = {k: v for k, v in all_mail.items()
                                if v[k]["From"].lower() == _from
                                or v["From"].lower() in _from
                                or _from in v["From"].lower()}
                if _to:
                    all_mail = {k: v for k, v in all_mail.items()
                                if v["To"].lower() == _to
                                or v["To"].lower() in _to
                                or _to in v["To"].lower()}
                if _subject:
                    all_mail = {k: v for k, v in all_mail.items()
                                if v["Subject"].lower() == _subject
                                or v["Subject"].lower() in _subject
                                or _subject in v["Subject"].lower()}
                if _appendix:
                    all_mail = {k: v for k, v in all_mail.items()
                                if v["Appendix"].lower() == _appendix
                                or v["Appendix"].lower() in _appendix
                                or _appendix in v["Appendix"].lower()}
            else:
                if _from:
                    all_mail = {k: v for k, v in all_mail.items()
                                if v[k]["From"] == _from
                                or v["From"] in _from
                                or _from in v["From"]}
                if _to:
                    all_mail = {k: v for k, v in all_mail.items()
                                if v["To"] == _to
                                or v["To"] in _to
                                or _to in v["To"]}
                if _subject:
                    all_mail = {k: v for k, v in all_mail.items()
                                if v["Subject"] == _subject
                                or v["Subject"] in _subject
                                or _subject in v["Subject"]}
                if _appendix:
                    all_mail = {k: v for k, v in all_mail.items()
                                if v["Appendix"] == _appendix
                                or v["Appendix"] in _appendix
                                or _appendix in v["Appendix"]}
            if _start_date:
                all_mail = {k: v for k, v in all_mail.items() if v["Date"] < _start_date}
            if _end_date:
                all_mail = {k: v for k, v in all_mail.items() if v["Date"] > _end_date}
            if _date:
                all_mail = {k: v for k, v in all_mail.items() if v["Date"] == _date}

        return all_mail

    def down_appendix(
            self,
            uid: str = None,
            email_file_down_path: str = None,
            appendix_info: str = None,
            payload: Any = None
    ) -> None:
        """下载附件

        Args:
            uid: 字符串类型, 附件对应邮件的id
            email_file_down_path: str = None,
            appendix_info: str = None,
            payload: Any = None
        Returns:
            None
        """
        if payload:
            if appendix_info:
                for item in appendix_info:
                    email_file_down_path = check_path(email_file_down_path, error_info="请指定附件保存路径")
                    f = open(email_file_down_path + item, 'wb')  # 注意一定要用wb来打开文件，因为附件一般都是二进制文件
                    f.write(payload)
                    f.close()
            else:
                raise Exception("若是指定payload参数，则必须指定文件名称")
        else:
            if not uid:
                raise Exception("下载指定附件，必须指定UID")
            status, email_content = self.imap.fetch(uid, '(RFC822)')
            for response_part in email_content:
                if isinstance(response_part, tuple):
                    email_parser = email.parser.BytesFeedParser()
                    email_parser.feed(response_part[1])
                    msg = email_parser.close()
                    if msg.is_multipart():
                        for part in msg.walk():
                            if not appendix_info:
                                appendix_info = decode_field(part.get_filename())
                            if part.get_content_charset():
                                attach_data = part.get_payload(decode=True)  # 解码出附件数据，然后存储到文件中
                                email_file_down_path = check_path(email_file_down_path, error_info="请指定附件保存路径")
                                f = open(email_file_down_path + appendix_info, 'wb')  # 注意一定要用wb来打开文件，因为附件一般都是二进制文件
                                f.write(attach_data)
                                f.close()
                            else:
                                appendix_info = part.get_filename()
                                attach_data = part.get_payload(decode=True)  # 解码出附件数据，然后存储到文件中
                                email_file_down_path = check_path(email_file_down_path, error_info="请指定附件保存路径")
                                f = open(email_file_down_path + appendix_info, 'wb')  # 注意一定要用wb来打开文件，因为附件一般都是二进制文件
                                f.write(attach_data)
                                f.close()


class TencentMailSendService:
    """腾讯邮箱发送服务

    Args:
        smtp:           SMTP类 -> 邮箱发送客户端 -> 必需
        mail_account:   字符串类型 -> 邮箱用户 -> 必需
    """

    def __init__(self, smtp: smtplib.SMTP, mail_account: str):
        self.smtp = smtp
        self.mail_account = mail_account

    def send_text_email(self, _title: str, _msg: str, receiver: str, _to: str = None, is_html: bool = False):
        """发送文本邮件(不含附件)

        Args:
            _title:     字符串类型 -> 邮件标题 -> 必需
            _msg:       字符串类型 -> 邮件内容 -> 必需
            receiver:   字符串类型 -> 接收邮箱 -> 必需
            _to:        字符串类型 -> 接收对象,可以是接收人的昵称,也可以是类别名称 -> 非必需
            is_html:    布尔值类型 -> 是否含有网页代码 -> 默认 False,否
        Returns:
            None
        """
        msg = MIMEText(_msg, 'html' if is_html else 'plain', 'utf-8')
        msg["From"] = self.mail_account
        msg["Subject"] = Header(_title, 'utf-8')
        if _to:
            msg["To"] = Header(_to, 'utf-8')
            self.smtp.sendmail(self.mail_account, receiver, msg.as_string())
        else:
            msg["To"] = Header(receiver, 'utf-8')
            self.smtp.sendmail(self.mail_account, receiver, msg.as_string())

    def send_text_many_email(self, _title: str, _msg: str, receiver: list, _to: dict = None, is_html: bool = False):
        """发送文本邮件给多人(不含附件)

        Args:
            _title:     字符串类型 -> 邮件标题 -> 必需
            _msg:       字符串类型 -> 邮件内容 -> 必需
            receiver:   列表类型 -> 接收对象邮箱列表 -> 必需
            _to:        字典类型 -> 接收对象,可以是接收人的昵称,也可以是类别名称,要求传入key为收件对象邮箱,value为昵称或类别 -> 非必需
            is_html:    布尔值类型 -> 是否含有网页代码 -> 默认 False,否
        Returns:
            None
        """
        msg = MIMEText(_msg, 'html' if is_html else 'plain', 'utf-8')
        msg["From"] = self.mail_account
        msg["Subject"] = Header(_title, 'utf-8')
        if _to and len(list(_to.keys())) == 1 and _to[list(_to.keys())[0]] == ['all']:
            msg["To"] = Header(list(_to.keys())[0], 'utf-8')
            self.smtp.sendmail(self.mail_account, receiver, msg.as_string())
        elif _to and len(list(_to.keys())) > 1:
            for key, value in _to.items():
                if value[0] not in receiver:
                    raise Exception("有收件人的邮箱不存在，请重新检查")
                if len(value) == 1:
                    msg["To"] = Header(key, 'utf-8')
                    self.smtp.sendmail(self.mail_account, value[0], msg.as_string())
                    receiver.remove(value[0])
                    if not receiver:
                        return
                elif len(value) > 1:
                    if len([x for x in value if x not in receiver]):
                        raise Exception("有收件人的邮箱不存在，请重新检查")
                    else:
                        msg["To"] = Header(key, 'utf-8')
                        receiver = [x for x in receiver if x not in value]
                        self.smtp.sendmail(self.mail_account, value, msg.as_string())
                        if not receiver:
                            return
            if receiver:
                for i in receiver:
                    msg["To"] = Header(i, 'utf-8')
                    self.smtp.sendmail(self.mail_account, i, msg.as_string())
        else:
            for i in receiver:
                if not msg["To"]:
                    msg["To"] = Header(i, 'utf-8')
                else:
                    msg.replace_header("To", i)
                self.smtp.sendmail(self.mail_account, i, msg.as_string())

    def send_multipart_mail(
            self,
            _title: str,
            _msg: str,
            receiver: str,
            appendix_path: str,
            appendix: list,
            _to=None,
            is_html=False,
            filename_with_timestamp: bool = False,
            custom_file_date: str or int = None
    ):
        """发送附件邮件

        Args:
            _title:         字符串类型 -> 邮件标题 -> 必需
            _msg:           字符串类型 -> 邮件内容 -> 必需
            receiver:       字符串类型 -> 接收对象邮箱 -> 必需
            appendix_path:  字符串类型 -> 附件路径 -> 必需
            appendix:       列表类型 -> 附件列表 -> 必需
            _to:            字符串类型 -> 接收对象,可以是接收人的昵称,也可以是类别名称 -> 非必需
            is_html:        布尔值类型 -> 是否含有网页代码 -> 默认 False,否
            filename_with_timestamp:    布尔值类型 -> 文件名是否携带时间戳,附件发送时,可让文件名携带时间戳 -> 默认 False,否
            custom_file_date:           字符串或整数类型 -> 自定义附件文件名中的时间 -> 非必需
        Returns:
            None
        """
        msg = MIMEMultipart()
        msg["From"] = self.mail_account
        msg["Subject"] = Header(_title, 'utf-8')
        msg.attach(MIMEText(_msg, 'html' if is_html else 'plain', 'utf-8'))
        for item in appendix:
            file = check_path(folder_path=appendix_path, filename=item)
            if 'txt' in item:
                att = MIMEText(str(open(file, 'rb').read()), 'base64', 'utf-8')
            else:
                att = MIMEApplication(open(file, 'rb').read())
            att["Content-Type"] = 'application/octet-stream'
            if filename_with_timestamp:
                att.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename=(
                        "gbk",
                        "",
                        datetime.strptime(str(custom_file_date), "%Y%m%d").strftime("%Y年%m月%d日") + item
                        if custom_file_date else
                        datetime.now().strftime("%Y年%m月%d日") + item))
            else:
                att.add_header("Content-Disposition", "attachment", filename=("gbk", "", item))
            msg.attach(att)
        if _to:
            msg["To"] = Header(_to, 'utf-8')
            self.smtp.sendmail(self.mail_account, receiver, msg.as_string())
        else:
            msg["To"] = Header(receiver, 'utf-8')
            self.smtp.sendmail(self.mail_account, receiver, msg.as_string())

    def send_many_multipart_mail(
            self,
            _title: str,
            _msg: str,
            receiver: list,
            appendix_path: str,
            appendix: list,
            _to: dict = None,
            is_html=False,
            filename_with_timestamp=False,
            custom_file_date: str or int = None
    ):
        """发送附件邮件给多人

        Args:
            _title:         字符串类型 -> 邮件标题 -> 必需
            _msg:           字符串类型 -> 邮件内容 -> 必需
            receiver:       字符串类型 -> 接收对象邮箱 -> 必需
            appendix_path:  字符串类型 -> 附件路径 -> 必需
            appendix:       列表类型 -> 附件列表 -> 必需
            _to:            字典类型 -> 接收对象,可以是接收人的昵称,也可以是类别名称,要求传入key为收件对象邮箱,value为昵称或类别 -> 非必需
            is_html:        布尔值类型 -> 是否含有网页代码 -> 默认 False,否
            filename_with_timestamp:    布尔值类型 -> 文件名是否携带时间戳,附件发送时,可让文件名携带时间戳 -> 默认 False,否
            custom_file_date:           字符串或整数类型 -> 自定义附件文件名中的时间 -> 非必需
        Returns:
            None
        """
        msg = MIMEMultipart()
        msg["From"] = self.mail_account
        msg["Subject"] = Header(_title, 'utf-8')

        msg.attach(MIMEText(_msg, 'html' if is_html else 'plain', 'utf-8'))
        for item in appendix:
            file = check_path(folder_path=appendix_path, filename=item)
            if 'txt' in item:
                att = MIMEText(str(open(file, 'rb').read()), 'base64', 'utf-8')
            else:
                att = MIMEApplication(open(file + item, 'rb').read())
            att["Content-Type"] = 'application/octet-stream'
            if filename_with_timestamp:
                att.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename=(
                        "gbk",
                        "",
                        datetime.strptime(str(custom_file_date), "%Y%m%d").strftime("%Y年%m月%d日") + item
                        if custom_file_date else
                        datetime.now().strftime("%Y年%m月%d日") + item))
            else:
                att.add_header("Content-Disposition", "attachment", filename=("gbk", "", item))
            msg.attach(att)
        if _to and len(list(_to.keys())) == 1 and _to[list(_to.keys())[0]] == ['all']:
            msg["To"] = Header(list(_to.keys())[0], 'utf-8')
            self.smtp.sendmail(self.mail_account, receiver, msg.as_string())
        elif _to and len(list(_to.keys())) > 1:
            for key, value in _to.items():
                if value[0] not in receiver:
                    raise Exception("有收件人的邮箱不存在，请重新检查")
                if len(value) == 1:
                    msg["To"] = Header(key, 'utf-8')
                    self.smtp.sendmail(self.mail_account, value[0], msg.as_string())
                    receiver.remove(value[0])
                    if not receiver:
                        return
                elif len(value) > 1:
                    if len([x for x in value if x not in receiver]):
                        raise Exception("有收件人的邮箱不存在，请重新检查")
                    else:
                        msg["To"] = Header(key, 'utf-8')
                        receiver = [x for x in receiver if x not in value]
                        self.smtp.sendmail(self.mail_account, value, msg.as_string())
                        if not receiver:
                            return
            if receiver:
                for i in receiver:
                    msg["To"] = Header(i, 'utf-8')
                    self.smtp.sendmail(self.mail_account, i, msg.as_string())
        else:
            for i in receiver:
                if not msg["To"]:
                    msg["To"] = Header(i, 'utf-8')
                else:
                    msg.replace_header("To", i)
                self.smtp.sendmail(self.mail_account, i, msg.as_string())

    def send_image_and_text_mail(
            self,
            _title: str,
            _msg: str,
            receiver: str,
            image_path: str,
            image: list,
            _to: str = None
    ):
        """发送带图片的文本邮件

        Args:
            _title:         字符串类型 -> 邮件标题 -> 必需
            _msg:           字符串类型 -> 邮件内容 -> 必需
            receiver:       字符串类型 -> 接收对象邮箱 -> 必需
            image_path:     字符串类型 -> 图片路径 -> 必需
            image:          列表类型 -> 图片列表 -> 必需
            _to:            字符串类型 -> 接收对象,可以是接收人的昵称,也可以是类别名称 -> 非必需
        Returns:
            None
        """
        msg = MIMEMultipart('related')
        msg["From"] = self.mail_account
        msg["Subject"] = Header(_title, 'utf-8')
        msg_alternative = MIMEMultipart('alternative')
        msg.attach(msg_alternative)
        msg_text = (MIMEText(_msg, 'html', 'utf-8'))
        msg_alternative.attach(msg_text)

        for item in image:
            file = check_path(folder_path=image_path, filename=item)
            img = open(file, 'rb')
            msg_image = MIMEImage(img.read())
            img.close()
            # 定义图片 ID，在 HTML 文本中引用
            msg_image.add_header('Content-ID', f'<{str(item).replace(".", "_")}>')
            msg.attach(msg_image)

        if _to:
            msg["To"] = Header(_to, 'utf-8')
            self.smtp.sendmail(self.mail_account, receiver, msg.as_string())
        else:
            msg["To"] = Header(receiver, 'utf-8')
            self.smtp.sendmail(self.mail_account, receiver, msg.as_string())

    def send_many_image_and_text_mail(
            self,
            _title: str,
            _msg: str,
            receiver: list,
            image_path: str,
            image: list,
            _to: dict = None
    ):
        """发送带图片的文本邮件给多人

        Args:
            _title:         字符串类型 -> 邮件标题 -> 必需
            _msg:           字符串类型 -> 邮件内容 -> 必需
            receiver:       字符串类型 -> 接收对象邮箱 -> 必需
            image_path:     字符串类型 -> 图片路径 -> 必需
            image:          列表类型 -> 图片列表 -> 必需
            _to:            字典类型 -> 接收对象,可以是接收人的昵称,也可以是类别名称,要求传入key为收件对象邮箱,value为昵称或类别 -> 非必需
        Returns:
            None
        """
        msg = MIMEMultipart('related')
        msg["From"] = self.mail_account
        msg["Subject"] = Header(_title, 'utf-8')
        msg_alternative = MIMEMultipart('alternative')
        msg.attach(msg_alternative)
        msg_text = (MIMEText(_msg, 'html', 'utf-8'))
        msg_alternative.attach(msg_text)

        for item in image:
            file = check_path(folder_path=image_path, filename=item)
            img = open(file, 'rb')
            msg_image = MIMEImage(img.read())
            img.close()
            # 定义图片 ID，在 HTML 文本中引用
            msg_image.add_header('Content-ID', f'<{str(item).replace(".", "_")}>')
            msg.attach(msg_image)

        if _to and len(list(_to.keys())) == 1 and _to[list(_to.keys())[0]] == ['all']:
            msg["To"] = Header(list(_to.keys())[0], 'utf-8')
            self.smtp.sendmail(self.mail_account, receiver, msg.as_string())
        elif _to and len(list(_to.keys())) > 1:
            for key, value in _to.items():
                if value[0] not in receiver:
                    raise Exception("有收件人的邮箱不存在，请重新检查")
                if len(value) == 1:
                    msg["To"] = Header(key, 'utf-8')
                    self.smtp.sendmail(self.mail_account, value[0], msg.as_string())
                    receiver.remove(value[0])
                    if not receiver:
                        return
                elif len(value) > 1:
                    if len([x for x in value if x not in receiver]):
                        raise Exception("有收件人的邮箱不存在，请重新检查")
                    else:
                        msg["To"] = Header(key, 'utf-8')
                        receiver = [x for x in receiver if x not in value]
                        self.smtp.sendmail(self.mail_account, value, msg.as_string())
                        if not receiver:
                            return
            if receiver:
                for i in receiver:
                    msg["To"] = Header(i, 'utf-8')
                    self.smtp.sendmail(self.mail_account, i, msg.as_string())
        else:
            for i in receiver:
                if not msg["To"]:
                    msg["To"] = Header(i, 'utf-8')
                else:
                    msg.replace_header("To", i)
                self.smtp.sendmail(self.mail_account, i, msg.as_string())

    def send_image_and_multipart_mail(
            self,
            _title,
            _msg,
            receiver: str,
            image_path: str,
            image: list,
            appendix_path: str,
            appendix: list,
            _to: str = None,
            filename_with_timestamp: bool = False,
            custom_file_date: str or int = None
    ):
        """发送带图片与附件的文本邮件

        Args:
            _title:         字符串类型 -> 邮件标题 -> 必需
            _msg:           字符串类型 -> 邮件内容 -> 必需
            receiver:       字符串类型 -> 接收对象邮箱 -> 必需
            image_path:     字符串类型 -> 图片路径 -> 必需
            image:          列表类型 -> 图片列表 -> 必需
            appendix_path:  字符串类型 -> 附件路径 -> 必需
            appendix:       列表类型 -> 附件列表 -> 必需
            _to:            字符串类型 -> 接收对象,可以是接收人的昵称,也可以是类别名称 -> 非必需
            filename_with_timestamp:    布尔值类型 -> 文件名是否携带时间戳,附件发送时,可让文件名携带时间戳 -> 默认 False,否
            custom_file_date:           字符串或整数类型 -> 自定义附件文件名中的时间 -> 非必需
        Returns:
            None
        """
        msg = MIMEMultipart('related')
        msg["From"] = self.mail_account
        msg["Subject"] = Header(_title, 'utf-8')
        msg_appendix = MIMEMultipart()
        for item in appendix:
            file = check_path(folder_path=appendix_path, filename=item)
            if 'txt' in item:
                att = MIMEText(str(open(file, 'rb').read()), 'base64', 'utf-8')
            else:
                att = MIMEApplication(open(file, 'rb').read())
            att["Content-Type"] = 'application/octet-stream'
            if filename_with_timestamp:
                att.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename=(
                        "gbk",
                        "",
                        datetime.strptime(str(custom_file_date), "%Y%m%d").strftime("%Y年%m月%d日") + item
                        if custom_file_date else
                        datetime.now().strftime("%Y年%m月%d日") + item))
            else:
                att.add_header("Content-Disposition", "attachment", filename=("gbk", "", item))
            msg_appendix.attach(att)
        msg.attach(msg_appendix)
        msg_alternative = MIMEMultipart('alternative')
        msg.attach(msg_alternative)
        msg_text = (MIMEText(_msg, 'html', 'utf-8'))
        msg_alternative.attach(msg_text)

        for item in image:
            file = check_path(folder_path=image_path, filename=item)
            img = open(file + item, 'rb')
            msg_image = MIMEImage(img.read())
            img.close()
            # 定义图片 ID，在 HTML 文本中引用
            msg_image.add_header('Content-ID', f'<{str(item).replace(".", "_")}>')
            msg.attach(msg_image)

        if _to:
            msg["To"] = Header(_to, 'utf-8')
            self.smtp.sendmail(self.mail_account, receiver, msg.as_string())
        else:
            msg["To"] = Header(receiver, 'utf-8')
            self.smtp.sendmail(self.mail_account, receiver, msg.as_string())

    def send_many_image_and_multipart_mail(
            self,
            _title: str,
            _msg: str,
            receiver: list,
            image_path: str,
            image: list,
            appendix_path: str,
            appendix: list,
            _to: dict = None,
            filename_with_timestamp=False,
            custom_file_date: str or int = None
    ):
        """发送带图片与附件的文本邮件给多人

        Args:
            _title:         字符串类型 -> 邮件标题 -> 必需
            _msg:           字符串类型 -> 邮件内容 -> 必需
            receiver:       字符串类型 -> 接收对象邮箱 -> 必需
            image_path:     字符串类型 -> 图片路径 -> 必需
            image:          列表类型 -> 图片列表 -> 必需
            appendix_path:  字符串类型 -> 附件路径 -> 必需
            appendix:       列表类型 -> 附件列表 -> 必需
            _to:            字典类型 -> 接收对象,可以是接收人的昵称,也可以是类别名称,要求传入key为收件对象邮箱,value为昵称或类别 -> 非必需
            filename_with_timestamp:    布尔值类型 -> 文件名是否携带时间戳,附件发送时,可让文件名携带时间戳 -> 默认 False,否
            custom_file_date:           字符串或整数类型 -> 自定义附件文件名中的时间 -> 非必需
        Returns:
            None
        """
        msg = MIMEMultipart('related')
        msg["From"] = self.mail_account
        msg["Subject"] = Header(_title, 'utf-8')
        msg_appendix = MIMEMultipart()
        for item in appendix:
            file = check_path(folder_path=appendix_path, filename=item)
            if 'txt' in item:
                att = MIMEText(str(open(file, 'rb').read()), 'base64', 'utf-8')
            else:
                att = MIMEApplication(open(file, 'rb').read())
            att["Content-Type"] = 'application/octet-stream'
            if filename_with_timestamp:
                att.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename=(
                        "gbk",
                        "",
                        datetime.strptime(str(custom_file_date), "%Y%m%d").strftime("%Y年%m月%d日") + item
                        if custom_file_date else
                        datetime.now().strftime("%Y年%m月%d日") + item))
            else:
                att.add_header("Content-Disposition", "attachment", filename=("gbk", "", item))
            msg_appendix.attach(att)
        msg.attach(msg_appendix)
        msg_alternative = MIMEMultipart('alternative')
        msg.attach(msg_alternative)
        msg_text = (MIMEText(_msg, 'html', 'utf-8'))
        msg_alternative.attach(msg_text)
        for item in image:
            file = check_path(folder_path=image_path, filename=item)
            img = open(file, 'rb')
            msg_image = MIMEImage(img.read())
            img.close()
            # 定义图片 ID，在 HTML 文本中引用
            msg_image.add_header('Content-ID', f'<{str(item).replace(".", "_")}>')
            msg.attach(msg_image)

        if _to and len(list(_to.keys())) == 1 and _to[list(_to.keys())[0]] == ['all']:
            msg["To"] = Header(list(_to.keys())[0], 'utf-8')
            self.smtp.sendmail(self.mail_account, receiver, msg.as_string())
        elif _to and len(list(_to.keys())) > 1:
            for key, value in _to.items():
                if value[0] not in receiver:
                    raise Exception("有收件人的邮箱不存在，请重新检查")
                if len(value) == 1:
                    msg["To"] = Header(key, 'utf-8')
                    self.smtp.sendmail(self.mail_account, value[0], msg.as_string())
                    receiver.remove(value[0])
                    if not receiver:
                        return
                elif len(value) > 1:
                    if len([x for x in value if x not in receiver]):
                        raise Exception("有收件人的邮箱不存在，请重新检查")
                    else:
                        msg["To"] = Header(key, 'utf-8')
                        receiver = [x for x in receiver if x not in value]
                        self.smtp.sendmail(self.mail_account, value, msg.as_string())
                        if not receiver:
                            return
            if receiver:
                for i in receiver:
                    msg["To"] = Header(i, 'utf-8')
                    self.smtp.sendmail(self.mail_account, i, msg.as_string())
        else:
            for i in receiver:
                if not msg["To"]:
                    msg["To"] = Header(i, 'utf-8')
                else:
                    msg.replace_header("To", i)
                self.smtp.sendmail(self.mail_account, i, msg.as_string())


class EmailManager:
    """邮箱管理器
    目前仅支持 `QQ（腾讯）邮箱` 与 `QQ（腾讯）企业邮箱` 的 `IMAP` 与 `SMTP` 服务，其余邮箱待开发...
    功能支持：收发邮件、筛选邮件
    Args:
        email_port: 整数类型 -> 邮件服务器端口号，当
        email_type: 字符串类型 -> 邮件服务器类型：当服务器地址无法识别接收或发送时指定，目前仅支持 `imap` 与 `smtp` -> 非必需
        username:   字符串类型 -> 邮箱用户名 -> 必需
        password:   字符串类型 -> 邮箱密码 -> 必需
    """

    def __init__(self, username: str, password: str, email_host: str, email_port: int, email_type: str = None):
        self.email_host = email_host
        self.email_port = email_port
        self.email_type = email_type
        self.username = username
        self.password = password

    def get_mail_control(self):
        if not re.match(".*.qq.com", self.email_host):
            raise Exception("目前仅支持QQ(腾讯)邮箱与QQ(腾讯)企业邮箱，其余邮箱开发中...")
        if self.email_type and self.email_type.upper() == "IMAP":
            import imaplib
            imap = imaplib.IMAP4_SSL(self.email_host, port=self.email_port)
            imap.login(self.username, self.password)
            imap.select()
            return TencentMailReceiveService(imap)
        elif self.email_type and self.email_type.upper() == "SMTP":
            import smtplib
            smtp = smtplib.SMTP_SSL(self.email_host, port=self.email_port)
            smtp.login(self.username, self.password)
            return TencentMailSendService(smtp, self.username)
        elif not self.email_type and "imap" in self.email_host:
            import imaplib
            imap = imaplib.IMAP4_SSL(self.email_host, port=self.email_port)
            imap.login(self.username, self.password)
            imap.select()
            return TencentMailReceiveService(imap)
        elif not self.email_type and "smtp" in self.email_host:
            import smtplib
            smtp = smtplib.SMTP_SSL(self.email_host, port=self.email_port)
            smtp.login(self.username, self.password)
            return TencentMailSendService(smtp, self.username)
        else:
            raise Exception("请指定有效的 SMTP 或 IMAP 服务器地址")
