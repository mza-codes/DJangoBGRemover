#!/bin/bash - this script removes folder /uploads and recreate it as empty. This action is irreversible, proceed with caution!

rm -rf uploads
mkdir uploads
cd uploads
touch .gitignore