#!/usr/bin/env python

import argparse
import vcf
import sys
import pandas as pd
import numpy as np
import intervaltree

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='interval_filter_vcf.py',
                                     description='filter vcf file according to a bed file')
    parser.add_argument('interval_file')
    parser.add_argument('vcf_infile')
    args = parser.parse_args()

    intervals = pd.read_table(args.interval_file, header=None, dtype={0: str, 1: np.int32, 2: np.int32})
    intervals = intervals.rename(columns={0: 'chr', 1: 'start', 2: 'end'})
    trees = {}
    for chrom, interval in intervals.groupby('chr'):
        trees[chrom] = intervaltree.IntervalTree.from_tuples(zip(interval.start - 10, interval.end + 10))

    vcf_reader = vcf.Reader(open(args.vcf_infile, 'r'))
    vcf_reader.filters['targetInterval'] = vcf.parser._Filter(id='targetInterval',
                                                              desc='no overlap with intervals')
    vcf_writer = vcf.Writer(sys.stdout, vcf_reader)

    for record in vcf_reader:
        if record.CHROM not in trees:
            record.FILTER.append('targetInterval')
        else:
            query = trees[record.CHROM].search(record.POS)
            if len(query) == 0:
                record.FILTER.append('targetInterval')
        vcf_writer.write_record(record)

    vcf_writer.close()
