# IntronPhaser pipeline for genome phasing

## Prerequisite

Before conducting genome phasing analysis, there are some requirements,

```shell
# Env1
# install JCVI previously
conda install -c bioconda jcvi
conda install seqkit

# Env2 -> Python2.7
conda create -n py2.7 python=2.7
wget -c --no-check-certificate http://phylo.bio.ku.edu/software/sate/downloads2/src/satesrc-v2.2.7-2013Feb15.tar.gz
cd /biosoft/satesrc-v2.2.7-2013Feb15/sate-core
sudo python setup.py develop

git clone https://github.com/chenmy33/IntronGetting.git
```

and due to the Introngetting was based on Python 2, you should make sure Python2-installation.



## Extract single-copy exon from result of OrthoFinder2

Note: After you finish the OrthoFinder2 analysis, you'll have a dir named `Single_Copy_Orthologue_Sequences` under  Results dir.

We're gonna use that to perform the later analysis.

### (1) Generate the BED file of exon

Before using the scripts in this repo, preparing BED file of all exon using JCVI.

```shell
python -m jcvi.formats.gff bed --type exon --key Parent input.gff > output.exon.bed
```



### (2) Run `SCE.py` to extract to BED of single-copy exon

```shell
# e.g.
python SCE.py <Single_copy_Results_from_OrthoFinder2> <BED_byJCVI> <BED_exon>
```



### (3) Run `Seq.py` to extract sequence of single-copy exon

```shell
# e.g.
python Seq.py <BED_of_singlecopy_exon> <Path_to_Genome> <Sequene_of_Single_Copy_exon>
```



### (4) Reformat

Note: The header of exon fasta should be like,

`Gene stable ID|Gene name|Chromosome/scaffold name|Exon stable ID|Genomic coding start|Genomic coding end|strand`

```shell
python Formats.py <Sequene_of_Single_Copy_exon> <Sequene_of_Reformatted_Single_Copy_exon>
```



## Introngetting

Note: Introngetting is based on Python2

```shell
python2 PATH/get_EPIC.py <Exon_dir> <Genome_dir> <Reference_Species_Name> <Number_of_Threads>
```

Now, just change working dir to `<Exon_dir>/Results`

```shell
seqkit stats *.fas | awk '{if($4==9) print $1}' > retained.config
```



## MultiAlignment using [SATé](https://phylo.bio.ku.edu/software/sate/sate.html)

```shell
conda activate py2.7

cat retained.config | while read id
do
	python /home/chphl/biosoft/satesrc-v2.2.7-2013Feb15/sate-core/run_sate.py --auto -i $id
done
```

The result has `.aln` as suffix.



## Remove exon sequences to Save Multialignment only contain intron

Note: Using the exon length of blast-centor species as reference.

```shell
cd Exon_dir/xml/Coverage0.60_Identity0.70/two_way_blast_orthologs/
python3 Parsepair.py exon_pair.txt  # results with .bed suffix
```

Then, place SATé alignment results and BED of exon pair in the same dir,

```shell
ls *.bed | sort -t "_" -k5.1 > bed.config
ls *.aln | sort -t "_" -k5.1 > aln.config
paste bed.config aln.config > config

cat config | while read id
do
	arr=($id)
	bed=${arr[0]}
	aln=${arr[1]}
	name=${bed%.*}
	# echo "python RMexon.py $bed $aln > rmexon.${name}.aln"
	python3 RMexon.py $bed $aln > rmexon.${name}.aln
done

# Using Gblocks to save only conservative regions
ls ../remove_exon/rmexon.* | > rmexon.config
cat rmexon.config | while read id
do 
	cp $id ./
	aln=${id##*/}
	# echo $aln
	Gblocks $aln -t=d -b5=h -e=
done

ls *<suffix> > blocks.config
cat blocks.config | while read id
do
	python3 Concatgblocks.py $id > $id.fasta
done
```



## RAxML and ASTRAL

```shell
mkdir Tree_of_RAxML
cp -r <PATH_to_SATéAlignment>/*.fasta ./
ls * > config

# 1.
dir=/home/chphl/biosoft/raxml/bin
cat config | while read id
do
	echo "$dir/raxmlHPC -p 12345 -x 12345 -s $id -n ${id} -f a -# 100 -m GTRGAMMA" >> raxml_para.commandlines
done
# Run ParaFly
ParaFly -c raxml_para.commandlines -CPU 10 &

# 2.
mkdir Tree_of_ASTRAL
cp -r <PATH_to_Tree_of_RAxML>/*bestTree* ./
cat * > in.tree
adir=/biosoft/Astral
java -jar $adir/astral.5.7.8.jar -i in.tree -o out.tree
```

