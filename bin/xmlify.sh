#!/bin/bash
# Preprocessing for XML file - to include <DOC> and </doc> at the start and at the end
output="${1:0:-4}.2.XML"
{ echo -n $'<START>\n' ; cat $1 ; echo -n $'</START>\n' ; } > "${output}"
printf "${output}"