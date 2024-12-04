[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)

# Description

> Uniovi AVIB Morphing Projection Job Converter.

## Scaffolding your python project:

```
$ putup --markdown uniovi-avib-morphingprojections-job-converter -p morphingprojections_job_converter \
      -d "Uniovi AVIB Morphing Projection Job Converter Service." \
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
pip install tox
pip install pyaml-env
pip install mongoengine
pip install minio
pip install pandas
pip install pyarrow
```

Installation your python pipeline packages in your virtual environment in development mode:

```
pip freeze > requirements.txt
```

# Docker

build image for local environment:

```
docker build -t uniovi-avib-morphingprojections-job-converter:1.1.0 .

docker tag uniovi-avib-morphingprojections-job-converter:1.1.0 avibdocker.azurecr.io/uniovi-avib-morphingprojections-job-converter:1.1.0

docker push avibdocker.azurecr.io/uniovi-avib-morphingprojections-job-converter:1.1.0
```

build image for local minikube environment:

```
docker build --build-arg ARG_PYTHON_PROFILES_ACTIVE=minikube -t uniovi-avib-morphingprojections-job-converter:1.1.0 .

docker tag uniovi-avib-morphingprojections-job-converter:1.1.0 avibdocker.azurecr.io/uniovi-avib-morphingprojections-job-converter:1.1.0

docker push avibdocker.azurecr.io/uniovi-avib-morphingprojections-job-converter:1.1.0
```

build image for avib environment:

```
docker build --build-arg ARG_PYTHON_PROFILES_ACTIVE=avib -t uniovi-avib-morphingprojections-job-converter:1.1.0 .

docker tag uniovi-avib-morphingprojections-job-converter:1.1.0 avibdocker.azurecr.io/uniovi-avib-morphingprojections-job-converter:1.1.0

docker push avibdocker.azurecr.io/uniovi-avib-morphingprojections-job-converter:1.1.0
```

Execute job locally for a case_id 65cdc989fa8c8fdbcefac01e:

```
docker run --rm uniovi-avib-morphingprojections-job-converter:1.1.0 python src/morphingprojections_job_converter/service.py --bucket 65cd021098d02623c46da92d --key 65cd02d9e6ba3947be825ac8/673cd073190c686d772d7bfa/datamatrix.csv
```

## Note

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.