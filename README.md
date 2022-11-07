Works with Perple_X version 6.9.1, source updated October 14, 2022.

These are simple python modules to

* Define a number of quadrants in the PT space
* Run BUILD for each of these quadrants, automating the input
* Run VERTEX in each of these automating the input and possibly parallelizing
* Run WERAMI, automating the input
* Stitch the tab files thus created into one neat tab file


The dir_ign directory contains my own tests (it's gitignored)

# Usage

Create txt file with components, mass amounts, solution models 
(check template for how it's done):
```
vim template.txt
```

Then:
```
python split.py template.txt n_sub
```

Then:
```
./parallelize build template n_proc
./parallelize vertex template n_proc
./parallelize werami template n_proc
```
(Note: need to wait for vertex to finish before you can do werami, 
same thing for vertex and build but the latter is almost instantaneous).

Finally:
```
python unsplit.py foo
```