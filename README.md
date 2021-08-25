# algovanity

generate vanity addresses for the Algorand blockchain


##### pattern format
- all patterns must be passed in the formats `{pattern},{position}` or `{pattern_start}...{pattern_end}`
  - `pattern` is any alphanumerical string - **NB: anything over 6 characters will be running for a long time**
  - `position` *[optional]* can be either `start` or `end` - if omitted defaults to `start`
