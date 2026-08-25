<!--
SPDX-FileCopyrightText: 2018-2026 Slavi Pantaleev
SPDX-FileCopyrightText: 2019-2022 Aaron Raimist
SPDX-FileCopyrightText: 2019-2023 MDAD project contributors
SPDX-FileCopyrightText: 2023 QEDeD
SPDX-FileCopyrightText: 2024 Fabio Bonelli
SPDX-FileCopyrightText: 2024 Nikita Chernyi
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara
SPDX-FileCopyrightText: 2026 spatterlight

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Molecule Testing

This role supports [Molecule](https://docs.ansible.com/projects/molecule/), an Ansible testing framework designed for developing and testing Ansible collections, playbooks, and roles.

## Prerequisites

To utilize Molecule you need to prepare several requirements:

- **x86** computer running one of these operating systems that make use of [systemd](https://systemd.io/):
  - **Archlinux**
  - **CentOS**, **Rocky Linux**, **AlmaLinux**, or possibly other RHEL alternatives (although your mileage may vary)
  - **Debian** (10/Buster or newer)
  - **Ubuntu** (18.04 or newer, although [20.04 may be problematic](https://github.com/mother-of-all-self-hosting/mash-playbook/blob/main/docs/ansible.md#supported-ansible-versions) if you run the Ansible playbook on it)
- `root` access on the computer which Molecule runs against
- [Ansible](http://ansible.com/) program
- [Python](https://www.python.org/)
  - Most distributions install Python by default, but some don't (e.g. Ubuntu 18.04) and require manual installation (something like `apt-get install python3`)
- [Docker](https://www.docker.com)
  - Access to Docker UNIX socket (`/var/run/docker.sock`) is required by default

## Installation

To set up the environment for using Molecule, run the command below on the terminal:

```bash
python3 -m venv ./molecule/venv
source ./molecule/venv/bin/activate
pip3 install -r ./molecule/requirements.txt
```

## Scenarios

Currently there are two testing scenarios available.

Both start a small web server on Browserless's own container network and have Browserless render the page it serves, because asserting that the systemd unit is active proves very little on its own: the unit is configured with `Restart=always`, which makes systemd report a crash-looping container as `active` too.

### `default`

Tests a standard Browserless installation, with the role's defaults for authentication (that is: none).

It asserts that the running Browserless reports the version which `browserless_version` pins, that the settings the scenario passes through `browserless_environment_variables_additional_variables` and `browserless_environment_variables_tz` reach the process (they differ from every default Browserless has of its own), and that Browserless really drives a browser: it fetches the probe target page over HTTP, runs JavaScript against it, screenshots an element of it and prints it to PDF.

It also asserts, as a negative control rather than as an endorsement, that with no token configured every one of those endpoints — including the Chrome DevTools Protocol WebSocket — is served to an anonymous caller.

### `auth`

Tests an installation with `browserless_auth_token` set.

It asserts that the token reaches the process (Browserless echoes it back through `GET /config`), that requests carrying no token or the wrong token are refused with `401`, that the CDP WebSocket endpoint refuses them too, and that a caller presenting the token still gets a rendering of the probe target page.

## Running

By default it is configured to run the scenarios on Ubuntu 26.04.

```bash
molecule test --scenario-name default
molecule test --scenario-name auth
```

You can utilize other distributions by setting one to the `MOLECULE_DISTRO` environment variable:

```bash
# Ubuntu 24.04
MOLECULE_DISTRO=ubuntu2404 molecule test --scenario-name default

# Debian 13
MOLECULE_DISTRO=debian13 molecule test --scenario-name default

# Debian 12
MOLECULE_DISTRO=debian12 molecule test --scenario-name default
```
