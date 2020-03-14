""" ......................................................................
# Application Name				: zaevswr.py
# Version						: v1.0.4
# Author 						: me@endang-ismaya.com
# Date Created                  : April 19, 2018
# Update						: Mar 09, 2020
# Comment						: Bot Zaenal's request
......................................................................."""
import getopt
import os
import re
import sys


def main():
    logs_folder = None
    try:
        options, remainder = getopt.getopt(
            sys.argv[1:], 'f:vh',
            [
                'version', 'folder=', 'help'
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)

    for opt, arg in options:
        if opt in ('-v', '--version'):
            print("Zaevswr v1.0.4")
            sys.exit(1)
        elif opt in ('-h', '--help'):
            print("Help is in progress")
            sys.exit(1)
        elif opt in '-f':
            logs_folder = arg

    # Validate kget's folder
    if logs_folder is None:
        print("Please enter a log folder!!!")
        sys.exit(1)
    else:
        # print(logs_folder)
        inv = InvxrParser(logs_folder)
        inv.do_parser()


class InvxrParser:

    def __init__(self, target_folder):
        self._target_folder = target_folder

    def get_target_folder(self):
        return self._target_folder

    def do_parser(self):
        dict_a = {}
        dict_b = {}
        dict_c = {}
        dict_d = {}
        for invxr_logs in os.listdir(self._target_folder):
            if invxr_logs.endswith('.log'):
                invxr_log = os.path.join(self._target_folder, invxr_logs)
                sitename = 'siteid'
                with open(invxr_log) as f:
                    for line in f:
                        xline = line.rstrip()
                        m_siteid = re.match(r'([\w-]+)>\s?Invxrfc', xline, flags=re.IGNORECASE)
                        m_co_lte = re.match(r'RRU.*FDD=(\w+)\s+?\(\d+:(\d+)\)$', xline)
                        m_lte_aceh_fdd1 = re.match(r'RRU.*FDD=(\w+)\s+?\(\d+:(\d+):\d+\)$', xline)
                        m_lte_aceh_gt5_fdd1 = re.match(r'RRU.*FDD=(\w+)\s+?\(\d,\s?\d,\s?\d,\s?\d,\s?\d,\s?\d+:(\d+):\d+\)$', xline)
                        m_lte_aceh_tdd1 = re.match(r'RRU.*TDD=(\w+)\s+?\(\d+:(\d+):\d+\)$', xline)
                        m_co_wcdma = re.match(r'RRU.*NB=([\w/]+)\s+?\((\d+)\)$', xline)
                        m_co_lte_wcdma_split = \
                            re.match(
                                r'RRU.*FDD=(\w+)\s+?NB=([\w/]+)\s+?NB=([\w/]+)\s+?\(\d+:(\d+),\s+?(\d+),\s+(\d+)\)',
                                xline
                            )
                        m_dus_g = \
                            re.match(
                                r'\d-\d/R?RUW.*SR=\d\s+(S\dC\d)\s+(S\dC\d)\s+(S\dC\d)\s+\((\d+),\s+(\d+),\s+(\d+)\)$',
                                xline
                            )
                        m_dus_g_single = re.match(
                            r'RUW.*SR=\d.*(S\dC\d)\s+\((\d+)\)$',
                            xline)
                        m_dus_g_asterik_single = re.match(
                            r'\d-\d/R?RUW.*SR=\d.*(S\dC\d)\s+\((\d+)\)$',
                            xline)
                        m_dus_g_indoor = re.match(
                            r'\d/\d/R?RUW.*SR=\d\s+(S\dC\d)\s+(S\dC\d)\s+\((\d+),\s+(\d+)\)$',
                            xline)
                        if m_siteid:
                            sitename = m_siteid.group(1)
                            print(sitename)
                        elif m_co_lte:
                            xline_split = xline.split(';')
                            rf = xline_split[3].strip()
                            try:
                                vswr = xline_split[5].strip().split('(')[0].strip()
                            except IndexError:
                                vswr = '-'
                            fdd = m_co_lte.group(1)
                            cellid = m_co_lte.group(2)
                            # print(sitename, fdd, cellid, rf, vswr)
                            if rf == 'A':
                                dict_a[sitename + "#" + fdd + "#" + cellid] = vswr
                            elif rf == 'B':
                                dict_b[sitename + "#" + fdd + "#" + cellid] = vswr
                            elif rf == 'C':
                                dict_c[sitename + "#" + fdd + "#" + cellid] = vswr
                            elif rf == 'D':
                                dict_d[sitename + "#" + fdd + "#" + cellid] = vswr
                        elif m_lte_aceh_fdd1:
                            xline_split = xline.split(';')
                            rf = xline_split[3].strip()
                            try:
                                vswr = xline_split[6].strip().split('(')[0].strip()
                            except IndexError:
                                vswr = '-'
                            fdd = m_lte_aceh_fdd1.group(1)
                            cellid = m_lte_aceh_fdd1.group(2)
                            print(sitename, fdd, cellid, rf, vswr)
                            if rf == 'A':
                                dict_a[sitename + "#" + fdd + "#" + cellid] = vswr
                            elif rf == 'B':
                                dict_b[sitename + "#" + fdd + "#" + cellid] = vswr
                            elif rf == 'C':
                                dict_c[sitename + "#" + fdd + "#" + cellid] = vswr
                            elif rf == 'D':
                                dict_d[sitename + "#" + fdd + "#" + cellid] = vswr
                        elif m_lte_aceh_gt5_fdd1:
                            xline_split = xline.split(';')
                            rf = xline_split[3].strip()
                            try:
                                vswr = xline_split[6].strip().split('(')[0].strip()
                            except IndexError:
                                vswr = '-'
                            fdd = m_lte_aceh_gt5_fdd1.group(1)
                            cellid = m_lte_aceh_gt5_fdd1.group(2)
                            print(sitename, fdd, cellid, rf, vswr)
                            if rf == 'A':
                                dict_a[sitename + "#" + fdd + "#" + cellid] = vswr
                            elif rf == 'B':
                                dict_b[sitename + "#" + fdd + "#" + cellid] = vswr
                            elif rf == 'C':
                                dict_c[sitename + "#" + fdd + "#" + cellid] = vswr
                            elif rf == 'D':
                                dict_d[sitename + "#" + fdd + "#" + cellid] = vswr
                        elif m_lte_aceh_tdd1:
                            xline_split = xline.split(';')
                            rf = xline_split[3].strip()
                            try:
                                vswr = xline_split[6].strip().split('(')[0].strip()
                            except IndexError:
                                vswr = '-'
                            fdd = m_lte_aceh_tdd1.group(1)
                            cellid = m_lte_aceh_tdd1.group(2)
                            print(sitename, fdd, cellid, rf, vswr)
                            if rf == 'A':
                                dict_a[sitename + "#" + fdd + "#" + cellid] = vswr
                            elif rf == 'B':
                                dict_b[sitename + "#" + fdd + "#" + cellid] = vswr
                            elif rf == 'C':
                                dict_c[sitename + "#" + fdd + "#" + cellid] = vswr
                            elif rf == 'D':
                                dict_d[sitename + "#" + fdd + "#" + cellid] = vswr
                        elif m_co_wcdma:
                            xline_split = xline.split(';')
                            rf = xline_split[3].strip()
                            try:
                                # vswr = xline_split[5].strip().split('(')[1].replace(')', '')
                                vswr = xline_split[5].strip().split('(')[0].strip()
                            except IndexError:
                                vswr = '-'
                            fdd = m_co_wcdma.group(1)
                            cellid = m_co_wcdma.group(2)
                            # print(sitename, fdd, cellid, rf, vswr)
                            if rf == 'A':
                                dict_a[sitename + "#" + fdd + "#" + cellid] = vswr
                            elif rf == 'B':
                                dict_b[sitename + "#" + fdd + "#" + cellid] = vswr
                            elif rf == 'C':
                                dict_c[sitename + "#" + fdd + "#" + cellid] = vswr
                            elif rf == 'D':
                                dict_d[sitename + "#" + fdd + "#" + cellid] = vswr
                        elif m_co_lte_wcdma_split:
                            xline_split = xline.split(';')
                            rf = xline_split[3].strip()
                            try:
                                # vswr = xline_split[5].strip().split('(')[1].replace(')', '')
                                vswr = xline_split[5].strip().split('(')[0].strip()
                            except IndexError:
                                vswr = '-'
                            fdd = m_co_lte_wcdma_split.group(1)
                            wcdma1 = m_co_lte_wcdma_split.group(2)
                            wcdma2 = m_co_lte_wcdma_split.group(3)
                            fdd_cellid = m_co_lte_wcdma_split.group(4)
                            wcdma1_cellid = m_co_lte_wcdma_split.group(5)
                            wcdma2_cellid = m_co_lte_wcdma_split.group(6)
                            # print(sitename, fdd, fdd_cellid, rf, vswr)
                            # print(sitename, wcdma1, wcdma1_cellid, rf, vswr)
                            # print(sitename, wcdma2, wcdma2_cellid, rf, vswr)
                            if rf == 'A':
                                dict_a[sitename + "#" + fdd + "#" + fdd_cellid] = vswr
                                dict_a[sitename + "#" + wcdma1 + "#" + wcdma1_cellid] = vswr
                                dict_a[sitename + "#" + wcdma2 + "#" + wcdma2_cellid] = vswr
                            elif rf == 'B':
                                dict_b[sitename + "#" + fdd + "#" + fdd_cellid] = vswr
                                dict_b[sitename + "#" + wcdma1 + "#" + wcdma1_cellid] = vswr
                                dict_b[sitename + "#" + wcdma2 + "#" + wcdma2_cellid] = vswr
                            elif rf == 'C':
                                dict_c[sitename + "#" + fdd + "#" + fdd_cellid] = vswr
                                dict_c[sitename + "#" + wcdma1 + "#" + wcdma1_cellid] = vswr
                                dict_c[sitename + "#" + wcdma2 + "#" + wcdma2_cellid] = vswr
                            elif rf == 'D':
                                dict_d[sitename + "#" + fdd + "#" + fdd_cellid] = vswr
                                dict_d[sitename + "#" + wcdma1 + "#" + wcdma1_cellid] = vswr
                                dict_d[sitename + "#" + wcdma2 + "#" + wcdma2_cellid] = vswr
                        elif m_dus_g:
                            # print(xline)
                            xline_split = xline.split(';')
                            sector1 = m_dus_g.group(1)
                            sector2 = m_dus_g.group(2)
                            sector3 = m_dus_g.group(3)
                            cellid1 = m_dus_g.group(4)
                            cellid2 = m_dus_g.group(5)
                            cellid3 = m_dus_g.group(6)
                            rf = xline_split[3].strip()
                            try:
                                # vswr = xline_split[5].strip().split('(')[1].replace(')', '')
                                vswr = xline_split[5].strip().split('(')[0].strip()
                            except IndexError:
                                vswr = '-'
                            # print(sitename, sector1, cellid1, rf, vswr)
                            # print(sitename, sector2, cellid2, rf, vswr)
                            # print(sitename, sector3, cellid3, rf, vswr)
                            if rf == 'A':
                                dict_a[sitename + "#" + sector1 + "#" + cellid1] = vswr
                                dict_a[sitename + "#" + sector2 + "#" + cellid2] = vswr
                                dict_a[sitename + "#" + sector3 + "#" + cellid3] = vswr
                            elif rf == 'B':
                                dict_b[sitename + "#" + sector1 + "#" + cellid1] = vswr
                                dict_b[sitename + "#" + sector2 + "#" + cellid2] = vswr
                                dict_b[sitename + "#" + sector3 + "#" + cellid3] = vswr
                            elif rf == 'C':
                                dict_c[sitename + "#" + sector1 + "#" + cellid1] = vswr
                                dict_c[sitename + "#" + sector2 + "#" + cellid2] = vswr
                                dict_c[sitename + "#" + sector3 + "#" + cellid3] = vswr
                            elif rf == 'D':
                                dict_d[sitename + "#" + sector1 + "#" + cellid1] = vswr
                                dict_d[sitename + "#" + sector2 + "#" + cellid2] = vswr
                                dict_d[sitename + "#" + sector3 + "#" + cellid3] = vswr
                        elif m_dus_g_single:
                            # print(xline)
                            xline_split = xline.split(';')
                            sector1 = m_dus_g_single.group(1)
                            cellid1 = m_dus_g_single.group(2)
                            rf = xline_split[3].strip()
                            try:
                                # vswr = xline_split[5].strip().split('(')[1].replace(')', '')
                                vswr = xline_split[5].strip().split('(')[0].strip()
                            except IndexError:
                                vswr = '-'
                            # print(sitename, sector1, cellid1, rf, vswr)
                            if rf == 'A':
                                dict_a[sitename + "#" + sector1 + "#" + cellid1] = vswr
                            elif rf == 'B':
                                dict_b[sitename + "#" + sector1 + "#" + cellid1] = vswr
                            elif rf == 'C':
                                dict_c[sitename + "#" + sector1 + "#" + cellid1] = vswr
                            elif rf == 'D':
                                dict_d[sitename + "#" + sector1 + "#" + cellid1] = vswr
                        elif m_dus_g_asterik_single:
                            # print(xline)
                            xline_split = xline.split(';')
                            sector1 = m_dus_g_asterik_single.group(1)
                            cellid1 = m_dus_g_asterik_single.group(2)
                            rf = xline_split[3].strip()
                            try:
                                # vswr = xline_split[5].strip().split('(')[1].replace(')', '')
                                vswr = xline_split[5].strip().split('(')[0].strip()
                            except IndexError:
                                vswr = '-'
                            # print(sitename, sector1, cellid1, rf, vswr)
                            if rf == 'A':
                                dict_a[sitename + "#" + sector1 + "#" + cellid1] = vswr
                            elif rf == 'B':
                                dict_b[sitename + "#" + sector1 + "#" + cellid1] = vswr
                            elif rf == 'C':
                                dict_c[sitename + "#" + sector1 + "#" + cellid1] = vswr
                            elif rf == 'D':
                                dict_d[sitename + "#" + sector1 + "#" + cellid1] = vswr
                        elif m_dus_g_indoor:
                            # print(xline)
                            xline_split = xline.split(';')
                            sector1 = m_dus_g_indoor.group(1)
                            sector2 = m_dus_g_indoor.group(2)
                            cellid1 = m_dus_g_indoor.group(3)
                            cellid2 = m_dus_g_indoor.group(4)
                            rf = xline_split[3].strip()
                            try:
                                # vswr = xline_split[5].strip().split('(')[1].replace(')', '')
                                vswr = xline_split[5].strip().split('(')[0].strip()
                            except IndexError:
                                vswr = '-'
                            # print(sitename, sector1, cellid1, rf, vswr)
                            # print(sitename, sector2, cellid2, rf, vswr)
                            if rf == 'A':
                                dict_a[sitename + "#" + sector1 + "#" + cellid1] = vswr
                                dict_a[sitename + "#" + sector2 + "#" + cellid2] = vswr
                            elif rf == 'B':
                                dict_b[sitename + "#" + sector1 + "#" + cellid1] = vswr
                                dict_b[sitename + "#" + sector2 + "#" + cellid2] = vswr
                            elif rf == 'C':
                                dict_c[sitename + "#" + sector1 + "#" + cellid1] = vswr
                                dict_c[sitename + "#" + sector2 + "#" + cellid2] = vswr
                            elif rf == 'D':
                                dict_d[sitename + "#" + sector1 + "#" + cellid1] = vswr
                                dict_d[sitename + "#" + sector2 + "#" + cellid2] = vswr

        file_name = os.path.join(self.get_target_folder(), "vswr_result.log")
        if os.path.exists(file_name):
            os.remove(file_name)
        with open(file_name, 'a', newline='') as fp:
            for k, v in dict_a.items():
                # print(k + "#" + v + "#" + dict_b.get(k, '-') + "#" + dict_c.get(k, '-') + "#" + dict_d.get(k, '-'))
                fp.write(k + "#" + v + "#" + dict_b.get(k, '-') + "#" + dict_c.get(k, '-') + "#" + dict_d.get(k, '-') + '\n')
        print("File save as: " + file_name)


if __name__ == '__main__':
    main()
