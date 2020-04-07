# Mapping to reference genome ##7/12/19##

#mapping first round
# %.* removes one thing from right at a time whereas %% removes 2 things at a time (extensions)
for file in *.fastq;
do
minimap2 -ax map-ont chr_A_B_unassigned.fasta $file >${file%.*}.sam
done

#Minimap2 seamlessly works with FASTA (.fa), FASTQ (.fq /.fastq) and gzip'd (.gz) formats as input.
#-a >output in sam format
#--sam-hit-only >only include mapped reads in the output sam
#-ax map-ont >map long noisy Oxford Nanopore reads

for sam in *.sam;
do
samtools flagstat $sam >${sam%.*}.map.flagstat.txt
done

#remove sam files as we have our flagstat files with correct map%
rm *.sam

#mapping this time do with sam-hit-only
for file in *.fastq;
do
minimap2 -ax map-ont --sam-hit-only chr_A_B_unassigned.fasta $file >${file%.*}.hitonly.sam
done

#convert to bam (converting sam to bam)
for sam in *.sam;
do
samtools view -S -b $sam >${sam%.*}.unsorted.bam
done

#this will convert bam into sorted bam

for bam in *.bam;
do 
samtools sort $bam >${bam%%.*}.sorted.bam
done

#unsorted bam has no use, delete
rm *.unsorted.bam

#NanoStat now possible with a sorted .bam
for bam in *.sorted.bam;
do
NanoStat --bam $bam >${bam}.Nanostat.txt
done

#NanoStat on fastq for comparison
for fastq in *.fastq;
do
NanoStat --fastq $fastq >${fastq}.Nanostat.txt
done

