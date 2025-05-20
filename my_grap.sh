#!/bin/bash
grep --color=auto -r --exclude-dir={.git,node_modules,dist} "$1" .
