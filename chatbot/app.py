import subprocess
import wget
import os

from argparse import ArgumentParser
from os import path, environ, getenv


dirname = path.abspath(path.dirname(__file__))

BERT_CPU_PATH = path.join(dirname, './models/cdqa/bert_qa.joblib')
BERT_GPU_PATH = path.join(dirname, './models/cdqa/bert_qa_vGPU-sklearn.joblib')

TIKA_JAR_PATH       = path.join(dirname, './models/tika/tika-server.jar')
TIKA_JAR_MD5_PATH   = path.join(dirname, './models/tika/tika-server.jar.md5')

def get_bert_model(gpu_version=False):
    """Retrieve BEST CPU|GPU model if not exists in chatbot/models/cdqa/, and
    set an ENV VAR with model path.

    @params:
        gpu_version: bool -> flag to use GPU version of BERT model
    """
    dist_path = path.join(dirname, './models/cdqa/')

    environ['BERT_MODEL_PATH'] = str(BERT_GPU_PATH) if gpu_version else str(BERT_CPU_PATH)

    if (gpu_version and path.exists(BERT_GPU_PATH)):
        return

    if (not gpu_version) and path.exists(BERT_CPU_PATH):
        return

    MODEL_URL = 'https://github.com/cdqa-suite/cdQA/releases/download/bert_qa/bert_qa.joblib'
    if gpu_version == True:
        MODEL_URL = 'https://github.com/cdqa-suite/cdQA/releases/download/bert_qa_vGPU/bert_qa_vGPU-sklearn.joblib'
    
    try:
        wget.download(MODEL_URL, dist_path)
    except Exception as e:
        print("Can't Retrieve Bert Model: You can download it manually and add it to chatbot/models/cdqa through: {MODEL_URL}.")


def get_tika_jar():
    """Retrieve Tika JAR file if not exist in chatbot/models/tika, and set ENV
    VARS required by tika script."""
    dist_path = path.join(dirname, './models/tika/')

    if getenv('TIKA_SERVER_JAR', False):
        """Check if TIKA_SERVER_JAR set before to avoid download duplicate
        files."""
        return
    
    JAR_URL = 'https://repo1.maven.org/maven2/org/apache/tika/tika-server/1.19/tika-server-1.19.jar'
    JAR_MD5_URL = 'https://repo1.maven.org/maven2/org/apache/tika/tika-server/1.19/tika-server-1.19.jar.md5'

    if not path.exists(TIKA_JAR_PATH):
        try:
            print('>> Downloading Tika JAR.')
            wget.download(JAR_URL, path.join(dist_path, 'tika-server.jar'))
        except Exception as e:
            print("Can't Retrieve Tika JAR file: You can download it manually and add it to chatbot/models/tika through: {JAR_URL}")

    if not path.exists(TIKA_JAR_MD5_PATH):
        try:
            print('>> Downloading Tika JAR MD5.')
            wget.download(JAR_MD5_URL, path.join(dist_path, 'tika-server.jar.md5'))
        except Exception as e:
            print("Can't Retrieve Tika JAR file: You can download it manually and add it to chatbot/models/tika through: {JAR_URL}")

    environ['TikaJarPath']      = str(dist_path)
    environ['TIKA_PATH']        = str(dist_path)
    environ['TIKA_VERSION']     = str('1.19')
    environ['TIKA_SERVER_JAR']  = str(TIKA_JAR_PATH)
    environ['TIKA_LOG_PATH']    = str(path.join(dirname, './logs'))


def train_rasa():
    RASA_MODEL_PATH = path.abspath(path.join(dirname, './models/rasa-model.tar.gz'))
    if path.exists(RASA_MODEL_PATH):
        return
    print('>> Training RASA model')
    subprocess.call('rasa train --out ./models/ --fixed-model-name rasa-model --data ./framework/data/ --config ./framework/config.yml --domain ./framework/domain.yml', shell=True)
    
    if not path.exists(RASA_MODEL_PATH):
        raise 'Erorr while training RASA model.'
    return

def run(bert_gpu_version=False):

    get_bert_model(gpu_version=bert_gpu_version)

    rasa_server_process = subprocess.Popen("""rasa run --model ./models/rasa-model.tar.gz --endpoints ./framework/endpoints.yml --log-file ./logs/rasa-server.log -t abc --cors "*" --enable-api --credentials ./framework/credentials.yml""", shell=True)
    actions_server_process = subprocess.Popen("rasa run actions --actions framework.actions", shell=True)

    wait_process = [p.wait() for p in [rasa_server_process, actions_server_process]]

    print('>> Killing Processes')
    actions_server_process.kill()
    rasa_server_process.kill()

def run_gui():
    yarnv = subprocess.call("yarn -v", shell=True)
    if(yarnv):
        raise ValueError("""Error: you must install yarn package manager  
            install yarn from here: https://classic.yarnpkg.com/en/docs/install""")
    subprocess.Popen("cd gui && yarn install && yarn serve", shell=True)

if __name__ == "__main__":

    parser = ArgumentParser(description="CLI Interface For Chatbot Application")
    subparsers = parser.add_subparsers(help='commands')

    # run cli to start RASA server and action server together
    run_subparser = subparsers.add_parser('run', help='Start chatbot server and action server')
    run_subparser.set_defaults(command='run')
    run_subparser.add_argument('--gpu', action="store_true", default=False, help='Use BERT GPU model version')
    
    
    # preprocessing pdf parser cli
    parse_subparser = subparsers.add_parser('parse', help='Preprocess PDF file')
    parse_subparser.set_defaults(command='parse')
    parse_subparser.add_argument('--file', help='PDF document path to convert')
    parse_subparser.add_argument('--dest-dir', default='./assets/converted_documents', help='Directory path to cache parsing process')
    parse_subparser.add_argument('--name', help='PDF document name to store on desk')
    parse_subparser.add_argument('--include-line-breaks', action="store_true", default=False, help='if true PDFParser will merge small paragraphs together')

    args = parser.parse_args()

    if args.command == 'run':
        run_gui()
        train_rasa()
        run(args.gpu)

    if args.command == 'parse':
        get_tika_jar()

        # it must be imported here to avoid redownloading tika
        from preprocessing.pdfconverter import parse_pdf_and_save

        pdf_file = path.abspath(args.file)
        dest_dir = path.abspath(args.dest_dir)
        file_name = args.name
        include_line_breaks = args.include_line_breaks
        parse_pdf_and_save(file_path=pdf_file, dest_path=dest_dir, doc_name=file_name, include_line_breaks=include_line_breaks)



