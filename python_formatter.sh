#!/bin/bash

# convert 4 space indentation to 2 space indentation
find './' -type f -name "*.py" -exec sed -i '' 's/    /  /g' {} \;