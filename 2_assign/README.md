# CSE 559 Assign 2

## How to Run

### Setup

`python3 -m pip install requirements.txt`
`python3 setup.py build_ext --inplace`


### Q1 Randomized Motif Search

`OPIMIZE=1 python3 randomized_motif_search.py ./input_1.txt` -> will output the result in
a new `outputs` dir with name `randomized_motif_search_1.txt`

* If the above command gives you an error, use `python3 randomized_motif_search.py ./input_1.txt`

* `OPTIMIZE=1` utilizes the cython compiled code for getting profile-most-probable-kmer motif

### Q2 Gibbs Sampling Motif Search

`OPTIMIZE=1 python3 gibbs_sampling_motif_search.py ./input_1.txt` -> will output the result in
a new `outputs` dir with name `gibbs_sampling_motif_search_1.txt`

* If the above command gives you an error, use `python3 gibbs_sampling_motif_search..py ./input_1.txt`

### Q3

`OPTIMIZE=1 python3 q3.py ./motif_dataset.txt` -> will output the result and append it in `outputs/q3_result.txt`

* If the above command gives you an error, use `python3 q3.py ./motif_dataset.txt`

