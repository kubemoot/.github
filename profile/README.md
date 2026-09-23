# Kubemoot

Kubemoot is a Kubernetes operator for running crews of LLM agents that hold
consensus discussions instead of answering alone. A crew, its models, its RAG
sources, and its MCP tools are Custom Resources: declared, versioned, reviewed, and
applied through GitOps, the same way you already manage the rest of the cluster.

Agent behavior is governed by ADL (Agent Definition Language): WHEN/THEN, ASSERT, and
NEVER rules, shipped as `PromptModule` Custom Resources instead of free-text prompts
buried in application code. A moot is an assembly that meets to discuss and decide; a
Kubemoot crew does the same, with a coordinator that determines when the discussion
has settled.

## Quickstart

```bash
kind create cluster --name kubemoot
./quickstart/quickstart.sh
```

That installs the operator, a small CPU model, and a two-agent crew, then has the
crew answer a question. See [kubemoot/quickstart](https://github.com/kubemoot/kubemoot/tree/main/quickstart)
for what each step does.

## Repos

- **[kubemoot](https://github.com/kubemoot/kubemoot)**, the operator: controllers,
  CRDs, the agent runtime, and the dashboard.
- **[crews](https://github.com/kubemoot/crews)**, a collection of crew definitions,
  from the minimal quickstart crew to fuller reference examples.
- **[kmctl](https://github.com/kubemoot/kmctl)**, the terminal CLI for working with
  crews and conversations, the `kubectl`-style counterpart to CrewForge.
- **[kubemoot-docs](https://github.com/kubemoot/kubemoot-docs)**, the documentation
  site: a Hugo and Docsy shell that aggregates each component's own docs.
- **[crew-forge](https://github.com/kubemoot/crew-forge)**, a desktop app for
  authoring crews and their CRDs without hand-writing YAML.

## Status

`v0.x`, alpha API (`v1alpha1`). Built and run on a homelab with production-like
patterns, not a production deployment.

<!-- TODO: kubemoot.org is planned as the project website, with kubemoot.org/docs as
     the hosted reference; link both here once DNS and the site are live. -->
