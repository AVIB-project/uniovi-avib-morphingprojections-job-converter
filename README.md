[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)

# Description

> Uniovi AVIB Morphing Projection Job Converter.

## Scaffolding your python project:

```
$ putup --markdown uniovi-avib-morphingprojections-job-converter -p morphingprojections_job_converter \
      -d "Uniovi AVIB Morphing Projection Job Converter." \
      -u https://dev.azure.com/gsdpi/avib/_git/uniovi-avib-morphingprojections-job-converter
```

Create a virtual environment in you python project and activated it:

```
$ cd uniovi-avib-morphingprojections-job-converter

$ python3 -m venv .venv 

$ source .venv/bin/activate
(.venv) miguel@miguel-Inspiron-5502:~/git/uniovi/uniovi-avib-morphingprojections-job-converter$
```

## Dependencies

```
$ pip install -e .
```

```
$ pip install tox
$ pip install pyaml-env
$ pip install pandas
$ pip install pyarrow
$ pip install minio
```

Installation your python pipeline packages in your virtual environment in development mode:

```
$ pip freeze > requirements.txt
```

# Docker

build image for local minikube environment:

```
docker build -t morphingprojections-job-converter:1.1.0 .

docker tag morphingprojections-job-converter:1.1.0 gsdpi/morphingprojections-job-converter:1.1.0

docker push gsdpi/morphingprojections-job-converter:1.1.0
```

build image for avib environment:

```
docker build --build-arg ARG_PYTHON_PROFILES_ACTIVE=avib -t morphingprojections-job-converter:1.1.0 .

docker tag morphingprojections-job-converter:1.1.0 gsdpi/morphingprojections-job-converter:1.1.0

docker push gsdpi/morphingprojections-job-converter:1.1.0
```

Execute job locally for a case_id 65cdc989fa8c8fdbcefac01e:

```
docker run --rm uniovi-avib-morphingprojections-job-converter:1.1.0 python src/morphingprojections_job_converter/service.py --organization-id  65cd021098d02623c46da92d --project-id 65cd05c798d02623c46da92e --case-id 65cdc989fa8c8fdbcefac01e --file-name datamatrix.csv
```

## Note

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.