import os
import sys
import math
import time
import argparse
import logging

from datetime import date, datetime
from io import StringIO, BytesIO
from pyaml_env import parse_config

import numpy as np
import pandas as pd

from mongoengine import connect, disconnect
from mongoengine.queryset.visitor import Q
from bson.objectid import ObjectId

from minio import Minio
from minio.error import MinioException

import pyarrow as pa
import pyarrow.parquet as pq

__author__ = "Miguel Salinas Gancedo"
__copyright__ = "Miguel Salinas Gancedo"
__license__ = "MIT"

_logger = logging.getLogger(__name__)

# MongoDB parameters
_MONGODB_DATABASE = "configuration"

def argument_spaces(arg):
    return arg.split(',')

def parse_args(args):   
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Format Converter Job")
    parser.add_argument(
        "-bucket",
        "--bucket",
        dest="bucket",
        help="File Bucket"
    )
    parser.add_argument(
        "-key",
        "--key",
        dest="key",
        help="File Key"
    )             
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )   
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )

    return parser.parse_args(args)

def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )

def main(args):
    """Wrapper allowing :func:`training` to be called with string arguments in a CLI fashion

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``[ "--case-id", "65cdc989fa8c8fdbcefac01e"]``).
    """
    # get arguments and configure app logger
    args = parse_args(args)
    setup_logging(args.loglevel)
    
    # get job arguments
    case_id = args.case_id
    spaces = args.spaces

    _logger.info("Projection for buket id: " + case_id + " and spaces: " + ','.join(spaces))

    # get job active profile            
    if not os.getenv('ARG_PYTHON_PROFILES_ACTIVE'):
        config = parse_config('./src/morphingprojections_job_converter/environment/environment.yaml')        
    else:
        config = parse_config('./src/morphingprojections_job_converter/environment/environment-' + os.getenv('ARG_PYTHON_PROFILES_ACTIVE') + '.yaml')

    _logger.info("Starting converter job")

    # STEP01: get case from case identifier from mongodb database
    _logger.info("STEP01: Get case from case indentifier %s ", case_id)
    
    _logger.info("Converter job finalized")

def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])

if __name__ == "__main__":
    run()
