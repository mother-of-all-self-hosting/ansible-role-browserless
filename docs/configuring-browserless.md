<!--
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 - 2026 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Browserless

This is an [Ansible](https://www.ansible.com/) role which installs [Browserless](https://docs.browserless.io) to run as a [Docker](https://www.docker.com/) container wrapped in a systemd service.

Browserless allows to deploy headless browsers in Docker.

See the project's [documentation](https://docs.browserless.io/enterprise/quick-start) to learn what Browserless does and why it might be useful to you.

## Adjusting the playbook configuration

To enable Browserless with this role, add the following configuration to your `vars.yml` file.

**Note**: the path should be something like `inventory/host_vars/mash.example.com/vars.yml` if you use the [MASH Ansible playbook](https://github.com/mother-of-all-self-hosting/mash-playbook).

```yaml
########################################################################
#                                                                      #
# browserless                                                          #
#                                                                      #
########################################################################

browserless_enabled: true

########################################################################
#                                                                      #
# /browserless                                                         #
#                                                                      #
########################################################################
```

### Requiring a token (recommended)

Browserless does not authenticate anything unless it is given a token. Out of the box this role does not set one, which is what Browserless itself does too, and it keeps the instance usable by services on the same container network without any further configuration.

That default is only defensible while the instance is reachable from the container network alone, because every endpoint is served to whoever can reach it:

- `/content`, `/screenshot` and `/pdf` fetch and render whatever URL they are handed, from inside the container networks Browserless is attached to — so a caller can use it to reach services which are not published to the internet at all
- `/function` runs JavaScript supplied in the request body
- `ws://…/chromium` hands out a Chrome DevTools Protocol session, with the same reach

To require a token, add the following configuration to your `vars.yml` file. Make sure to replace `TOKEN_HERE` with a secret value of your own (e.g. one generated with `pwgen -s 64 1`).

```yaml
browserless_auth_token: TOKEN_HERE
```

Unauthenticated requests are then answered with `401 Unauthorized`, and callers have to present the token as a `token` query parameter, an `Authorization: Bearer` header or an `X-API-Key` header.

**Note**: setting a token also changes what the services connecting to Browserless need to be told — their connection URL has to carry `?token=TOKEN_HERE`. Services which a playbook wires up to Browserless automatically (such as Karakeep, RSS-Bridge and RSSHub) are not adjusted for you.

### Exposing the instance (optional)

By default, the Browserless instance is not exposed externally, as it is mainly intended to be used in the internal network, connected to other services.

>[!WARNING]
> Do not expose Browserless publicly without either setting `browserless_auth_token` (see [above](#requiring-a-token-recommended)) or enabling basic authentication (`browserless_container_labels_traefik_middleware_basic_auth_enabled`). Without one of the two, anyone who finds the hostname can have your server fetch arbitrary URLs and run arbitrary JavaScript on your behalf. The role prints a warning during installation when it detects this combination.

To expose it to the internet, add the following configuration to your `vars.yml` file. Make sure to replace `example.com` with your own value.

```yaml
browserless_hostname: "example.com"

browserless_container_labels_traefik_enabled: true
```

After adjusting the hostname, make sure to adjust your DNS records to point the domain to your server.

**Note**: hosting Browserless under a subpath (by configuring the `browserless_path_prefix` variable) does not seem to be possible due to Browserless's technical limitations.

### Extending the configuration

There are some additional things you may wish to configure about the service.

Take a look at:

- [`defaults/main.yml`](../defaults/main.yml) for some variables that you can customize via your `vars.yml` file. You can override settings (even those that don't have dedicated playbook variables) using the `browserless_environment_variables_additional_variables` variable

See the [documentation](https://docs.browserless.io/enterprise/docker/config) for a complete list of Browserless's config options that you could put in `browserless_environment_variables_additional_variables`.

## Installing

After configuring the playbook, run the installation command of your playbook as below:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

If you use the MASH playbook, the shortcut commands with the [`just` program](https://github.com/mother-of-all-self-hosting/mash-playbook/blob/main/docs/just.md) are also available: `just install-all` or `just setup-all`

## Usage

After running the command for installation, Browserless becomes available internally to other services on the same network. If the service is exposed to the internet, it becomes available at the specified hostname like `https://example.com`.

## Troubleshooting

### Check the service's logs

You can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu browserless` (or how you/your playbook named the service, e.g. `mash-browserless`).
