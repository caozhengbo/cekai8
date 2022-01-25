
import os
import shutil
import subprocess
import sys
import tempfile

from test_runner import models

from test_runner.utils import loader
from cekai8.settings import BASE_DIR

EXEC = sys.executable

if 'uwsgi' in EXEC:
    EXEC = "/usr/bin/python3"


class DebugCode(object):

    def __init__(self, code, project, filename):
        self.__code = code
        self.resp = None
        self.temp = tempfile.mkdtemp(prefix='tempHttpRunner', dir=os.path.join(BASE_DIR, 'tempWorkDir'))
        self.project = project
        self.filename = filename

    def run(self):
        """ dumps file.py and run
        """
        try:
            os.chdir(self.temp)
            files = models.PycodeModel.objects.filter(project__id=self.project)
            for file in files:
                file_path = os.path.join(self.temp, file.name)
                print(file_path)
                loader.FileLoader.dump_python_file(file_path, file.code)

            testdata_files = models.ModelWithFileFieldModel.objects.filter(project__id=self.project)
            for testdata in testdata_files:
                testdata_path = os.path.join(self.temp, testdata.name)
                myfile_path = os.path.join(BASE_DIR, 'media', str(testdata.file))
                loader.FileLoader.copy_file(myfile_path, testdata_path)
            run_file_path = os.path.join(self.temp, self.filename)

            self.resp = decode(subprocess.check_output([EXEC, run_file_path], stderr=subprocess.STDOUT, timeout=60))

        except subprocess.CalledProcessError as e:
            self.resp = decode(e.output)

        except subprocess.TimeoutExpired:
            self.resp = 'RunnerTimeOut'

        os.chdir(BASE_DIR)
        shutil.rmtree(self.temp)


def decode(s):
    try:
        return s.decode('utf-8')

    except UnicodeDecodeError:
        return s.decode('gbk')
