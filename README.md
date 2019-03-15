## MultiLoc2
### Bioinformatics tool for predicting subcellular localizations of eukaryotic proteins

Travis CI  
[![Build Status](https://travis-ci.org/KohlbacherLab/MultiLoc2.svg?branch=master)](https://travis-ci.org/KohlbacherLab/MultiLoc2)  

This repository mainly provides a containerized installation of MultiLoc2 using Docker.  
Most of the required depdendencies are directly installed in the Docker image.  
In order to install the software elsewhere please read the instructions in the  
[README](MultiLoc2/README) file of the MultiLoc2 source folder and have a look in the Dockerfile.  


**Citing & Further Information**  

If you use MultiLoc2 please cite the following publications:

Blum T., Briesemeister S., and Kohlbacher O. (2009)  
[MultiLoc2: integrating phylogeny and Gene Ontology terms improves subcellular protein localization prediction.](https://doi.org/10.1186/1471-2105-10-274)  
BMC Bioinformatics, 10:274
  
  
**Requirements**  

- Linux OS
- Docker
- InterProScan (optional)


**Installation**

The easiest option is to build the Docker image from this repository using the following steps:  
` $ git clone https://github.com/KohlbacherLab/MultiLoc2.git`  
` $ docker build --no-cache -t <your_image_name> MultiLoc2/`  

**MultiLoc2 Usage (Interactively in container)**  

MultiLoc2 general usage:  
` $ sh /MultiLoc2/run_multiloc2.sh <fasta_file> <origin> <predictor> <result_file> <go_file>`  

**Use InterProScan**  
In order to use InterProScan you nee a separate installation.  
You the have to mount the InterProScan installation directory to some place into the docker container.  
Inside the container please export the environment variable INTERPROSCAN and set it to the mounted directory.  

Example:  
` docker run --rm -it -v <path_to_host_interproscan>:<container_mount_point> multiloc2 /bin/bash`  
` root@be2eb1efa8c8:/# export INTERPROSCAN=<container_mount_point>`  

Now run MultiLoc2, which should internally use InterProScan now.






