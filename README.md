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
- **reserved_ip**: read, update
- **sizes**: read
- **ssh_key**: read
- **tag**: create, read, delete

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
  --key [ssh_key_id_1] --key [ssh_key_id_2] \
  --volume [volume_id_1] --volume [volume_id_2] \
  --tag production --tag web-server \
  --cloud-config name-of-my-cloud-init
```

The above command creates a droplet named `ai-tasks-01` using the `nvidia-h100` template. It attaches specified SSH keys and volumes, adds tags, and applies a cloud-init configuration (`name-of-my-cloud-init.yaml` located in `cloud-configs/`).

#### Start/Stop a Droplet

```bash
# Stop a droplet
dom droplet stop [droplet_id]

# Start a droplet
dom droplet start [droplet_id]
```

#### Delete a Droplet

```bash
dom droplet delete [droplet_id]
```
*Note: Protected droplets cannot be deleted.*

#### List Droplets

```bash
# List all droplets (CPU and GPU)
dom droplet list

# List only GPU droplets
dom droplet list --droplet-type gpu

# List only CPU droplets
dom droplet list --droplet-type cpu
```

#### Get Droplet Information

```bash
dom droplet info [droplet_id]
```

#### List Droplet Templates

```bash
dom droplet templates
```
This lists available templates defined in the `droplets/` directory.

### Volume Management

`dom` also supports creating and managing volumes for storing data, such as AI models.

#### Create a Volume

Example using the `models.json` configuration file (contents shown below):

```json
{
    "name": null,
    "size_gigabytes": 100,
    "description": "Models volume",
    "region": null,
    "filesystem_type": "ext4",
    "filesystem_label": "models"
}
```

```bash
# Create volume using the 'models' template and name it 'aimodels'
dom volume create models aimodels --tag database --tag critical
```

This creates a volume named `aimodels` based on the `models` template, applies the specified tags, and uses settings from `config.yaml` (like region).

#### Attach/Detach a Volume

```bash
# Attach volume 'my-volume-name' to droplet [droplet_id]
dom volume attach my-volume-name [droplet_id]

# Detach volume 'my-volume-name' from droplet [droplet_id]
dom volume detach my-volume-name [droplet_id]
```
*Note: Volumes cannot be detached from protected droplets.*

#### Delete a Volume

```bash
dom volume delete [volume_id]
```
*Note: Protected volumes cannot be deleted.*

#### List Volumes

```bash
dom volume list
```

#### Get Volume Information

```bash
dom volume info [volume_id]
```

#### List Volume Templates

```bash
dom volume templates
```
This lists available templates defined in the `volumes/` directory.

### SSH Key Management

#### List SSH Keys

```bash
dom key list
```

#### Get SSH Key Information

```bash
dom key info [ssh_key_id]
```

### Reserved IP Management

#### List Reserved IPs

```bash
dom ip list
```

#### Assign/Unassign a Reserved IP

```bash
# Assign a reserved IP to a droplet
dom ip assign [reserved_ip_address] [droplet_id]

# Unassign a reserved IP
dom ip unassign [reserved_ip_address]
```

### Action Management

#### Get Action Information

Actions represent events like droplet creation or volume attachment. You can track their status.

```bash
dom action info [action_id]
```
The `action_id` is typically returned when you perform an action like creating a droplet.

### Other Commands

#### Initialize Project

As shown in the Workflow section, initialize a new project structure:

```bash
dom init
```

#### Show Version

```bash
dom version
```

---

## License

This project is licensed under the Apache License 2.0. See the `LICENSE` file for details.
