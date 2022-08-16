'''this module is applied to seq extract based on seqkit
Note: Thus you should've already install seqkit to your env'''
import os
import sys
# import datetime


def ParaSubseq(inputpath, fapath, outputpath):
    '''this function run seqkit to extract exon fasta'''

    # Singlecopy exon version
    BED_list = [x for x in os.listdir(inputpath) if os.path.splitext(x)[-1] == ".bed"]

    with open('seqkit.commands', 'w') as output:
        for x in BED_list:
            command = "seqkit subseq --bed %s %s -o %s\n" % (os.path.join(inputpath, x), 
                                                            os.path.join(fapath, (x.split('.')[0]+'.fa')),
                                                            os.path.join(outputpath, (x.split('.')[0]+'.singlecopy.exon.fa')))
            print(command)
            output.write(command)



if __name__ == "__main__":
    # ParaSubseq('tmp_data/Output', 'tmp_data/Genome', 'tmp_data/Exon_of_SingleCopy')
    path_of_exonbed = sys.argv[1]
    path_of_genome = sys.argv[2]
    path_of_exonseq = sys.argv[3]
    ParaSubseq(path_of_exonbed, path_of_genome, path_of_exonseq)
