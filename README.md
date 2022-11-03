Works with Perple_X version 6.9.1, source updated October 14, 2022.

These are simple python modules to

* Define a number of quadrants in the PT space
* Run BUILD for each of these quadrants, automating the input
* Run VERTEX in each of these automating the input and possibly parallelizing
* Run WERAMI, automating the input
* Stitch the tab files thus created into one neat tab file


The dir_ign directory contains my own tests (it's gitignored)

# Usage

Create txt file with components, massa amounts, solution models

```
vim foo.txt
```

Then

```
python split.py foo.txt n_sub
```

Then

```
./parallelize build foo n_proc
./parallelize vertex foo n_proc
./parallelize werami foo n_proc
```
Then

```
python unsplit.py foo
```