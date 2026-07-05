# Docker Terraform versions

Blast Radius Fork bundles a Terraform binary into the Docker image so that the container can run `terraform init` and `terraform graph` without depending on the host machine's Terraform installation.

The default Dockerfile build currently pins Terraform to `1.15.7`:

```sh
docker build -t blast-radius-fork .
```

To build an image with a different Terraform version, pass `TF_VERSION` explicitly:

```sh
docker build \
  --build-arg TF_VERSION=1.10.5 \
  --build-arg PYTHON_VERSION=3.10 \
  -t blast-radius-fork:1.10.5 \
  .
```

Verify the Terraform version embedded in an image with:

```sh
docker run --rm --entrypoint terraform blast-radius-fork:1.10.5 version
```

When running against a Terraform project, choose or build an image whose Terraform version satisfies the project's `required_version` constraint. For example, a project declaring:

```hcl
terraform {
  required_version = ">= 1.15.0"
}
```

should be run with an image built from Terraform `1.15.x` or newer.

Example run:

```sh
docker run --rm -it -p 5000:5000 \
  -v $(pwd):/data:ro \
  --security-opt apparmor:unconfined \
  --cap-add=SYS_ADMIN \
  blast-radius-fork:1.15.7
```

Windows PowerShell:

```powershell
docker run --rm -it -p 5000:5000 `
  -v ${pwd}:/data:ro `
  --security-opt apparmor:unconfined `
  --cap-add=SYS_ADMIN `
  blast-radius-fork:1.15.7
```

If your path contains spaces, quote the volume argument:

```powershell
-v "${pwd}:/data:ro"
```
