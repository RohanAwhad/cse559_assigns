SAVE=1 OPTIMIZE=1 python3 ./randomized_motif_search.py ./submission_tests/rand_testcases/test_1.txt &
SAVE=1 OPTIMIZE=1 python3 ./randomized_motif_search.py ./submission_tests/rand_testcases/test_2.txt &
SAVE=1 OPTIMIZE=1 python3 ./randomized_motif_search.py ./submission_tests/rand_testcases/test_3.txt &
SAVE=1 OPTIMIZE=1 python3 ./randomized_motif_search.py ./submission_tests/rand_testcases/test_4.txt

SAVE=1 OPTIMIZE=1 python3 ./gibbs_sampling_motif_search.py ./submission_tests/gibbs_testcases/test_1.txt &
SAVE=1 OPTIMIZE=1 python3 ./gibbs_sampling_motif_search.py ./submission_tests/gibbs_testcases/test_2.txt &
SAVE=1 OPTIMIZE=1 python3 ./gibbs_sampling_motif_search.py ./submission_tests/gibbs_testcases/test_3.txt &
SAVE=1 OPTIMIZE=1 python3 ./gibbs_sampling_motif_search.py ./submission_tests/gibbs_testcases/test_4.txt

SAVE=1 OPTIMIZE=1 python3 ./q3.py ./submission_tests/motif_dataset.txt
