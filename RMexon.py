import sys


def RmExon(ref_bed, multialignment):
    '''this function is used to remove exon matches from exon-intron-exon alignment
    Note: the input of this function are listed below
    1) BED file of the reference species
    2) multialignemnt output of SATe'''

    # Parse BED file to acquire the pos info
    input1 = open(ref_bed, 'r')
    dist_lst = []
    for line in input1:
            parsed_line = line.strip().strip('>').split('\t')
            dist_lst.append(int(parsed_line[2]) - int(parsed_line[1]) + 1)
    input1.close()
    # print(dist_lst)

    # Read multialignment 
    seqid_lst = []
    seq_lst = []
    tmp_str = ''
    with open(multialignment, 'r') as input2:
        for index, line in enumerate(input2):
            if ">" in line:
                seqid_lst.append(line.strip('\n'))
                seq_lst.append(tmp_str)
                tmp_str = ''
            else:
                tmp_str += line
        seq_lst.pop(0)
        seq_lst.append(tmp_str)
    input2.close()
    
    # for x in seq_lst:
    #     print('seq')
    #     print(x)
    # print(len(seq_lst))


    # Using reference species to conduct the analysis
    # Wrtie the after-cut multialignment
    # output = open('tmp_data/test_out.aln', 'w')
    # for i in range(len(seqid_lst)):
    #     join_seq = seqid_lst[i] + '\n' + seq_lst[i][dist_lst[0]:-dist_lst[1]] + '\n'
    #     output.write(join_seq)
    # output.close()

    for i in range(len(seqid_lst)):
        join_seq = seqid_lst[i] + '\n' + seq_lst[i][dist_lst[0]:-dist_lst[1]] + '\n'
        print(join_seq)




if __name__ == "__main__":
    RmExon(sys.argv[1], sys.argv[2])