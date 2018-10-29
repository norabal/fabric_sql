import enum
import os
from datetime import datetime

from fabric.api import run, env, task
from fabric.colors import yellow
from fabric.contrib.console import confirm
from fabric.utils import puts, error

from config import get_config
from definitions import ROOT_DIR, CONFIG_PATH
from util import adjust_for_expanduser

config = get_config(CONFIG_PATH)

env.user = config.get('ssh', 'user')
env.hosts = config.get('hosts', env.dest).split(',') if 'dest' in env else None
env.gateway = config.get('hosts', 'step', fallback=None)
env.ssh_config_path = adjust_for_expanduser(config.get('ssh', 'config_path'))
env.use_ssh_config = True

MYSQL_EXEC = config.get('mysql', 'exec')


class Style(enum.Enum):
    txt = {'message': 'result as text file', 'format': '.txt', 'encode': 'utf-8'}
    csv = {'message': 'result as csv', 'format': '.csv', 'encode': 'utf-8'}
    excel = {'message': 'result as csv for excel (shift_jis)', 'format': '_sjis.csv', 'encode': 'shift_jis'}


@task()
def remote_sql():
    """
    Execute your sql on remote hosts from local PC.

    - Copy config.ini.sample as 'config.ini'.
    - Edit 'config.ini'
    - Write sql on 'exec.py'.
    - Execute remote_sql task with set keys.
        if you want to extract sql result from staging environment with csv format for excel.
        ex) fab --set dest=stg,format=excel remote_sql

    :return: void
    """
    sql_path = os.path.join(ROOT_DIR, 'exec.sql')
    with open(sql_path, 'r') as f:
        sql = f.read()

    disp_sql = '\n'.join([
        '\n\n*** you are about to execute below sql ***\n',
        yellow(sql),
        '\n******************************************\n'
    ])
    puts(disp_sql)

    if confirm('ok?', default=False):
        exec_sql = MYSQL_EXEC.format(sql)
        exec_sql_csv = "{} | sed -e 's/\t/,/g'".format(exec_sql, sql)

        try:
            if 'format' not in env:
                result = run(exec_sql)
                puts('\n' + result)

            elif 'txt' == env.format:
                get_sql_result(exec_sql, Style.txt)

            elif 'csv' == env.format:
                get_sql_result(exec_sql_csv, Style.csv)

            elif 'excel' == env.format:
                get_sql_result(exec_sql_csv, Style.excel)

            else:
                raise ValueError('choose proper format: [txt, csv, excel]')

        except Exception as err:
            error('something wrong happened: {}'.format(err))

    puts('Bye')


def get_sql_result(sql, style):
    puts(style.value.get('encode'))

    output_dir = os.path.join(ROOT_DIR, 'output')
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    output_name = datetime.now().strftime('%Y%m%d%H%M%S')
    output_path = os.path.join(output_dir, output_name + style.value.get('format'))

    result = run(sql)
    with open(output_path, 'w', encoding=style.value.get('encode')) as f:
        f.write(result)
