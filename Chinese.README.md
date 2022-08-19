# IntronPhaser「暂定」

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



## 从OrthoFinder2的分析结果中提取single-copy exon

将`Single_Copy_Orthologue_Sequences`文件夹复制到当前工作目录，

### （1）single-copy exon BED文件的生成

首先，需要使用JCVI获取下述形式的exon BED文件，

```shell
python -m jcvi.formats.gff bed --type exon --key Parent input.gff > output.exon.bed
```

### （2）运行`SCE.py` 进行single-copy exon BED提取

```shell
# e.g.
python SCE.py <Single_copy_Results_from_OrthoFinder2> <BED_byJCVI> <BED_exon>
```

### （3）运行`Seq.py`进行序列提取

```shell
# e.g.
python Seq.py <BED_of_singlecopy_exon> <Path_to_Genome> <Sequene_of_Single_Copy_exon>
```

### （4）序列ID重编码

Introngetting所要求的形式，

`Gene stable ID|Gene name|Chromosome/scaffold name|Exon stable ID|Genomic coding start|Genomic coding end|strand`

```shell
python Formats.py <Sequene_of_Single_Copy_exon> <Sequene_of_Reformatted_Single_Copy_exon>
```



## Introngetting运行

Note: Introngetting is based on Python2

```shell
python2 PATH/get_EPIC.py <Exon_dir> <Genome_dir> <Reference_Species_Name> <Number_of_Threads>
```

完成运行之后，切换至`<Exon_dir>/Results`目录，获取所有gene均存在的序列文件，

```shell
seqkit stats *.fas | awk '{if($4==9) print $1}' > retained.config
```



## [SATé](https://phylo.bio.ku.edu/software/sate/sate.html)运行

```shell
conda activate py2.7

cat retained.config | while read id
do
	python /home/chphl/biosoft/satesrc-v2.2.7-2013Feb15/sate-core/run_sate.py --auto -i $id
done
```

结果以`.aln`结尾。



## 去除多序列比对结果中的exon序列

Note：以blast对冲中心物种的exon长度作为参考

```shell
cd Exon_dir/xml/Coverage0.60_Identity0.70/two_way_blast_orthologs/
python3 Parsepair.py exon_pair.txt  # results with .bed suffix
```

将上一步得到的BED文件与`.aln`文件放置于同一文件夹下，

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



## 物种树构建

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

