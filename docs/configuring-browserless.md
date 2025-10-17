<!--
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 - 2024 Slavi Pantaleev
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

This is an [Ansible](https://www.ansible.com/) role which installs [Browserless](https://github.com/caronc/browserless-api) to run as a [Docker](https://www.docker.com/) container wrapped in a systemd service.

[Browserless](https://github.com/caronc/browserless/) allows you to send a notification to almost all of the most popular notification services available to us today such as Matrix, Telegram, Discord, Slack, Amazon SNS, ntfy, Gotify, etc.

See the project's [documentation](https://github.com/caronc/browserless-api/blob/master/README.md) to learn what Browserless does and why it might be useful to you.

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

### Exposing the built-in Configuration Manager (optional)

By default, the Browserless's built-in Configuration Manager where one can access and create configurations on the web browser is not exposed to the internet. Note that the Configuration Manager is not required for using Browserless as you can access to it with the [Browserless CLI](https://github.com/caronc/browserless/wiki/CLI_Usage).

To expose it to the internet, add the following configuration to your `vars.yml` file. Make sure to replace `example.com` with your own value.

```yaml
browserless_hostname: "example.com"

browserless_container_labels_traefik_enabled: true
```

After adjusting the hostname, make sure to adjust your DNS records to point the domain to your server.

When exposing, make sure to enable authentication as anyone can access to it by default. Refer to [this section](https://github.com/caronc/browserless-api/blob/master/README.md#authentication) on the role's documentation for details about how to enable it with the internal nginx instance.

**Note**: hosting the Configuration Manager under a subpath (by configuring the `browserless_path_prefix` variable) does not seem to be possible due to Browserless's technical limitations.

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- [`defaults/main.yml`](../defaults/main.yml) for some variables that you can customize via your `vars.yml` file. You can override settings (even those that don't have dedicated playbook variables) using the `browserless_environment_variables_additional_variables` variable

See the [documentation](https://github.com/caronc/browserless-api/blob/master/README.md#environment-variables) for a complete list of Browserless's config options that you could put in `browserless_environment_variables_additional_variables`.

## Installing

After configuring the playbook, run the installation command of your playbook as below:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

If you use the MASH playbook, the shortcut commands with the [`just` program](https://github.com/mother-of-all-self-hosting/mash-playbook/blob/main/docs/just.md) are also available: `just install-all` or `just setup-all`

## Usage

After running the command for installation, Browserless becomes available. If the Configuration Manager is configured to be exposed to the internet, it becomes available at the specified hostname like `https://example.com`.

You can check the list of notification services supported by Browserless at <https://github.com/caronc/browserless/wiki#notification-services>.

## Troubleshooting

### Check the service's logs

You can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu browserless` (or how you/your playbook named the service, e.g. `mash-browserless`).
