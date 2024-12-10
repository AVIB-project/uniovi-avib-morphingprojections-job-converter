import os
import sys
import time
import argparse
import logging

from datetime import date, datetime
from io import BytesIO

from pyaml_env import parse_config

import pandas as pd

import pyarrow as pa
import pyarrow.parquet as pq

from minio import Minio
from minio.error import MinioException

__author__ = "Miguel Salinas Gancedo"
__copyright__ = "Miguel Salinas Gancedo"
__license__ = "MIT"

_logger = logging.getLogger(__name__)

_client_minio = None

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
        "-organization-id",
        "--organization-id",
        dest="organization_id",
        help="Organization Id"
    )
    parser.add_argument(
        "-project-id",
        "--project-id",
        dest="project_id",
        help="Project Id"
    )
    parser.add_argument(
        "-case-id",
        "--case-id",
        dest="case_id",
        help="Case Id"
    )
    parser.add_argument(
        "-file-name",
        "--file-name",
        dest="file_name",
        help="File Name"
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

def connect_object_storage(config):
    global _client_minio

    _client_minio = Minio(config['minio']['host'] + ":" + str(config['minio']['port']),
        access_key=config['minio']['access_key'],
        secret_key=config['minio']['secret_key'],
        cert_check=False) 

def get_resource_dataframe(bucket, key):
    global _client_minio

    df_datamatrix = None
    try:
        _logger.info("Loading resource with name: %s ", bucket + "/" + key)

        response = _client_minio.get_object(bucket_name=bucket, object_name=key)

        df_datamatrix = pd.read_csv(response, header=[0], keep_default_na=False) 
    except MinioException as e:
        _logger.error(e)        

    return df_datamatrix

def convert_from_csv_to_parquet(dataframe):
    return pa.Table.from_pandas(dataframe)

def save_resource_datatable(bucket, key, data_table):
    global _client_minio

    # create the new key parquet name located in the same bucket
    key_tokens = key.split('.')
    key = key_tokens[0] + ".parquet"

    try:            
        _logger.info("Saving resource for name: %s ", bucket + "/" + key)

        buffer = BytesIO()
        pq.write_table(data_table, buffer)
        buffer.seek(0)        

        result = _client_minio.put_object(
            bucket_name=bucket, 
            object_name=key,
            data=buffer,
            length=buffer.getbuffer().nbytes,
            content_type="application/x-parquet")        
    except MinioException as e:
        _logger.error(e)        

    return result    

def main(args):
    # get arguments and configure app logger
    args = parse_args(args)
    setup_logging(args.loglevel)
    
    # get job arguments
    bucket = args.organization_id
    key = args.project_id + "/" + args.case_id + "/" + args.file_name

    # get job active profile            
    if not os.getenv('ARG_PYTHON_PROFILES_ACTIVE'):
        config = parse_config('./src/morphingprojections_job_converter/environment/environment.yaml')        
    else:
        config = parse_config('./src/morphingprojections_job_converter/environment/environment-' + os.getenv('ARG_PYTHON_PROFILES_ACTIVE') + '.yaml')

    _logger.info("Starting Job Converter")

    # STEP01: connect to minio object storage
    _logger.info("STEP01: Connect to minio")
    _client_minio = connect_object_storage(config)

    # STEP02: Get resource from object storage
    _logger.info("STEP02: Get resource from bucket %s and key %s", bucket, key)
    data_dataframe = get_resource_dataframe(bucket, key)
    
    # STEP03: Convert resource from csv to parquet
    _logger.info("STEP03: Convert resource from csv to parquet")
    data_table = convert_from_csv_to_parquet(data_dataframe)

    # STEP04: Save parquet resource to object storage
    _logger.info("STEP04: Save parquet resource to object storage")
    result = save_resource_datatable(bucket, key, data_table)

    _logger.info("Converter job finalized")

def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])

if __name__ == "__main__":
    run()
