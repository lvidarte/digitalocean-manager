
# DigitalOcean Manager (DOM) CLI

`dom` is a command-line tool to manage your DigitalOcean resources. From GPU droplets to volumes, it provides an intuitive interface to simplify your cloud management tasks, especially for AI workloads.

---

## Installation

Install `dom` using pip:

```bash
pip install dom-cli
```

---

## Prerequisites

Before using the `dom` CLI, you need to set up your DigitalOcean API token.  
Export the `DIGITALOCEAN_TOKEN` environment variable with your token, ensuring it has the following permissions:

- **actions**: read
- **block_storage**: read, delete, create
- **block_storage_action**: read, create
- **droplet**: read, update, delete, create
- **regions**: read
- **sizes**: read
- **tag**: create, read, delete
- **ssh_key**: read

---

## Usage

The general syntax of the `dom` command is:

```bash
dom [OPTIONS] COMMAND [ARGS]...
```

### Workflow

1. **Installation**: Install the CLI tool using pip.
2. **Initialize a Project**: Create a new project in the current directory using:
   ```bash
   dom init
   ```

   This command will create the following project structure:

   ```
   ├── config.yaml
   ├── cloud-configs
   │   └── base.yaml
   ├── droplets
   │   ├── cpu-mini.json
   │   └── nvidia-h100.json
   └── volumes
       └── models.json
   ```

### `config.yaml`

The `config.yaml` file contains the main configuration for the project. Below is an example:

```yaml
# DigitalOcean datacenter region slug (str).
# Full detail here: https://docs.digitalocean.com/platform/regional-availability/
digitalocean_region: nyc2

# List of (int) protected droplets IDs.
# You can't stop/delete a protected droplet.
# You can't detach a volume from a protected droplet.
protected_droplets: []

# List of (str) protected volumes IDs.
# You can't delete a protected volume.
protected_volumes: []

# JSON indentation level (int) for raw outputs.
json_indent: 4

# Action ping interval (float) in seconds.
ping_interval: 1
```

### Project Directories

- **`cloud-configs/`**: Directory for cloud-init YAML files used to define tasks and configurations for droplets.
- **`droplets/`**: Directory for droplet templates, including configurations for CPUs and GPUs.
- **`volumes/`**: Directory for volume templates, such as those for storing AI models.

---

## Examples

### Droplet Management

`dom` handles GPU droplets and is optimized for managing automated AI tasks on DigitalOcean GPU droplets.

#### Create a Droplet

Example of droplet creation using the `nvidia-h100` template:

```bash
dom droplet create nvidia-h100 ai-tasks-01 \
  --key [some key id] \
  --volume [some volume id] \
  --cloud-config name-of-my-cloud-init
```

The above command creates a droplet with all the configurations and scripts needed for running AI tasks on GPU droplets, using a cloud-init file (`name-of-my-cloud-init.yaml`) defined under the `cloud-configs/` directory.

### Volume Management

`dom` also supports creating and managing volumes for storing data, such as AI models.

#### Example: Create a Volume

Example using the `models.json` configuration file:

```bash
cat volumes/models.json 
{
    "name": null,
    "size_gigabytes": 100,
    "description": "Models volume",
    "region": null,
    "filesystem_type": "ext4",
    "filesystem_label": "models"
}

dom volume create models aimodels
```

This creates a volume named `aimodels` with a size of 100GB, formatted with the `ext4` filesystem, and labeled as `models`. The volume can then be shared across multiple droplet instances.

---

## License

This project is licensed under the Apache License 2.0. See the `LICENSE` file for details.
