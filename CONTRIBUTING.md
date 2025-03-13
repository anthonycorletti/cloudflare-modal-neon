# Contributing Guide

## Installation Requirements

Install the suggested requirements via `brew` (assuming mac users).

- [server](./server/)
    - uv: python and python package management
    - docker: running postgres locally
- [web](./web)
    - bun: web building and package management

Run the following commands:

```sh
brew install --cask docker
brew install bun uv
```

## Getting started

To get started working with server side code, make sure you have access to modal, sentry, and neon.

Also, explore all the contents of the `bin` directory. These are commands you can run to install, lint, run, and test the code.

For the frontend code, the admin panel, this is a secondary bit of work to the backend services, but it's basically a react app with shadcn, and all bun commands are listed in `package.json`.

When in doubt, visit `.github` for all details about what's being run in CI.


## Services in use

- [Cloudflare](https://cloudflare.com)
    - Nameserver hosting
    - Cloud Object Storage Hosting on R2
    - General web/ frontend Hosting
- [Modal](https://modal.com)
    - API and data pipeline Hosting
- [Neon](https://neon.tech)
    - Database Hosting
- [Logfire](https://pydantic.dev/logfire)
    - Error Monitoring, Logging, Observability
- [Google Cloud Platform](https://console.cloud.google.com)
    - OAuth Provider
