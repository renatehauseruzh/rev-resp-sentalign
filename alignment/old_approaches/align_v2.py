import csv
import argparse
import similarity_v2


class Aligner():
    # only one instance of this should be created at the beginning of the process

    def __init__(self, threshold):
        self.threshold = threshold
        self.uaid = 100000 # schauen, mit welcher zahl das initialisiert werden soll

    def extract_alignments(self, sim_matrix):
        """
        for a given similarity matrix of a document, extract the alignments
        :param sim_matrix: dict of format {revsent_id1: {resp_id1: sim1, resp_id2: sim2}, revsent_id2: {...} }
        :return: dicts with sentence IDs as keys and alignment IDs as values?
        """
        candidates = self._get_candidates(sim_matrix=sim_matrix)

        # format of alignments: [(rev_id1, resp_id2), (rev_id1, resp_id3), (rev_id2, resp_id4)]
        buckets = []
        while candidates:
            # get first element in the list
            el = candidates.pop(0)

            # if only one element was left, this forms a bucket by itself
            if len(candidates) == 0:
                bucket = el
                leftover = []
            # put all alignments that have either same resp_id or rev_id than first element into a bucket
            #bucket = [(rev, resp) for (rev, resp) in candidates if rev == el[0] or resp == el[1]]
            else:
                bucket = [el]
                leftover = []
                for rev, resp in candidates:
                    if rev == el[0] or resp == el[1]:
                        bucket.append((rev, resp))
                    else:
                        leftover.append((rev, resp))

                # save bucket to a list
                buckets.append(bucket)
                # only keep on searching in candidates that don't belong to any bucket yet
                candidates = leftover


        rev_sents = {}
        resp_sents = {}
        for bucket in buckets:
            # each bucket gets a unique alignment ID
            self.uaid += 1

            for alignment in bucket:
                rev_sents[alignment[0]] = self.uaid
                resp_sents[alignment[1]] = self.uaid
        self._refresh_uaid()
        return rev_sents, resp_sents

    def _get_candidates(self, sim_matrix):
        """
        Get all rev-resp pairs that have a similarity above the specified threshold
        :param sim_matrix: dict of format {revsent_id1: {resp_id1: sim1, resp_id2: sim2}, rev_sent_id2: {...}}
        :return alignments: list of format [(rev_id1, resp_id2), (rev_id1, resp_id3), (rev_id2, resp_id4)]
        """
        alignments = []
        for rev_sent_id, responses in sim_matrix.items():

            for resp_sent_id, sim in responses.items():
                if sim >= self.threshold:
                    alignments.append((rev_sent_id, resp_sent_id))
        return alignments

    def _refresh_uaid(self):
        """
        Go to new % 10 for each document, i.e. when one alignment process is done
        """
        if (self.uaid % 10) != 0:
            rest = 10 - (self.uaid % 10)
            self.uaid += rest


class Document():

    def __init__(self, doc_data):
        # doc data format: {'doc_id': docid, 'rev': {revid1: rev1, revid2: rev2}, 'resp': {respid1: resp1, respid2: resp2} }
        self.id = doc_data['doc_id']
        self.rev_ids = list(doc_data['rev'].keys())
        self.resp_ids = list(doc_data['resp'].keys())
        self.rev_sents = doc_data['rev']  # mapping review id / review sent
        self.resp_sents = doc_data['resp']  # mapping response id / response sent

    def _get_similarity_matrix(self):
        ...

    def _get_alignments(self):
        ...

    def pad_sent_ids(self):
        """
        Pad the shorter text so that review and response have the same length
        :return padded_rev_ids, padded_resp_ids: lists of ids that have the same length
        """
        padded_rev_ids = self.rev_ids[:]
        padded_resp_ids = self.resp_ids[:]
        if len(self.rev_ids) != len(self.resp_ids):
            # pad review document
            if len(self.rev_ids) < len(self.resp_ids):
                i = len(self.rev_ids)
                while i < len(self.resp_ids):
                    padded_rev_ids.append('')
                    i += 1
            # pad response document
            elif len(self.rev_ids) > len(self.resp_ids):
                i = len(self.resp_ids)
                while i < len(self.rev_ids):
                    padded_resp_ids.append('')
                    i += 1
        return padded_rev_ids, padded_resp_ids


###########################################################################################
# UTILITY FUNCTIONS FOR READING AND WRITING FILES
###########################################################################################


def read_data(filename):
    """
    Read in data from file and create a Document object for each document
    :param filename: file path to the sentence split corpus file
    :yield: Document object
    """
    with open(filename, 'r', encoding='utf-8') as inf:
        reader = csv.reader(inf, delimiter='\t')
        doc_data = {}
        for line in reader:
            # as soon as an empty dividing line is reached, the document is complete
            #print(line)
            if not line:
                #print('reached')
                # create document and yield it
                doc = Document(doc_data=doc_data)
                doc_data = {}
                yield doc

            else:
                # get relevant data from line
                document_id = str(line[0])
                rev_sent_id = str(line[1]) if line[1] else None
                rev_sent = line[2]
                resp_sent_id = str(line[4]) if line[4] else None
                resp_sent = line[5]

                # add all sentences of one document to the dictionary entry of the document ID
                if 'doc_id' in doc_data.keys() and document_id == doc_data['doc_id']:
                    if rev_sent_id is not None:
                        doc_data['rev'][rev_sent_id] = rev_sent
                    if resp_sent_id is not None:
                        doc_data['resp'][resp_sent_id] = resp_sent
                # if a new document starts, initialize new dict for document ID
                else:
                    doc_data['doc_id'] = document_id
                    doc_data['rev'] = {rev_sent_id: rev_sent}
                    doc_data['resp'] = {resp_sent_id: resp_sent}
                    # doc_data[document_id] = {'rev': {rev_sent_id: rev_sent}, 'resp': {resp_sent_id: resp_sent}}


def create_rows(doc, rev_alignments, resp_alignments):

    # ensure the two lists have the same length so that they align nicely in the tsv document
    padded_rev_ids, padded_resp_ids = doc.pad_sent_ids()
    rows = []
    for rev_id, resp_id in zip(padded_rev_ids, padded_resp_ids):
        # add all information to the row
        rev_uaid = rev_alignments[rev_id] if rev_id in rev_alignments.keys() else ''
        resp_uaid = resp_alignments[resp_id] if resp_id in resp_alignments.keys() else ''
        rev_sent = doc.rev_sents[rev_id] if rev_id in doc.rev_sents.keys() else ''
        resp_sent = doc.resp_sents[resp_id] if resp_id in doc.resp_sents.keys() else ''
        row = [doc.id, rev_id, rev_sent, rev_uaid, resp_id, resp_sent, resp_uaid]
        rows.append(row)
    return rows


###########################################################################################
# COMMAND LINE INTERFACE
###########################################################################################


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('infile', help="path to the sentence segmented file")
    parser.add_argument('outfile', help="path to the file with the similarity matrices")
    #parser.add_argument('--out-format', choices=['tsv', 'json'], default='json')
    parser.add_argument('--ngram-order', type=int, default=6)  # default=6 in Popovic, 2015
    parser.add_argument('--threshold', type=float, default=0.5) # TODO: has to be investigated

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    aligner = Aligner(args.threshold)
    simc = similarity_v2.Similarity(args.ngram_order)

    # generator
    data = read_data(args.infile)

    with open(args.outfile, 'w', newline='', encoding='utf-8') as outf:
        # headers
        tsv_writer = csv.writer(outf, delimiter='\t')
        tsv_writer.writerow(['DOCID', 'REVIEW SENTID', 'REVIEW SENT', 'REVIEW UAID', 'RESPONSE SENTID', 'RESPONSE SENT',
                             'RESPONSE UAID'])
        for doc in data:

            # calculate similarities for each sentence pair in the doc
            similarities = simc.calculate_similarities(doc=doc)

            # extract alignments
            rev_alignments, resp_alignments = aligner.extract_alignments(sim_matrix=similarities)

            # write extracted alignments to
            rows = create_rows(doc, rev_alignments, resp_alignments)
            #tsv_writer.writerows(rows)
            for row in rows:
                tsv_writer.writerow(row)
            tsv_writer.writerow('')


if __name__ == '__main__':
    main()










##########################################################
# id_bucket = []
#             for i in range(0, len(candidates)):
#                 rev = candidates[i][0]
#                 resp = candidates[i][1]
#                 if rev == el[0] or resp == el[1]:
#                     id_bucket.append(i)
#
#             for id in id_bucket:
#                 pair = candidates[id]
#                 bucket.append(pair)
#
#             for id in id_bucket:
#                 candidates.remove(id)
#             bucket.append(el)