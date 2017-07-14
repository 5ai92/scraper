import logging
import mammoth
import os
import shutil
import time
import yaml


logging.basicConfig(level=logging.INFO)

class Step:

    def __init__(self, doc):
        self.doc = doc
        self.pth = os.path.abspath('..')

    @staticmethod
    def working_dir():
        pth = os.path.abspath('..')
        if os.path.exists('{}/results_dir'.format(pth)):
            shutil.rmtree('{}/results_dir'.format(pth))             #removing the directory before executing the process.
        if not os.path.exists('{}/results_dir'.format(pth)):
            os.makedirs('{}/results_dir'.format(pth))

    @property
    def docx_to_html(self):
        with open(self.doc, 'r') as f:
            html_result = mammoth.convert_to_html(self.doc)
            logging.debug("Finished converting {} to html file".format((self.doc.split('/')[-1]).split('.')[0]))
            # output_data = self.working_dir(html_result.value)
            file_pth = '{0}/results_dir/{1}.html'.format(self.pth, (self.doc.split('/')[-1]).split('.')[0])
            with open(file_pth, 'w+') as f:
                f.write(html_result.value)

    def soso(self):
        logging.debug("Finished soso")
        pass


# decorator to calculate the entire process time
def timetaken(some_function):
    t1 = time.time()
    def wrapper_function(*args, **kwargs): 
        some_function(*args, **kwargs)
        t2 = time.time()
        t3 = t2-t1
        logging.info("Process finished in {} seconds".format(t3.__round__(2)))
    return wrapper_function


@timetaken
def main():    # This is the main method that we are going to trigger.
    try:
        with open('pass.yaml', 'r') as f:
            data = yaml.safe_load(f)
            list_of_todo = data['load']
            Step.working_dir()
            for todo in list_of_todo:
                # functions to be executed are:
                logging.info('starting to {}'.format(todo['step']))
                docs = todo['docs']
                for doc in docs:
                    getattr(Step(doc), todo['action'])

    except Exception as e:
        print ("There is an error {}".format(str(e)))

if __name__ == "__main__":
    main()

