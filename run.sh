#!/bin/sh

if [ -f package.json ]; then
    /build/gen_node_build_infos.py
fi
