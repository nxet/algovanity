# algovanity

generate vanity addresses for the Algorand blockchain

The script supports multiple patterns matching at once, and that is in fact the suggested operation mode: generate once, match many.  
Bundling more patterns into a single run allows for substantial gains in execution time, since there is no logic in place to avoid potential duplicates any paraller run would
This design also facilitates attempts in finding longer matches in a potentially shorter timespan, giving the user control in reducing the precision and diverging from the initial desired outcome.
The process spawns multiple subprocesses which will run indefinitely, with a main loop printing to console some basic statistics and any new matches as they're found, waiting for a keyboard interrupt.

---

## howto and gotchas

##### pattern formats
Matching is supported with three different patterns:
  - `start` matches the string at the beginning of the address  
    configured with arguments like `ADDR...` or `MYNAME...`
  - `end` matches the string at the end of the address  
    configured with arguments like `...ADDR` or `...MYNAME`
  - `edges` matches strings both at start and end of the address  
    configured with arguments like `COOL...ADDR` or `ABC...XYZ`
  - `regex` compiles the provided pattern as is and attempts to `re.fullmatch`
    configured with arguments like `^AB[.]*CD[.]*YZ$` or `^NAME[0-9]*[.]*$`

> NB: the longer the pattern the longer the run time.  
> Anything over 6 characters will be running for a **very** long time.

##### file output
The script will always try to append new matches to the provided file instead of overwriting, creates a new file if none is available.  
Matches are dumped to file at each status update, and finally once the script is terminated.  
The file is opened/closed on-demand, allowing to `tail -f` it for example.

##### examples
```sh
# install package
pip3 install algovanity

# match addresses starting with MYNAME
algovanity MYNAME...
# or either starting or ending with MYNAME
algovanity MYNAME... ...MYNAME
# but limiting to only 2 subprocesses
algovanity MYNAME... ...MYNAME --procs-max 2
# dump results to file
algovanity MYNAME... --output ~/algovanity.txt
# match addresses starting with COOL and ending with ADDR
algovanity COOL...ADDR
# match addresses starting with NAME plus one exact number
algovanity NAME9... --output ~/algovanity.txt
# match addresses starting with NAME plus one random number
algovanity '^NAME[0-9][A-Z0-9]+$' --output ~/algovanity.txt
# match addresses starting with NAME plus two random numbers
algovanity '^NAME[0-9]{2}[A-Z0-9]+$' --output ~/algovanity.txt
```

---

##### support this project
if this software has been helpful please consider donating a few $ALGO to support future development
##### License
This project is licensed under GPL 3.0 - see LICENSE for details.

