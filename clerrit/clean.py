# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Philippe Proulx <eeppeliteloop@gmail.com>

import subprocess

import rich.console

import clerrit.common


def _run():
    console = rich.console.Console(highlighter=None)

    # Filter for `clerrit-*` branches, skipping the current branch
    cur_clerrit_branch = None
    branches = []

    for line in subprocess.run(['git', 'branch', '--no-color'], capture_output=True,
                               text=True, check=True).stdout.splitlines():
        stripped = line.strip()

        if line.startswith('*'):
            if stripped.lstrip('* ').startswith('clerrit-'):
                cur_clerrit_branch = stripped.lstrip('* ')

            continue

        if stripped.startswith('clerrit-'):
            branches.append(stripped)

    if cur_clerrit_branch is not None:
        clerrit.common._warn(console, f'Skipping current branch `[bold]{cur_clerrit_branch}[/bold]`')

    if not branches:
        clerrit.common._info(console, 'No `[bold]clerrit-*[/bold]` branches to delete!')
        return

    clerrit.common._info(console, f'Deleting {len(branches)} `[bold]clerrit-*[/bold]` branch(es)...')
    clerrit.common._exec(console, ['git', 'branch', '-D'] + branches, check=True)
    clerrit.common._info(console, 'Done.')
