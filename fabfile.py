import os
from datetime import datetime

from fabric.api import run, env, task
from fabric.colors import green, yellow
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
        output_dir = os.path.join(ROOT_DIR, 'output')
        output_name = datetime.now().strftime('%Y%m%d%H%M%S')
        exec_sql = MYSQL_EXEC.format(sql)
        exec_sql_csv = "{} | sed -e 's/\t/,/g'".format(exec_sql, sql)

        try:
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)

            if 'format' not in env:
                result = run(exec_sql)
                puts(result)

            elif 'txt' == env.format:
                puts('result as text file')
                output_path = os.path.join(output_dir, '{}.txt'.format(output_name))
                result = run(exec_sql)
                with open(output_path, 'w') as f:
                    f.write(result)

            elif 'csv' == env.format:
                puts(green('result as csv'))
                output_path = os.path.join(output_dir, '{}.csv'.format(output_name))
                result = run(exec_sql_csv)
                with open(output_path, 'w') as f:
                    f.write(result)

            elif 'excel' == env.format:
                puts(green('result as csv for excel (shift_jis)'))
                output_path = os.path.join(output_dir, '{}_sjis.csv'.format(output_name))
                result = run(exec_sql_csv)
                with open(output_path, 'w', encoding='shift_jis') as f:
                    f.write(result)

            else:
                raise ValueError('chose proper format: [txt, csv, excel]')

        except Exception as err:
            error('something wrong happened: {}'.format(err))

    puts('Bye')
