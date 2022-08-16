'''this module is applied to reformat the header of seqkit-extracted fasta'''
from collections import defaultdict
from Bio import SeqIO
import re
import os
from Path import ExonPath
import sys


def RFHeader(inputpath, outputpath, filename, sortedfilename):
    '''this function is used to reformat the sequence ID of a specified fasta'''
    # Read fasta, and reformat the header
    gene_dict = defaultdict(list)
    handle = open(os.path.join(inputpath, filename), 'r')
    for record in SeqIO.parse(handle, 'fasta'):
        # print(record.id)
        # print(vars(record))

        geneid = record.description.split(' ')[-1]
        # Using re to grep start and end position of exon
        pos_p = re.compile(r'([0-9]+)-([0-9]+)')
        start = pos_p.search(record.id).group(1)
        end = pos_p.search(record.id).group(2)
        # print(exonid)
        # print(f'{start} {end}')
        
        chr = record.id.replace(f'_{start}-{end}', '').split(':')[0]
        # print(chr)

        strand_sym = record.id.replace(f'_{start}-{end}', '').split(':')[1]
        # print(strand_sym)
        if strand_sym == "+":
            strand = "1"
        elif strand_sym == "-":
            strand = "-1"
        else:
            strand = "."
        
        # Reformat the header
        record.id = f"{geneid}|{chr}|{start}|{end}|{strand}"
        gene_dict[geneid].append([record.id, record.seq]) # .seq is a unchangeble object

    handle.close()
    # print(gene_dict.items())
    

    # Output reformatted fasta
    with open(os.path.join(outputpath, sortedfilename), 'w') as output:
        # Define lambda function to sort the exon
        exonLocation = lambda x:int(x[0].split('|')[2])
        
        # Reformat the record id and assign exon ID
        for key in list(gene_dict.keys()):
            # records = sorted(gene_dict.items(), key = exonLocation)
            records = sorted(gene_dict[key], key = exonLocation)
            # print(records)
            # print(len(records))
            for id in range(len(records)):
                records[id][0] = "%s|%s|%s|%s|%s|%s|%s" % (records[id][0].split('|')[0], 
                                                        records[id][0].split('|')[0],
                                                        records[id][0].split('|')[1],
                                                        records[id][0].split('|')[0] + '.' + str(id + 1),
                                                        records[id][0].split('|')[2],
                                                        records[id][0].split('|')[3],
                                                        records[id][0].split('|')[4])
            # print(records)
            gene_dict[key] = records
            
        for key in list(gene_dict.keys()):
            records = gene_dict[key]
            for record in records:
                output.write(">" + record[0] + '\n' + str(record[1]) + '\n')
    output.close()


def main():
    inputpath = sys.argv[1]
    outputpath = sys.argv[2]
    filenames = ExonPath(inputpath)
    # Using a loop to reformat original exon fasta
    for fa in filenames:
        print(f"{fa}\t{fa.replace('.singlecopy.exon.fa', '_exon')}")
        RFHeader(inputpath, outputpath, fa, fa.replace('.fa', '_exon'))
    




if __name__ == "__main__":
    # RFHeader('tmp_data', 'tmp_data', 'test.fa', 'test.rfmt.fa')
    
    main()
    '''
    inputpath is the input path of seqkit-extracted exon fasta
    outputpath is the output path of reformatted exon fasta
    Note: pattern of the input filename for Introngettng should be 'Species_exon'
    '''

