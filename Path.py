'''this module is used to manage the file in a specified path'''
import os
import sys

def SingleCopyPath(p):
    '''this function could get all the fasta filename in the specified SingleCopy dir'''
    # filenames = [x for x in os.listdir(p)]
    filenames = os.listdir(p)
    # print(filenames)

    return filenames


def BEDpath(p):
    '''this function could get all the BED filename in specified BED dir which is generated by JCVI
    e.g.
    python -m jcvi.formats.gff bed --type exon --key ID'''
    filenames = sorted(os.listdir(p))
    # print(filenames)

    return filenames


def Genelist(p):
    '''this function could grep all the gene list file'''
    filenames = os.listdir(p)
    lists = sorted([x for x in filenames if os.path.splitext(x)[-1] == '.list'])
    # print(lists)

    return lists


def ExonPath(p):
    '''this function is used to grep all the exon fasta in the specified dir
    Note: this version the exon and header-reformatted fasta should not be placed in the same dir'''
    filenames = os.listdir(p)
    lists = sorted([x for x in filenames if os.path.splitext(x)[-1] == '.fa'])
    print(lists)

    return lists


if __name__ == "__main__":
    pass
    # SingleCopyPath('tmp_data/Single_Copy_Orthologue_Sequences')
    # BEDpath(sys.argv[1])
    # Genelist('tmp_data/Output')
    ExonPath('tmp_data/')