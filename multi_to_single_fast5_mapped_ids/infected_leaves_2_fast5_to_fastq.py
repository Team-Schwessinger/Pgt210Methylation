import os
from ont_fast5_api.fast5_interface import get_fast5_file
from ont_fast5_api.analysis_tools.basecall_1d import Basecall1DTools
import time
from multiprocessing import Pool, Process
from joblib import Parallel, delayed


def fast5s_to_fastq(dir_):
    print(dir_)
    start = time.time()
    plus = '+'
    fastq_fn = os.path.join(os.path.join(dir_), os.path.basename(dir_) + '.fastq')
    fast5s = [os.path.join(dir_ ,x) for x in os.listdir(dir_) if x.endswith('.fast5') ]
    n  = []
    s  = []
    q  = []
    
    for fast5_fn in fast5s:
        with get_fast5_file(fast5_fn, mode='r') as f5:
            with Basecall1DTools(f5) as basecall:
                n1, s1, q1 = basecall.get_called_sequence('template')
                n.append(n1)
                s.append(s1)
                q.append(q1)
    with open(fastq_fn, mode='w') as fastq_fh:
        for (n1, s1, q1) in zip(n, s, q):
            print('@%s' % n1, file=fastq_fh)
            print(s1, file=fastq_fh)
            print(plus, file=fastq_fh)
            print(q1, file=fastq_fh)
    string = '%s done' % fastq_fn
    stop = time.time()
    string = string + ': Done in {:.2f}'.format(stop - start)
    print(string)
    return string

if __name__ == '__main__':
    #BAMIN_DIR = '../../analyses/mapping/infected_leaves/infected_leaves_2/'
    #FAST5IN_DIR = '../../data/genomic_data/infected_leaves/workspace_fast5/infected_leaves_2_fast5_out/'
    #FAST5singleIN_DIR = '../../analyses/single_fast5s/infected_leaves/infected_leaves_2_fast5_single_fast5/'
    #OUT_DIR = '../../analyses/single_fast5s/infected_leaves/infected_leaves_2_mapped_single_fast5/'
    n_threads = 20


    BAMIN_DIR = os.path.abspath(BAMIN_DIR)
    FAST5IN_DIR = os.path.abspath(FAST5IN_DIR)
    OUT_DIR = os.path.abspath(OUT_DIR)
    FAST5singleIN_DIR = os.path.abspath(FAST5singleIN_DIR)


    single_fast5_count = 0
    dirs = []
    for direcotry in (os.path.join(FAST5singleIN_DIR, x) for x in os.listdir(FAST5singleIN_DIR) if os.path.isdir(os.path.join(FAST5singleIN_DIR, x))):
        dirs.append(direcotry)
        fast5s = [os.path.join(direcotry ,x) for x in os.listdir(direcotry) if x.endswith('.fast5')]
        single_fast5_count += len(fast5s)
    dirs.sort()
    print('This is the amount of single fast5s %s' % single_fast5_count)
    print(len(dirs))
    #for i in range(len(dirs)):
        #p = Process(target=fast5s_to_fastq, args=(dirs[0]))
        #p.start()
        #p.join()
    
    #exit()
    with Pool(processes=n_threads) as pool:
        pool.map(fast5s_to_fastq, dirs)
    exit()
    while dirs:
        with Pool(processes=n_threads) as pool:
            pool.map(fast5s_to_fastq, dirs)
        for dir_ in (os.path.join(FAST5singleIN_DIR, x) for x in os.listdir(FAST5singleIN_DIR) if os.path.isdir(os.path.join(FAST5singleIN_DIR, x))):
            if os.path.exists(os.path.join(os.path.join(dir_), os.path.basename(dir_) + '.fastq')):
                dirs.remove(dir_)
        print('So many dirs to go %s' % len(dirs))
    exit()
    for  x in (Parallel(n_jobs=n_threads)(delayed(fast5s_to_fastq)(x) for x in dirs)):
                    print(x)
