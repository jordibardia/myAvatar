import os
import glob
import sys
from posmap_defs import make_posmaps

#Script file to generate position maps without training automatically
#Intended for transferring to HiPerGator


#num_to_generate = len(glob.glob1('AFLW2000', '*.jpg'))
num_to_generate = len(glob.glob1(sys.argv[1], '*.jpg'))

if len(sys.argv) > 1:
    if int(sys.argv[1]) <= num_to_generate and int(sys.argv[1]) >= 1:
        num_to_generate = int(sys.argv[1])

files = glob.glob('data_input/*')
if sys.argv[1] == 'AFLW2000':
    files = glob.glob('posmap_output/')

for f in files:
    os.remove(f)

make_posmaps(num_to_generate)

