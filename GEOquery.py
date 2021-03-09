import os
import sys

def download(url, paths):
    destination = os.path.join(*paths)
    if not os.path.isfile(destination):
        os.system(f'wget "{url}" -O {destination}')
    else:
        print(f"File already exists. Skipping file: {paths[-1]}")

def get_samples(url):
    import os
    file_path = 'temp_file.temporary'
    os.system(f'wget "{url}" -O temp_file.temporary')
    return file_path

def remove_file(path):
    os.remove(path)

def create_dir(paths):
    try:
        os.mkdir(os.path.join(*paths))
    except FileExistsError:
        print("Folder already exists")
    except FileNotFoundError:
        os.mkdir(paths[0])
        create_dir(paths)

class GEOquery:
    download_dir: str
    accession: str
    query_args: dict
    acc_page: str
    def __init__(self, geo, destination):
        self.accession = geo
        self.download_dir = destination
        self.acc_page = "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi"
        self.query_args = { "self": {"text": ["full", "data"], "xml": ["full", "data"]},
                            "gse": {"text": ["full", "data"], "xml": ["full", "data"]}, #series
                            "gpl": {"text": ["full", "data"]}, #platform
                            "gsm": {"text": ["full", "data"]}, #samples
                            "all": {"text": ["full", "data"]}} #family
        create_dir((self.download_dir, self.accession))

    def query(self, targ="gsm", form="text", view="full"):
        try:
            if self.query_args[targ][form].index(view) == -1:
                self._invalid_arguments()
        except:
            self._invalid_arguments()
        url = f'{self.acc_page}?acc={self.accession}&targ={targ}&form={form}&view={view}'
        download(url, (self.download_dir, f"{self.accession}.txt"))

    def _sample_query(self, accession):
        url = f'{self.acc_page}?acc={accession}&targ=gsm&form=text&view=full'
        download(url, (self.download_dir, self.accession, f"{accession}.txt"))

    def load_samples(self):
        url = f"{self.acc_page}?acc={self.accession}&targ=self&form=text&view=full"
        temp_file = get_samples(url)
        with open(temp_file) as samples_file:
            for line in samples_file:
                if line.startswith("!Series_sample_id"):
                    yield line.split(' = ')[1].rstrip()
        remove_file(temp_file)

    def _invalid_arguments(self):
        raise ValueError("Invalid query arguments")

destination = sys.argv[1]

acc_list = []
with open('data/accessions.txt') as acc_file:
    for line in acc_file:
        acc = line.rstrip()
        acc_list.append(acc)

for geo_accession in acc_list:
    geo = GEOquery(geo_accession, destination)
    for sample in geo.load_samples():
        geo._sample_query(sample)