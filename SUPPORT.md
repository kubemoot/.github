# Support

Kubemoot has no commercial support. Support is community, best effort, single
maintainer.

## First, try the quickstart

If you are new here, run the quickstart on an empty `kind` cluster before asking a
question. It takes a few minutes and exercises the same path CI checks on every
release:

```bash
kind create cluster --name kubemoot
./quickstart/quickstart.sh
```

If that fails, it is likely the fastest path to your answer: see the "quickstart
failed" issue template below.

## Have a question?

Use [Discussions](https://github.com/orgs/kubemoot/discussions), not Issues.
Discussions are for "how do I," "is this expected," "what's the right pattern for,"
and anything where you are not sure yet whether it is a defect.

## Found a defect?

Open an Issue on the repo where you found it, using the matching template:

- **Bug report** for something that is broken.
- **Feature request** for something that does not exist yet.
- **Quickstart failed** for a fresh-cluster quickstart run that did not work; it asks
  for the exact information needed to reproduce a stranger's environment.

## Everything else

Speaking, press, teaching, or something that fits neither Discussions nor Issues:
write to moot@kubemoot.org. Security reports go to the private channel in
[SECURITY.md](../SECURITY.md), never to this address.

<!-- TODO: link to the docs site once its URL is finalized. -->
