Works with Perple_X version 6.9.1, source updated October 14, 2022.

These are simple python modules and shell scripts to

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
Where n_sub is the number of quadrants along each axis. (i.e., the number of times that build, vertex and werami will be performed is n = n_sub^2) 

Then:
```
./parallelize build template n_proc
./parallelize vertex template n_proc
./parallelize werami template n_proc
```
I suggest using n_proc = n_sub.
(Note: need to wait for vertex to finish before you can do werami, 
same thing for vertex and build but the latter is almost instantaneous).
You may take a gander at the progress with 
```
tail -f template/quadrant*/OUTPUT_*txt
```

Finally:
```
python unsplit.py template
```
This will put everything together. You can check out the result with pywerami.