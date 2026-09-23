# Security Policy

This is the org-wide default. Kubemoot is `v1alpha1`: under active development, not
production-ready, and run on a homelab with production-like patterns rather than in a
production environment.

## Supported versions

Security fixes target the latest minor release of each repo. Older minor releases do
not receive backported fixes.

## Reporting a vulnerability

Report privately using GitHub's private vulnerability reporting on the affected
repo: open the repo's **Security** tab and choose **Report a vulnerability**. Do not
open a public issue for a security report.

<!-- TODO: security@kubemoot.org is a placeholder mailbox; wire it up (or replace
     this line) before relying on it as a fallback. -->

If private reporting is not available on a given repo, email security@kubemoot.org
as a fallback.

We acknowledge reports within a reasonable period and coordinate disclosure with the
reporter before any public announcement. With a single maintainer, treat this as best
effort rather than a guaranteed SLA.

## Known limitations

These are current, deliberate gaps, not hidden ones. They are listed here so you can
decide whether they matter for your deployment.

- **NATS has no per-crew account isolation.** Every crew on a cluster shares the same
  NATS deployment without per-crew accounts, so a crew can read another crew's
  discussion messages. Do not run crews with different trust boundaries on the same
  cluster until this is addressed.
- **Images are published for `linux/amd64` only at launch.** There is no
  `linux/arm64` build yet, including for Apple Silicon.
- **Admission webhooks require cert-manager.** If cert-manager is not installed, the
  operator's admission webhooks will not come up; the quickstart runs with webhooks
  off for exactly this reason.

<!-- TODO: link to the docs site's security/known-limitations page once the URL is
     live. -->
