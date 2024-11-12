# PARADIM Algorithm Integration Guide

PARADIM (Medical image annotation, reuse and analysis platform) is a platform to power AI in health, particularly for medical images and radiotherapy data. This guide provides the technical steps to integrate your algorithm into PARADIM.

## Key Concepts

* **Dockerized Algorithms:** To ensure data security, your algorithm must be packaged as a Docker image, which will be executed on PARADIM servers. This means the data never leaves the PARADIM environment.
* **DICOM Format:** PARADIM exclusively uses the DICOM format. This standard provides rich metadata for tracking and maintaining data integrity (who, when, where, how), aligning with FAIR principles. DICOM is also the standard format for clinical data in real-world settings.
* **DICOM Output:** Your algorithm must read DICOM files and produce output in DICOM format.

Contact us at [paradim@ulaval.ca](mailto:paradim@ulaval.ca) for any questions or assistance.

## Preparing Your Algorithm

Your algorithm must be packaged in a Docker image. Docker provides portability and ensures your algorithm runs consistently within the PARADIM environment. If you're new to Docker, this is a good starting point: [https://www.geeksforgeeks.org/how-to-run-a-python-script-using-docker/](https://www.geeksforgeeks.org/how-to-run-a-python-script-using-docker/)

Your Docker image should be executable as follows:

```shell
docker run <your-image:TAG> ./dicom-in ./dicom-out <series-instance-uid> \
         -v ./tmp-path-in-paradim-cluster:./dicom-in \
         -v ./tmp-path-out-paradim-cluster:./dicom-out
```

The docker image must accept 3 arguments (here `./dicom-in`, `./dicom-out` and the `<series-instance-uid>`), 
where the first is the path where your container will find the DICOM files of the input series/study,
where the second corresponds to the path of the directory where the results in DICOM format must be written, 
and where the third is the SeriesInstanceUID of the DICOM input that triggered the run 
(Note that you can ignore this third argument in your docker image).
Input data will be in subdirectories, so your code should be able to parse data recursively.

Also, the Docker image must contain every thing, and your code should be able to run as stand alone without Internet.

_FYI, the `./tmp-path-in/out-paradim-cluster` are the paths where the actual data is on the PARADIM cluster._
_When testing your docker image locally, replace these paths with ones which that contain data on your machine._


## Example

This repository contains an example

### Requirements 
- Docker
- Unzip (to retrieve example data)
- Clone this git repository

### Retrieve example data from orthanc demo server (do it once)
```shell
mkdir -p $PWD/data && mkdir -p $PWD/out && curl  https://orthanc.uclouvain.be/demo/series/52f4cb90-29d1d1a2-2ca34edd-4b8851fc-8cb269f2/archive \
--output $PWD/data/my_ct.zip && unzip -o  $PWD/data/my_ct.zip -d $PWD/data/
```

### Build docker image
```shell
docker build -t paradim_example .
```

### Run docker image
```shell
docker run --rm -v $PWD/data:/paradim_in -v $PWD/out/:/paradim_out paradim_example /paradim_in /paradim_out \
1.3.6.1.4.1.14519.5.2.1.2193.7172.215111709746721743805035350686
```


## Uploading and register your Docker image to PARADIM
### 1. Upload the Docker image to the registry
At this step we assume that you have built your Docker own image. 

The next step aims to connect to the Docker registry of Université Laval, 
tag your Docker image and finally push it (Note that you can use dockerhub).

To login into the Docker registry (credentials will be provided by PARADIM staff):
```shell
$ docker login <TOKEN> <REGISTRY-URL>
```

Then, tag your built Docker image:
```shell
$ docker tag <DOCKER-IMAGE-ID> <REGISTRY-URL>/<image-name>:<TAG>
```

And Finally, push your tagged image to the registry:
```shell
$ docker push <REGISTRY-URL>/<image-name>:<TAG>
```

Note : Your token will be able to push to a specific image name.

### 2. Register the uploaded Docker image in PARADIM
At this moment, only the PARADIM staff can do this. 
Leave us a message and we will happily register your image in PARADIM  [paradim@ulaval.ca,](mailto:paradim@ulaval.ca) :)

## Launching your Docker image
Once your algorithm is uploaded to PARADIM, it should be accessible here https://launcher.paradim.science/.
Select the desired algorithm, album/studies/series and submit your runs!
Note that you need to be on the Université Laval VPN to have access to the launcher.


