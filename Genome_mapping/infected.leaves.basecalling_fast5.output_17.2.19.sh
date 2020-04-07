#To perform basecalling on infectedleaves_day7

nohup guppy_basecaller -i ../fast5/20200207_infectedleaves_3.fast5 -s ./20200207_infectedleaves_3.fastq -c dna_r9.4.1_450bps_hac.cfg --device auto --records_per_fastq 0 --recursive --fast5_out &

#nohup guppy_basecaller -i ../fast5/20200116_infectedleaves_2.fast5 -s ./20200116_infectedleaves_2.fastq -c dna_r9.4.1_450bps_hac.cfg --device auto --records_per_fastq 0 --recursive --fast5_out &

#nohup guppy_basecaller -i ../fast5/20191212_infectedleaves_1.fast5 -s ./20191212_infectedleaves_1.fastq -c dna_r9.4.1_450bps_hac.cfg --device auto --records_per_fastq 0 --recursive --fast5_out &
