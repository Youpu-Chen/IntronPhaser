import sys

def Parsepair(filename):
    '''this function is used to parse the exon pair'''

    # Set input file
    flag = False
    with open(filename, 'r') as input:
        for line in input:
            if flag == False:
                flag = True
            else:
                if not "None&None" in line:
                    parsed_line = line.rstrip().split('\t')
                    # print(parsed_line)
                    ref_id1 = parsed_line[0].split('&')[0]
                    ref_id2 = parsed_line[0].split('&')[1]
                    print('%s    %s' % (ref_id1, ref_id2))

                    # Parse id to save position info
                    chr = ref_id1.split('|')[2]
                    # print(chr)
                    start1 = ref_id1.split('|')[4]
                    end1 = ref_id1.split('|')[5]
                    start2 = ref_id2.split('|')[4]
                    end2 = ref_id2.split('|')[5]

                    part1 = ref_id1.split('|')[0]
                    part2 = ref_id1.split('|')[1]

                    part3 = ref_id2.split('|')[0]
                    part4 = ref_id2.split('|')[1]
                    
                    # with open('tmp_data/' + part1 + '_' + part2 + '.bed', 'w') as ouptut:
                    output = open(part1 + '_' + part2 + '.bed', 'w')
                    output.write(f'{chr}\t{start1}\t{end1}\t{part2}\n')
                    output.write(f'{chr}\t{start2}\t{end2}\t{part4}\n')
                    output.close()


    input.close()
if __name__ == "__main__":

    Parsepair(sys.argv[1])
