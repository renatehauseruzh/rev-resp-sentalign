import csv
import argparse
from sklearn.metrics import cohen_kappa_score


def agreement_measure(infile):
    with open(infile, 'r', encoding='utf-8') as inf:
        reader = csv.reader(inf, delimiter=',')

        a1, a2 = [], []

        for line in reader:
            # skip empty formatting line
            if line == ['', '', '', '', '', '', ''] or not line:
                continue

            # get relevant data from line
            document_id = str(line[0])
            rev_sent_id = line[1]
            rev_sent = line[2]
            alignment_a2 = line[3] if line[3] else None
            alignment_a1 = line[4] if line[4] else None
            resp_sent_id = str(line[5]).lstrip('V') if line[5] else None
            resp_sent = line[6]

            # add alignment tuples to the annotators lists
            if alignment_a2:
                als = alignment_a2.split("; ")
                for al in als:
                    clean = al.lstrip('V').rstrip(";")
                    a2.append((rev_sent_id, clean))

            if alignment_a1:
                als = alignment_a1.split("; ")
                for al in als:
                    clean = al.lstrip('V').rstrip(";")
                    a1.append((rev_sent_id, clean))

    agr = agreement(a1, a2)
    return agr


def cohens_kappa(infile):
    with open(infile, 'r', encoding='utf-8') as inf:
        reader = csv.reader(inf, delimiter=',')

        labels_a1, labels_a2 = [], []
        rev_ids, resp_ids = [], []
        a1, a2 = [], []

        for line in reader:
            if 'REVIEW SENTID' in line:
                continue



            # a rev-resp pair is complete if such a formatting line is hit
            if line == ['', '', '', '', '', '', '', ''] or not line:
                # loop over all rev_sent/resp_sent pairs in a doc
                for rev_id in rev_ids:
                    for resp_id in resp_ids:
                        if (rev_id, resp_id) in a1:
                            labels_a1.append(1)  # aligned pair
                        else:
                            labels_a1.append(0)  # not-aligned pair
                        if (rev_id, resp_id) in a2:
                            labels_a2.append(1)
                        else:
                            labels_a2.append(0)
                # prepare for new document
                rev_ids, resp_ids = [], []
                a1, a2 = [], []
                continue
            else:
                # get relevant data from line
                rev_sent_id = line[1] if line [1] else None
                alignment_a2 = line[3] if line[3] else None
                alignment_a1 = line[4] if line[4] else None
                resp_sent_id = line[5] if line[5] else None

                if rev_sent_id:
                    rev_ids.append(rev_sent_id)
                if resp_sent_id:
                    resp_ids.append(resp_sent_id)

                # add alignment tuples to the annotators lists
                if alignment_a2:
                    als = alignment_a2.split("; ")
                    for al in als:
                        clean = al.lstrip('V').rstrip(";")
                        a2.append((rev_sent_id, clean))

                if alignment_a1:
                    als = alignment_a1.split("; ")
                    for al in als:
                        clean = al.lstrip('V').rstrip(";")
                        a1.append((rev_sent_id, clean))

    kappa = cohen_kappa_score(labels_a1, labels_a2)
    return kappa


def agreement(a1, a2):
    """
    Calculate the Agreement such as in Kruijff et al. 2006
    :param a1: list of all alignment tuples of annotator 1
    :param a2: list of all alignment tuples of annotator 2
    :return: float agreement score
    """
    I = 0
    for al in a1:
        if al in a2:
            I += 1

    A1 = len(a1)
    A2 = len(a2)

    agr = (2 * I) / (A1 + A2)

    return agr


# TODO: CLI

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--gs_file', required=True, help="path to the double annotated gold standard")
    parser.add_argument('--metric', required=True, choices=['cohens-k', 'agr'], help="path to the file where the statistics should be stored")

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    if args.metric == 'cohens-k':
        kappa = cohens_kappa(args.gs_file)
        print("Cohen's kappa: ", kappa)
    elif args.metric == 'agr':
        agr = agreement_measure(args.gs_file)
        print("AGR measure: ", agr)


if __name__ == '__main__':
    main()



