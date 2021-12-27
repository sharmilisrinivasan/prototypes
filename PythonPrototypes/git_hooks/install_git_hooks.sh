#!/bin/bash
cd $(git rev-parse --git-dir)/hooks/
hook_path="$(git rev-parse --git-dir)/../git_hooks"
ls $hook_path | grep -v "\.sh" | while read file
do
    chmod +x $hook_path/$file
    ln -sf $hook_path/$file $file
done
