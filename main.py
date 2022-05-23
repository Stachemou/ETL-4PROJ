import os
import petl
import json
import requests
import coloredlogs, verboselogs, logging


verboselogs.install()
coloredlogs.install(fmt='%(asctime)s %(name)s %(levelname)s %(status_code)s %(message)s')
log = logging.getLogger('ETL')

