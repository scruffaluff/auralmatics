# Contributing

Thank you for taking the time to contribute to Auralmatics. This guide will
assist you in setting up a development environment, understanding the project
tooling, and learning the coding guidelines.

## Deployment

Auralmatics is deployed via a Docker container on FlyIO. The following commands
must be manually run before the first release.

```
flyctl launch --no-deploy --copy-config --name auralmatics
flyctl ips allocate-v4 --app auralmatics
flyctl certs add --app auralmatics auralmatics.scruffaluff.com
```

After creating the certifcates, follow the `Direct visitors to application` and
`Domain ownership verification` CNAME instructions at
https://fly.io/apps/auralmatics/certificates.
