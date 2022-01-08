import csv
import json
import argparse


class FormatConverter():

    def __init__(self, infile, outfile, delimiter=','):
        self.infile = infile
        self.outfile = outfile
        self.delimiter = delimiter

    def convert_data(self):
        with open(self.infile, 'r', encoding='utf-8') as inf:
            reader = csv.reader(inf, delimiter=self.delimiter)

            docs = []
            doc_data, alignments, respid2idx = {}, {}, {}
            review, response, al_tups = [], [], []

            for line in reader:
                print(line)
                # skip first line
                if 'REVIEW SENTID' in line:
                    continue
                # as soon as an empty dividing line is reached, the document is complete: create document
                if line == ['', '', '', '', '', '', ''] or not line:
                    # create alignment dict
                    alignments = self._create_alignment_dict(al_tups, respid2idx)
                    # construct document dict
                    doc_data['review'] = review
                    doc_data['response'] = response
                    doc_data['alignment'] = alignments
                    docs.append(doc_data)
                    # reset all collections for the new document
                    review, response, al_tups = [], [], []
                    doc_data, alignments, respid2idx = {}, {}, {}
                else:
                    # get relevant data from line
                    document_id = str(line[0])
                    rev_sent = line[2]
                    alignment = line[3] if line[3] else None
                    resp_sent_id = str(line[4]).lstrip('V') if line[4] else None
                    resp_sent = line[5]

                    # add all sentences of one document to the dictionary entry of the document ID
                    if 'doc_id' in doc_data.keys() and document_id == doc_data['doc_id']:
                        # only append to lists if there exists a sentence on the current line
                        if rev_sent:
                            review.append(rev_sent)
                        if resp_sent:
                            response.append(resp_sent)
                        # conversion from sentID to index can only be done when all responses have been read in
                        if resp_sent_id:
                            respid2idx[resp_sent_id] = str(len(response))
                        # add each alignment tuple to al_tups
                        if alignment:
                            als = alignment.split("; ")
                            cleaned = []
                            for al in als:
                                clean = al.lstrip('V').rstrip(";")
                                # add every alignment tuple rev, resp to a list
                                al_tups.append((str(len(review)), clean))

                            #prov_alignments[str(len(review))] = cleaned
                    # if a new document starts, initialize new dict for document ID
                    else:
                        # add each alignment tuple to al_tups
                        doc_data['doc_id'] = document_id
                        review.append(rev_sent)
                        response.append(resp_sent)
                        respid2idx[resp_sent_id] = str(len(response))
                        if alignment:
                            als = alignment.split("; ")
                            cleaned = []
                            for al in als:
                                clean = al.lstrip('V').rstrip(";")
                                #cleaned.append(clean)
                                al_tups.append((str(len(review)), clean))
                            #prov_alignments[str(len(review))] = cleaned
            return docs

    def _create_alignment_dict(self, al_tups, respid2idx):
        alignments = {}
        buckets = []
        while al_tups:
            # get first element in the list
            el = al_tups.pop(0)
            # if only one element was left, this forms a bucket by itself
            if len(al_tups) == 0:
                bucket = [el]
                buckets.append(bucket)
                leftover = []
            # put all alignments that have either same resp_id or rev_id than first element into a bucket
            # bucket = [(rev, resp) for (rev, resp) in al_tups if rev == el[0] or resp == el[1]]
            else:
                bucket = [el]
                leftover = []
                for rev, resp in al_tups:
                    if rev == el[0] or resp == el[1]:
                        bucket.append((rev, resp))
                    else:
                        leftover.append((rev, resp))
                buckets.append(bucket)
                # only keep on searching in candidates that don't belong to any bucket yet
                al_tups = leftover
        # adding buckets to alignments dict
        i = 1
        for bucket in buckets:
            #print(bucket)
            aid = str(i)
            alignments[aid] = {'review': [], 'response': []}
            for rev, resp in bucket:
                if rev not in alignments[aid]['review']:
                    alignments[aid]['review'].append(rev)
                if respid2idx[resp] not in alignments[aid]['response']:
                    alignments[aid]['response'].append(respid2idx[resp])
            i += 1
        return alignments  # dict: {'id1': {'review': [i1, i2, i3], 'response': [i3, i5]}, 'id2': {...} }

    def write_data(self, data):
        with open(self.outfile, 'w', encoding='utf-8') as outf:
            json.dump(data, outf, indent=4)

    def convert(self):
        data = self.convert_data()
        self.write_data(data)


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('infile', help="path to the raw goldstandard file")
    parser.add_argument('outfile', help="path to the new goldstandard tsv file")

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    converter = FormatConverter(infile=args.infile, outfile=args.outfile)
    converter.convert()


if __name__ == '__main__':
    main()
