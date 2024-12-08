# FastAPI Python App

## Dockerfile Overview

### Reason for Choosing Python's Image:
- **Lightweight**: Compared to Linux-based images, Python's slim images use lesser memory and storage.
- **Pre-installed Python Packages**: Comes with necessary Python package installations out of the box.
- **Secure**: Prevents direct shell access (`bash`), which enhances security during containerization (though access might be necessary in some scenarios).
- **Faster Build Times**: Optimized for efficient builds.

### Challenges with Other Linux-based Images:
- **Dependency Management**: Requires setting up `virtualenv` to isolate dependencies, adding extra steps.
- **Dependency Isolation**: While `virtualenv` is a good isolator, using a Python image simplifies the process.

For these reasons, a Python image was chosen to streamline the process and maintain simplicity.

## ENTRYPOINT and CMD
- **Best Practice**: Following Docker's best practices to avoid conflicts during application startup.
- **CMD Usage**: CMD is preferred as it allows overriding values when needed, making the setup more flexible.
