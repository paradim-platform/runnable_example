# PARADIM tech documentation

[PARADIM](https://pararim.science) (_Plateforme d'annotation, de réutilisation et d'analyse d'images médicales_, or Medical image annotation, reuse and analysis platform)
is a platform to power AI in health, in particular on images and radiotherapy related data.

This document aims to provide a technical guide to users who wish to integrate their algorithm into the platform.

## Key concepts

- The data never leaves the PARADIM environment.
  - Users must provide their algorithm in a Docker image which will be run on PARADIM servers.

- The only supported data format is __DICOM__.
    - The DICOM standard has a very rich metadata system, 
      which allows us to trace/keep data in a clean way (who, when, where, how) in the spirit of the FAIR principles.
    - Also, it is in this form that clinical data will be accessible "_in the real world_".

- Algorithms have to be a docker image that read DICOM files and __output DICOM files__

If you need help/have questions on the following steps, 
do no hesitate to contact us at [paradim@ulaval.ca](mailto:paradim@ulaval.ca)

## Preparing your algorithm
Your algorithm must be packaged in a Docker image. 
If you don't know how to package your algorithm in a Docker image, 
this can be a good starting point https://www.geeksforgeeks.org/how-to-run-a-python-script-using-docker/.

Your Docker image should be executable as:
```shell
$ docker run <your-image:TAG> ./dicom-in ./dicom-out <series-instance-uid> \
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


## Uploading and register your Docker image to PARADIM
### 1. Upload the Docker image to the registry
At this step we assume that you have built your Docker image. 

The next step aims to connect to the Docker registry of Université Laval, 
tag your Docker image and finally push it (Note that you can use dockerhub).

To login into the Docker registry:
```shell
$ docker login <REGISTRY-URL> --username <your-email@ulaval.ca>
```

Then, tag your built Docker image:
```shell
$ docker tag <DOCKER-IMAGE-ID> <REGISTRY-URL>/<image-name>:<TAG>
```

And Finally, push your tagged image to the registry:
```shell
$ docker push <REGISTRY-URL>/<image-name>:<TAG>
```

#### Example
There is an example for a TotalSegmentator Docker image:
```shell
$ docker login registre.apps.ul-pca-pr-ul01.ulaval.ca --username gacou54@ulaval.ca
$ docker tag 19fcc4aa71ba registre.apps.ul-pca-pr-ul01.ulaval.ca/total-segmentator:0.1.0
$ docker push registre.apps.ul-pca-pr-ul01.ulaval.ca/total-segmentator:0.1.0
```


### 2. Register the uploaded Docker image in PARADIM
At this moment, only the PARADIM staff can do this. 
Leave us a message and we will happily register your image in PARADIM  [paradim@ulaval.ca,](mailto:paradim@ulaval.ca) :)

## Launching your Docker image
Once your algorithm is uploaded to PARADIM, it should be accessible here https://launcher.paradim.science/.
Select the desired algorithm, album/studies/series and submit your runs!
Note that you need to be on the Université Laval VPN to have access to the launcher.



# Requirements 
- Docker
- Unzip (to retrieve example data)

# Build docker image
```shell
docker build -t paradim_example .
```

# Retrieve example data from orthanc demo server
```shell
mkdir -p $PWD/data && mkdir -p $PWD/out && curl  https://orthanc.uclouvain.be/demo/series/52f4cb90-29d1d1a2-2ca34edd-4b8851fc-8cb269f2/archive \
--output $PWD/data/my_ct.zip && unzip -o  $PWD/data/my_ct.zip -d $PWD/data/
```


# Run docker image
```shell
docker run --rm -v $PWD/data:/paradim_in -v $PWD/out/:/paradim_out paradim_example /paradim_in /paradim_out \
1.3.6.1.4.1.14519.5.2.1.2193.7172.215111709746721743805035350686
```
