# Statistics functions for Python's sqlite3 module.

SQLite is a great library which implements RDMS functionality. 

But if I am not mistaken, it lacks certain built-in statistics functions that could be useful in business analysis.

In this tiny project, I define classes which can be used with `create_aggregate()` and `create_window_function()` methods of the `sqlite3.Connection` object to create such functions. 

The statistics functions enabled by the classes are:

- the Median,
- the Mode,
- the Geometric mean,
- the Harmonic mean,
- the Standard Deviation (for the population),
- the Variance (for the population).

These functions can be created as regular aggregate functions or as window (analytic) functions. The aggregate functions are actually redundant because the corresponding window functions can be used instead. Indeed, classes for the latter should implement methods required for aggregate functions - `step()` and `finalize()` - as well as those needed specifically for window functions - `value()` and `inverse()`. 

The classes for both types of functions are defined in the sqlfuns.py module. To test the functionality, gendata.py creates a simple SQLite database with a single table containing random categorized data. It also features a command line interface (CLI) so it can be used as a standalone program. The CLI is rudimentary and accepts only the file name of the database (I haven't got round to making it more flexible yet :-)

The main.py opens the database and contains an SQL query which can be used to check any of the created functions.

Comments are provided in all *.py files to make the code easier to read.



