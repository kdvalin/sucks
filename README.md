# Systemd User Container Kickstarting System (SUCKS)

SUCKS is a simple frontend for podman commands to facilitate management and using containers
with Systemd as their entrypoint.

Why systemd?  Sometimes you might want to leverage systemd facilities within a container, or use
packages, such as Performance Co-Pilot, that need systemd to function.

# Base Images

SUCKS requires a container image that uses systemd as its entrypoint. The following
pre-built images are available on Quay.io:

| Image | Description |
|---|---|
| `quay.io/zathras/ubuntu-init:24.04` | Ubuntu 24.04 with systemd as the entrypoint |

Example container definition using the Ubuntu base image:

```yaml
name: My Ubuntu Container
image: quay.io/zathras/ubuntu-init:24.04
initSteps:
    - apt-get install -y git
ciSteps:
    - ./run_tests.sh
workdir: /root
```

# Logging

Verbosity is controlled via the `LOGLEVEL` environment variable. The default level is `WARNING`.
Set it to `DEBUG` for detailed output:

```sh
LOGLEVEL=DEBUG sucks test.yml setup
```

# Usage
`sucks <path/to/container_definition> <action> [options]`

## Container Definitions
A container definition is a simple YAML file, detailing the image to use, 
any steps you want done during the setup or CI step, and the working 
directory those commands should occur in.

Below is an example
```yaml
# Provided for human readability
name: UBI 9 Init
image: registry.access.redhat.com/ubi9-init # The image to use
initSteps: # The shell commands to run during `setup`
    - dnf install -y git
    - git clone example-repo.git
ciSteps: # The shell commands to run during `ci`
    - example-repo/run_example
workdir: /root # A working directory for any command to use
```

## Container Naming

SUCKS automatically names containers based on the YAML filename. The container name is always
`sucks-<filename-stem>` — for example, `test.yml` maps to a container named `sucks-test`. All
commands use this convention to locate the correct running container, so the filename of your
container definition is significant.

## Commands
### setup
`sucks <container_def_path> setup [arguments]`

This kicks the systemd container going with the provided configuration
options.

#### Arguments
- `-v/--volume <volstring>`
    - Performs a bind mount to the container so local
    files can be accessed within the container.
    - `volstring` is the same format as the argument passed to
    [docker/podman](https://docs.podman.io/en/v4.6.1/markdown/options/volume.html)
    - Can be specified multiple times for multiple mounts
- `--privileged`
    - Allows the container to access to the host machine's devices
    - More information [here](https://docs.podman.io/en/v4.3/markdown/options/privileged.html)
- `--pull <always, missing, never, newer>`
    - Sets when to pull an image, [see here](https://docs.podman.io/en/v5.0.1/markdown/podman-run.1.html#pull-policy) for information
    - Default is `missing`
- `-w/--workdir <path>`
    - Sets the working dir of the commands in `initSteps`
    - This overrides `workDir` within the container defintion

### destroy
`sucks <container_def_path> destroy`

Kills and removes the running systemd container. Containers created by `setup` are automatically
removed when killed, so no manual cleanup is required.

### run
`sucks <container_def_path> run [options] <exec_command ...>`

Runs a specified command within the systemd container
#### Options
- `-e/--env <env string>`
    - Set an enviornment variable for the command
    - Can be specified multiple times
    - Format is same as [docker/podman](https://docs.podman.io/en/v5.0.1/markdown/podman-run.1.html#env-e-env)
- `-i/--interactive`
    - Pass stdin to the running command
- `-t/--tty`
    - Allocate a pseudo-tty for the command
- `-w/--workdir <path>`
    - Sets the working dir of the command
    - This overrides `workDir` within the container defintion
- `exec_command`
    - A command that is available within the container

### shell
`sucks <container_def_path> shell [options]`

Opens a shell within the container
#### Options
- `-s/--shell_command <command>`
    - Sets what command to run for the shell
    - Default is `bash`
- `-w/--workdir <path>`
    - Sets the working dir of the shell
    - This overrides `workDir` within the container defintion

### ci
`sucks <container_def_path> ci [options]`

Runs the `ciSteps` commands within the container.

#### Arguments
- `-w/--workdir <path>`
    - Sets the working dir of the CI commands
    - This overrides `workDir` within the container defintion

