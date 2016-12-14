#!/bin/bash

awk '{print $2,$0}' $1  | sort -r |  awk '{print $1,$2,$16,$17,$18,$19,$20}' | head -n +3 | tail -n 1
