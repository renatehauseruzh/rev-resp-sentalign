import csv
import json
import argparse


class FormatConverter():

    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile

    def convert_data(self):
        with open(self.infile, 'r', encoding='utf-8') as inf:
            reader = csv.reader(inf, delimiter=',')

            docs = []
            doc_data, alignments, prov_alignments, respid2idx = {}, {}, {}, {}
            review, response = [], []

            for line in reader:
                # skip first line
                if 'REVIEW SENTID' in line:
                    continue
                # as soon as an empty dividing line is reached, the document is complete
                if line == ['', '', '', '', '', '', '']:
                    # create document and add it to list of documents
                    for rev, id_list in prov_alignments.items():
                        # map response sentIDs to response indices
                        idx_align = [respid2idx[i] for i in id_list]
                        alignments[rev] = idx_align
                    # construct document dict
                    doc_data['review'] = review
                    doc_data['response'] = response
                    doc_data['alignment'] = alignments
                    docs.append(doc_data)
                    # reset all collections for the new document
                    review, response = [], []
                    doc_data, alignments, prov_alignments, respid2idx = {}, {}, {}, {}

                else:
                    # get relevant data from line
                    document_id = str(line[0])
                    rev_sent_id = str(line[1]) if line[1] else None
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
                        # make a provisional mapping from rev idx to resp sentIDs
                        if alignment:
                            als = alignment.split("; ")
                            cleaned = []
                            for al in als:
                                clean = al.lstrip('V').rstrip(";")
                                cleaned.append(clean)
                            prov_alignments[str(len(review))] = cleaned
                    # if a new document starts, initialize new dict for document ID
                    else:
                        doc_data['doc_id'] = document_id
                        review.append(rev_sent)
                        response.append(resp_sent)
                        respid2idx[resp_sent_id] = len(str(response))
                        if alignment:
                            als = alignment.split("; ")
                            cleaned = []
                            for al in als:
                                clean = al.lstrip('V').rstrip(";")
                                cleaned.append(clean)
                            prov_alignments[str(len(review))] = cleaned
            return docs

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
