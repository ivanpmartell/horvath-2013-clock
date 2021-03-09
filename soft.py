def get_ids(file_path, ids):
    with open(file_path) as sample:
        reading_table = False
        table_line = 0
        for line in sample:
            if line.startswith('!sample_table_begin'):
                reading_table = True
                table_line = 0
            elif line.startswith('!sample_table_end'):
                reading_table = False
            elif reading_table:
                table_line += 1
                if table_line == 1:
                    continue
                k, _ = line.split('\t')
                key = k.strip()
                ids.add(key)

class SampleSoft:
    accessions: dict

    def __init__(self):
        self.accessions = dict()
        
    def load_file(self, file_path):
        with open(file_path) as sample:
            current_acc = ""
            reading_table = False
            table_line = 0
            for line in sample:
                if line.startswith('^'):
                    current_acc = line.split(' = ')[1].strip()
                    self.accessions[current_acc] = dict()
                elif line.startswith('!'):
                    try:
                        temp = line.index('=')
                    except ValueError:
                        if line.startswith('!sample_table_begin'):
                            reading_table = True
                            table_line = 0
                        elif line.startswith('!sample_table_end'):
                            reading_table = False
                            yield current_acc
                        continue
                    key, val = line.split(' = ')
                    prop = key[key.index('_')+1:].strip()
                    try:
                        extra_properties = val.index(':')
                        secondary_prop = val[:extra_properties].split(' ')[0].strip()
                        secondary_value = val[extra_properties+1:].strip()
                        try:
                            self.accessions[current_acc][prop][secondary_prop] = secondary_value
                        except:
                            self.accessions[current_acc][prop] = {secondary_prop: secondary_value}
                    except ValueError:
                        value = val.strip()
                        try:
                            self.accessions[current_acc][prop]['value'] = value
                            print(f"WARNING: Overwriting property ({prop}) with value: {value}")
                        except:
                            self.accessions[current_acc][prop] = {'value': value}
                if reading_table:
                    if table_line == 0:
                        try:
                            self.accessions[current_acc]['table_headers']['value'] = line.strip()
                            print("Overwriting table_headers. This should not happen (the file might be malformed)")
                            raise ValueError()
                        except KeyError:
                            self.accessions[current_acc]['table_headers'] = {'value': line.strip()}
                            self.accessions[current_acc]['table'] = dict()
                    else:
                        #Save table data
                        line_split = line.split('\t')
                        k = line_split[0]
                        v = line_split[1]
                        key = k.strip()
                        value = v.strip()
                        if value == 'null':
                            value = '0'
                        self.accessions[current_acc]['table'][key] = value
                    table_line += 1

    def get_data(self, id_dict, geo_accession):
        label = -1.
        try:
            label = float(self.accessions[geo_accession]['characteristics_ch1']['age'].split(' ')[0])
        except:
            print("WARNING: MISSING AGE")
        gender = self.accessions[geo_accession]['characteristics_ch1']['gender'].lower()
        arr = [0.0 for i in range(len(id_dict))]
        for k, _ in id_dict.items():
            arr[id_dict[k]] = float(self.accessions[geo_accession]['table'][k])
        return arr, label, gender

#print(soft.accessions['GSM989827']['table'])
#print(soft.accessions['GSM989827']['characteristics_ch1']['age'])