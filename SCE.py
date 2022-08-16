'''this module is used to parse the Single-Copy gene fasta from OrthoFinder2'''
from Bio import SeqIO
from Path import *
import os
from collections import defaultdict
import sys



def ParseFasta(filename):
    '''this function is used to parse the ipnut fasta file, but only save the ID for further analysis'''
    handle = open(filename, 'r')
    ID_list = [record.id for record in SeqIO.parse(handle, "fasta")]
    handle.close()
    # print(ID_list)

    return ID_list


def SCE(faintputpath, bedinputpath, outputpath):

    filenames1 = SingleCopyPath(faintputpath)
    filenames2 = BEDpath(bedinputpath)

    ### Part1: Generating the list of 
    # Create a list to save the gene ID
    genes = defaultdict(list)
    print(genes)

    # Read fa and save gene ID
    for fa in filenames1:
        for index, id in enumerate(ParseFasta(os.path.join(faintputpath, fa))):
            genes[filenames2[index]].append(id)
    # print(genes[8])
    # print(len(genes[6]))

    # Write gene list to outputpath
    for key in genes:
        with open(os.path.join(outputpath, (key.split('.')[0] + '.list')), 'w') as output:
            output.write('\n'.join(genes[key]))
        output.close()


    ### Part2: grep the exon ID based on the list pattern
    # Parse gff (already parsed by JCVI) to grep corresponding exon ID of each gene
    filename3 = Genelist(outputpath)
    for l in filename3:
        command = "grep -f %s %s > %s" % (str(os.path.join(outputpath, l)), str(os.path.join(bedinputpath, (l.split('.')[0] + '.bed'))), str(os.path.join(outputpath, (l.split('.')[0] + '.exon.bed'))))
        print(os.path.join(outputpath, l))
        print(command)
        os.system(command)



if __name__ == "__main__":
    # Test1
    # path = 'tmp_data/Single_Copy_Orthologue_Sequences/'
    # ParseFasta(path + 'OG0000043.fa')

    # Test2
    faintputpath = sys.argv[1] # 'tmp_data/Single_Copy_Orthologue_Sequences/'
    bedinputpath = sys.argv[2] # 'tmp_data/BED/'
    outputpath = sys.argv[3] # 'tmp_data/Output'
    SCE(faintputpath, bedinputpath, outputpath)

