import sys
import python

pydef download(url: str, paths: tuple[str]):
    import os
    destination = os.path.join(*paths)
    if not os.path.isfile(destination):
        os.system(f'wget "{url}" -O {destination}')
    else:
        print(f"File already exists. Skipping file: {paths[-1]}")

pydef get_samples(url: str) -> str:
    import os
    file_path = 'temp_file.temporary'
    os.system(f'wget "{url}" -O temp_file.temporary')
    return file_path

pydef remove_file(path: str):
    import os
    os.remove(path)

pydef create_dir(paths: tuple[str]):
    import os
    try:
        os.mkdir(os.path.join(*paths))
    except FileExistsError:
        print("Folder already exists")

class GEOquery:
    download_dir: str
    accession: str
    query_args: dict[str,dict[str,list[str]]]
    acc_page: str
    def __init__(self: GEOquery, geo: str, destination: str):
        self.accession = geo
        self.download_dir = destination
        self.acc_page = "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi"
        self.query_args = { "self": {"text": ["full", "data"], "xml": ["full", "data"]},
                            "gse": {"text": ["full", "data"], "xml": ["full", "data"]}, #series
                            "gpl": {"text": ["full", "data"]}, #platform
                            "gsm": {"text": ["full", "data"]}, #samples
                            "all": {"text": ["full", "data"]}} #family
        create_dir((self.download_dir, self.accession))

    def query(self: GEOquery, targ="gsm", form="text", view="full"):
        try:
            if self.query_args[targ][form].index(view) == -1:
                self._invalid_arguments()
        except:
            self._invalid_arguments()
        url = f'{self.acc_page}?acc={self.accession}&targ={targ}&form={form}&view={view}'
        download(url, (self.download_dir, f"{self.accession}.txt"))

    def _sample_query(self: GEOquery, accession: str):
        url = f'{self.acc_page}?acc={accession}&targ=gsm&form=text&view=full'
        download(url, (self.download_dir, self.accession, f"{accession}.txt"))

    def load_samples(self: GEOquery):
        url = f"{self.acc_page}?acc={self.accession}&targ=self&form=text&view=full"
        temp_file = get_samples(url)
        with open(temp_file) as samples_file:
            for line in samples_file:
                if line.startswith("!Series_sample_id"):
                    yield line.split(' = ')[1].rstrip()
        remove_file(temp_file)

    def _invalid_arguments(self: GEOquery):
        raise ValueError("Invalid query arguments")

geo_accession = sys.argv[1]
destination = sys.argv[2]
geo = GEOquery(geo_accession, destination)
geo.load_samples() |> geo._sample_query()