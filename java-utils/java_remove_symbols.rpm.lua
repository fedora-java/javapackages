local lib = require("java_symbols_lib")

-- rpmlua passes CLI arguments shifted by one
-- Do not forget to pass additional "--" to separate the script name from its
-- CLI arguments
lib.main(table.move(arg, 1, #arg, 0, {}))
