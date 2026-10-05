# llm-response-evaluation-system — project architecture

[README](README.md) · [Interview questions and answers](INTERVIEW_QA.md)

## Purpose and scope

Same overlap scorer as RAG eval, aimed at LLM answers.

This document describes files and symbols in this checkout. Deployment templates and statements in the original overview are distinguished from a verified running environment.

## Component diagram

```mermaid
flowchart LR
    M0["src/llmeval/__init__.py"]
    M1["src/llmeval/main.py"]
    M2["src/llmeval/score.py"]
    M1 -->|imports| M2
```

For Python repositories, arrows show resolved local imports, not network calls or deployment order. Otherwise the diagram is a repository component map; containment arrows do not assert runtime integration.

## Components and responsibilities

| Component | Responsibility |
| --- | --- |
| [`src/llmeval/main.py`](src/llmeval/main.py) | HTTP handlers: `GET /healthz`, `POST /evaluate` |
| [`src/llmeval/score.py`](src/llmeval/score.py) | Functions: `words`, `evaluate` |
| [`requirements.txt`](requirements.txt) | Implementation or supporting configuration |
| [`src/llmeval/__init__.py`](src/llmeval/__init__.py) | Implementation or supporting configuration |
| [`tests/test_eval.py`](tests/test_eval.py) | Executable checks and regression examples |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | GitHub Actions job definitions |
| [`README.md`](README.md) | Project explanations or operating notes |

## Request interface

| Method and path | Handler | Source |
| --- | --- | --- |
| `GET /healthz` | `healthz` | [`src/llmeval/main.py`](src/llmeval/main.py#L8) |
| `POST /evaluate` | `post_evaluate` | [`src/llmeval/main.py`](src/llmeval/main.py#L13) |

The table lists literal route decorators found in the inspected Python modules. Router prefixes and middleware can add behavior; check the linked handler and application setup before calling an endpoint.

## Implementation walkthrough

### `evaluate(answer, gold, context)`

Source: [`src/llmeval/score.py`](src/llmeval/score.py#L10).

Calls visible in this function: `len`, `round`, `words`.

```python
def evaluate(answer, gold, context):
    aw, gw, cw = words(answer or ""), words(gold or ""), words(context or "")
    faithfulness = len(aw & cw) / len(aw) if aw else 0
    correctness = len(aw & gw) / len(gw) if gw else 0
    return {
        "faithfulness": round(faithfulness, 4),
        "correctness": round(correctness, 4),
        "passed": faithfulness >= 0.5 and correctness >= 0.5,
    }
```

### `words(text)`

Source: [`src/llmeval/score.py`](src/llmeval/score.py#L6).

Calls visible in this function: `re.findall`, `set`, `text.lower`.

```python
def words(text):
    return set(re.findall(r"[a-z0-9]+", text.lower())) - STOP
```

## Data and state

- [`src/llmeval/score.py`](src/llmeval/score.py) defines module-level containers: `STOP`.

Module-level dictionaries/lists live in a Python process. They can be fixtures or mutable state; inspect writes before treating them as persistent storage. A production extension would need to define persistence and concurrency behavior explicitly.

## Data flow and design decisions

### What is the input-to-output contract of `evaluate`

In [`src/llmeval/score.py`](src/llmeval/score.py#L10), `evaluate(answer, gold, context)` receives the inputs. The function computes these intermediate values:

- `aw, gw, cw = (words(answer or ''), words(gold or ''), words(context or ''))`
- `faithfulness = len(aw & cw) / len(aw) if aw else 0`
- `correctness = len(aw & gw) / len(gw) if gw else 0`

Its result is defined by:

- `{'faithfulness': round(faithfulness, 4), 'correctness': round(correctness, 4), 'passed': faithfulness >= 0.5 and correctness >= 0.5}`

## Setup and verification

The following commands are derived from the checked-in dependency/test contracts. Execute them from the repository root; the block prepares a local environment, not a cloud deployment.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

Python dependencies: [`requirements.txt`](requirements.txt).

Test entry points: [`tests/test_eval.py`](tests/test_eval.py).

Automation definitions: [`.github/workflows/ci.yml`](.github/workflows/ci.yml). Read their triggers and job steps to determine what CI actually runs.

## Operating boundaries and design review

Before turning this checkout into a customer deployment, establish the input contract, data ownership, access controls, failure response, evaluation criteria, and rollback owner. Repository fixtures and unit tests demonstrate local behavior; they do not establish throughput, uptime, compliance, or business impact.

A useful architecture review starts with the linked implementation: identify where input enters, where a decision is made, which state can change, and which external dependency can fail. Add a deployment view only for infrastructure that is actually configured and exercised.
