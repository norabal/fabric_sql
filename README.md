# FabricSql

## Description

Get sql execution result as .txt and csv(UTG-8 or shift_jis for excel format).
Available for python3.6+


***DEMO:***

![result](https://github.com/norabal/fabric_sql/blob/media/demo.gif)

## Requirement

- Python 3.6.6 or above

## Installation

    $ git clone https://github.com/norabal/fabric_sql

if you have anaconda...

    $ conda create -n fabric_sql python=3.6 pip
    $ conda activate fabric_sql
    $ pip install -r requirements.txt

if you don't...

    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt

After the above processes, do following these steps.

- Copy config.ini.sample as 'config.ini'.
- Edit 'config.ini'
- Write sql on 'exec.py'.
- Execute remote_sql task with set keys.

## Usage

<img src="https://github.com/norabal/fabric_sql/blob/media/demo01.gif" data-canonical-src="https://github.com/norabal/fabric_sql/blob/media/demo01.gif" width="580" />

<img src="https://github.com/norabal/fabric_sql/blob/media/demo02.gif" data-canonical-src="https://github.com/norabal/fabric_sql/blob/media/demo02.gif" width="580" />

<img src="https://github.com/norabal/fabric_sql/blob/media/demo03.gif" data-canonical-src="https://github.com/norabal/fabric_sql/blob/media/demo03.gif" width="580" />

<img src="https://github.com/norabal/fabric_sql/blob/media/demo04.gif" data-canonical-src="https://github.com/norabal/fabric_sql/blob/media/demo04.gif" width="580" />

### Result Examples

text file:  
<img src="https://github.com/norabal/fabric_sql/blob/media/demo05.gif" data-canonical-src="https://github.com/norabal/fabric_sql/blob/media/demo05.gif" width="580" />

csv file:  
<img src="https://github.com/norabal/fabric_sql/blob/media/demo06.gif" data-canonical-src="https://github.com/norabal/fabric_sql/blob/media/demo06.gif" width="580" />

excel file:  
<img src="https://github.com/norabal/fabric_sql/blob/media/demo07.gif" data-canonical-src="https://github.com/norabal/fabric_sql/blob/media/demo07.gif" width="580" />


if you want to extract sql result from staging environment with csv format for excel.

    $ fab --set dest=stg,format=excel remote_sql

## Author

[norabal](https://twitter.com/norabalwks)

## License

[MIT](http://b4b4r07.mit-license.org)
