#! /usr/bin/bash
frontend=$(gp url 3000)
backend=$(gp url 4567)

echo $frontend
echo $backend

# gp preview $(gp url 3000) --external
# gp preview $(gp url 4567) --external