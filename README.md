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

> NB: the longer the pattern the longer the run time.  
> Anything over 6 characters will be running for a **very** long time.

##### file output
The script will always try to append new matches to the provided file instead of overwriting, creates a new file if none is available.  
Matches are dumped to file at each status update, and finally once the script is terminated.  
The file is opened/closed on-demand, allowing to `tail -f` it for example.

##### examples
for more details please use the help built into the CLI tool with `algovanity --help`

---

##### support this project
if this software has been helpful please consider donating a few $ALGO to support future development
