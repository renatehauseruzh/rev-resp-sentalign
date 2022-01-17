import argparse
import json
import csv


def read_data(hyp_filename, gs_filename):

    with open(hyp_filename, 'r', encoding='utf-8') as hypf:
        hyp = json.load(hypf)

    with open(gs_filename, 'r', encoding='utf-8') as gsf:
        gs = json.load(gsf)

    return hyp, gs


# TODO: complete alignment: for every alignment, TP if exact same is in gs
def get_tp_fp_fn(hyp, gs):
    tp = 0
    fp = 0
    fn = 0
    for hyp_doc, gs_doc in zip(hyp, gs):
        # doc: {doc_id: id, review: [...], response: [...], alignment: [ ([...], [...]), ([...], [...]) ] }



        hyp_resp_aligned_sents = [i for sublist in [al[1] for al in hyp_doc['alignment']] for i in sublist] # --> [[...], [...]]
        hyp_rev_aligned_sents = [i for sublist in [al[0] for al in hyp_doc['alignment']] for i in sublist]

        gs_resp_aligned_sents = [i for sublist in [al[1] for al in gs_doc['alignment']] for i in sublist]
        gs_rev_aligned_sents = [i for sublist in [al[0] for al in gs_doc['alignment']] for i in sublist]

        # false positives: if a sentence is aligned in the hypothesis but not in the gold standard
        for hyp_rev_id in hyp_rev_aligned_sents:
            if hyp_rev_id not in gs_rev_aligned_sents:
                fp += 1
        for hyp_resp_id in hyp_resp_aligned_sents:
            if hyp_resp_id not in gs_resp_aligned_sents:
                fp += 1
        # false negatives: if a sentence is aligned in the gold standard but not in the hypothesis
        for gs_rev_id in gs_rev_aligned_sents:
            if gs_rev_id not in hyp_rev_aligned_sents:
                fn += 1
        for gs_resp_id in gs_resp_aligned_sents:
            if gs_resp_id not in hyp_resp_aligned_sents:
                fn += 1

        # partial+complete alignment
        for hyp_rev, hyp_resp in hyp_doc['alignment']:

            for gs_rev, gs_resp in gs_doc['alignment']:
                matching_rev = False
                for i in hyp_rev:
                    if i in gs_rev:
                        matching_ref = True
                        break
                # if there is no tuple in the gs where one of the review sentences occurs in a tuple, no partial match
                if not matching_rev:
                    continue
                # if there is a matching tuple where one of the rev sents occurs, check if also a matching resp exists
                for i in hyp_resp:
                    if i in gs_resp and matching_rev:
                        matching_rev = True
                        break
                if matching_rev:
                    tp += 1
    return tp, fp, fn


def complete_tp_fp_fn(hyp_al, gs_al):
    nr_of_als = 0
    tp, fp, fn = 0, 0, 0

    for al_pair in hyp_al:
        nr_of_als += 1
        # complete match
        if al_pair in gs_al:
            tp += 1
        else:
            fp += 1

    for al_pair in gs_al:
        if al_pair not in hyp_al:
            fn += 1

    return tp, fp, fn, nr_of_als


def partial_tp_fp_fn(hyp_al, gs_al):
    tp, fp, fn = 0, 0, 0

    # tp and fp: partial+complete alignment
    for hyp_rev, hyp_resp in hyp_al:
        matching_rev, matching_resp = False, False
        for gs_rev, gs_resp in gs_al:
            matching_rev = False
            for i in hyp_rev:
                if i in gs_rev:
                    matching_rev = True
                    break
            # if there is no tuple in the gs where one of the review sentences occurs in a tuple, no partial match
            if not matching_rev:
                #fp += 1
                continue
            # if there is a matching tuple where one of the rev sents occurs, check if also a matching resp exists
            matching_resp = False
            for i in hyp_resp:
                if i in gs_resp and matching_rev:
                    matching_resp = True
                    break

            if matching_rev and matching_resp:
                #tp += 1
                break
            #else:
            #    fp += 1
        if matching_rev and matching_resp:
            tp += 1
        else:
            fp += 1

    # false negatives: there is an alignment in the goldstandard that has no partial correspondence in the hypothesis
    for gs_rev, gs_resp in gs_al:
        matching_rev, matching_resp = False, False
        for hyp_rev, hyp_resp in hyp_al:
            matching_rev = False
            for i in gs_rev:
                if i in hyp_rev:
                    matching_rev = True
                    break
            # if there is no tuple in the gs where one of the review sentences occurs in a tuple, no partial match
            if not matching_rev:
                #fn += 1
                continue
            # if there is a matching tuple where one of the rev sents occurs, check if also a matching resp exists
            matching_resp = False
            for i in gs_resp:
                if i in hyp_resp:
                    matching_resp = True
                    break
            if matching_resp:
                break
                #fn += 1
        if not (matching_rev and matching_resp):
            fn += 1
    return tp, fp, fn

    # oder: wenn ein complete match dann tp,
    # wenn es keiner ist dann fp und
    # wenn es in der ref einen hat, der nicht in der hyp, dann ist es ein fn?


    # und für partial:
    # tp wenn ein teil der ref und der hyp übereinstimmen
    # fp wenn nichts übereinstimmt (kein paar von hyp rev&resp sent vorhanden, das auch in gs ist)
    # fn wenn in ref ein paar von rev&resp vorhanden, das keine entsprechung in hyp hat.



def tp_fp_fn(hyp, gs):
    comp_tp, comp_fp, comp_fn = 0, 0, 0
    part_tp, part_fp, part_fn = 0, 0, 0
    nr_of_als = 0

    for hyp_doc, gs_doc in zip(hyp, gs):

        hyp_al = hyp_doc['alignment']
        #print(gs_doc)
        gs_al = gs_doc['alignment']


        ctp, cfp, cfn, al_nr = complete_tp_fp_fn(hyp_al, gs_al)
        nr_of_als += al_nr
        comp_tp += ctp
        comp_fp += cfp
        comp_fn += cfn

        ptp, pfp, pfn = partial_tp_fp_fn(hyp_al, gs_al)
        part_tp += ptp
        part_fp += pfp
        part_fn += pfn

    return (comp_tp, comp_fp, comp_fn), (part_tp, part_fp, part_fn), nr_of_als


def p_r_f(tp, fp, fn, beta=1.0):
    try:
        precision = tp / (tp + fp)
    except ZeroDivisionError:
        precision = 0
    try:
        recall = tp / (tp + fn)
    except ZeroDivisionError:
        recall = 0

    try:
        fscore = ((1 + beta**2) * precision * recall) / (beta**2 * precision + recall)
        #fscore = (2 * tp) / (2 * tp + fp + fn)
    except ZeroDivisionError:
        fscore = 0
    return precision, recall, fscore


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--gs_file', required=True, help="path to the gold standard")
    parser.add_argument('--outfile', required=True, help="path to the file where the statistics should be stored")
    parser.add_argument('--hyp_files', type=str, nargs='+', help="list of paths to the sentence aligned evaluation files")
    parser.add_argument('--beta', type=float, default=1.0, help="beta value for the calculation of the fscore")

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    #print(args)
    #print(args.hyp_files)
    #print(args.gs_file)
    with open(args.outfile, 'w', encoding='utf-8') as outf:
        csv_writer = csv.writer(outf, delimiter=',')
        ngram_order = 0
        for hyp_file in args.hyp_files:
            # TODO: leere zeile wenn n-gram order sich verändert

            hyp, gs = read_data(hyp_file, args.gs_file)

            if hyp['meta']['n-gram order'] > ngram_order:
                csv_writer.writerow([])
                csv_writer.writerow(['n-gram order', hyp['meta']['n-gram order']])
                csv_writer.writerow(['threshold', 'comp_p', 'comp_r', 'comp_f', 'part_p', 'part_r', 'part_f'])

            ngram_order = hyp['meta']['n-gram order']
            threshold = hyp['meta']['threshold']

            hyp = hyp['alignment']
            #gs = gs['alignment']

            complete, partial, nr_of_als = tp_fp_fn(hyp, gs)

            comp_p, comp_r, comp_f = p_r_f(*complete, beta=args.beta)
            part_p, part_r, part_f = p_r_f(*partial, beta=0.5)

            # TODO: write results to csv file
            row = [threshold, comp_p, comp_r, comp_f, part_p, part_r, part_f, nr_of_als]
            csv_writer.writerow(row)


            #print(f"Complete Matches:\n------------\nPrecision: {comp_p}\nRecall: {comp_r}\nFscore: {comp_f}\n\n")
            #print(f"Partial Matches:\n------------\nPrecision: {part_p}\nRecall: {part_r}\nFscore: {part_f}")


if __name__ == '__main__':
    main()



            # complete alignments
            #if al in gs_doc['alignment'].values():
            #    tp += 1


    # TODO: partial alignment: TP if at least one rev and one resp are the same

    # TODO: FP if there is an alignment in file but not in gs

    # TODO: FN if there is no alignment in file but one in gs


