# Contributing

Kubemoot is an independent open-source project under the Apache License 2.0. Contributing, support, governance, the code of conduct, security reporting, and releases are documented in one place: the [Community section of kubemoot.org](https://kubemoot.org/docs/community/). Ask questions and share ideas in [GitHub Discussions](https://github.com/orgs/kubemoot/discussions). Write to moot@kubemoot.org for anything else. Use security@kubemoot.org only to report a vulnerability, privately.

To report a bug or request a feature, open an issue on the repository using its template.
Report a vulnerability privately, as the
[Security page](https://kubemoot.org/docs/community/security/) describes.

Before you open a pull request:

- Read [Contributing](https://kubemoot.org/docs/community/contributing/) for the process,
  commit conventions, and testing expectations, and the
  [Development Guide](https://kubemoot.org/docs/community/development/) for how to build
  and test each component.
- Use a [Conventional Commits](https://www.conventionalcommits.org/) prefix; the prefix
  sets the version bump. See [Releases and Versioning](https://kubemoot.org/docs/community/releases/).
- Include tests with the change: new functionality gets tests in the component's
  automated test suite, and a bug fix gets a test that fails without it.
- Run the component's linter and fix what it reports. A false positive is suppressed on
  its line with the reason, never by turning a rule off. See
  [Linters and warnings](https://kubemoot.org/docs/community/contributing/#linters-and-warnings).

Contributions are licensed under the Apache License 2.0, the license of the repository
you contribute to. Sign off every commit with the
[Developer Certificate of Origin](https://developercertificate.org/) (`git commit -s`);
a pull request check verifies it. There is no CLA.
