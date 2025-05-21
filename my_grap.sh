#!/bin/bash
grep --color=auto -r --exclude-dir={.git,.astro,node_modules,dist} "$1" .
