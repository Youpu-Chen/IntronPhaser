


import sys


def ConcatGblocks(filename):
    '''this function is used to concatenate the oupput file of Gblocks'''

    seq_ids = []
    seqs = []
    tmp_str = ''
    with open(filename, 'r') as input:
        for line in input:
            if ">" in line:
                seq_ids.append(line.rstrip())
                seqs.append(tmp_str)
                tmp_str = ''
            else:
                tmp_str += line.rstrip().replace(' ', '')
        seqs = seqs[1:]
        seqs.append(tmp_str)
    
    input.close()

    for x in range(len(seq_ids)):
        print(seq_ids[x])
        print(seqs[x])


if __name__ == "__main__":
    ConcatGblocks(sys.argv[1])