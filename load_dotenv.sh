#! /usr/bin/bash
export $(grep -v '^#' .env | xargs)
