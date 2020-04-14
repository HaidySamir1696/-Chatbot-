# QA-System

## Installation

### Virtual Enviroment
1. install conda
2. cd 'project-folder'
3. conda create --prefix ./venv python=3.7 pip
4. conda activate ./venv
5. pip install -r requirements.txt

### Models

#### CDQA
download models to './models/cdqa/': [https://github.com/cdqa-suite/cdQA/releases](https://github.com/cdqa-suite/cdQA/releases)


#### Allennlp
download models to './models/allennlp/': [https://storage.googleapis.com/allennlp-public-models/bidaf-model-2020.02.10-charpad.tar.gz](https://storage.googleapis.com/allennlp-public-models/bidaf-model-2020.02.10-charpad.tar.gz)



#### Tika
- Tika jar:   [https://repo1.maven.org/maven2/org/apache/tika/tika-server/1.9/tika-server-1.9.jar](https://repo1.maven.org/maven2/org/apache/tika/tika-server/1.9/tika-server-1.9.jar)
- Tika jar md5:   [https://repo1.maven.org/maven2/org/apache/tika/tika-server/1.9/tika-server-1.9.jar.md5](https://repo1.maven.org/maven2/org/apache/tika/tika-server/1.9/tika-server-1.9.jar.md5)
- tika env vars:
    - export TikaJarPath='/path-to-tika-folder/'
    - export TIKA_LOG_PATH='/path-to-tika-folder/'
    - export TIKA_PATH='/path-to-tika-folder/'
    - export TIKA_VERSION='1.9'
    - export TIKA_SERVER_JAR='/path-to-tika-folder/tika-server.jar'


