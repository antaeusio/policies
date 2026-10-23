# eBay semantic study stopped on a mismatch

Observed 23 October 2026. **Qualification failed; the 24-case study is incomplete.**
The candidate is unavailable for hosted library checks.

This report concerns authored version `2026-10-22.1` at
[artifact commit `79f9b79`](https://github.com/antaeusio/policies/tree/79f9b79fa90e60b7f0fb4eebd8941327cf95dd7c/policies/ebay-chance-listings/versions/2026-10-22.1),
policy digest `sha256:9d57f466cdf2a9db06672befdb4bbf8c99bb88acfb6df59f2cc4c856da330f3f`.
It evaluates selected listing-text requirements from eBay's
[Chance listings policy](https://www.ebay.com/help/policies/prohibited-restricted-items/chance-listings-policy?id=4311).
It does not certify a sale or overall eBay compliance.

## Observed results

The frozen suite specified 24 original synthetic content cases. The live
runner stopped at the first mismatched final outcome, after four evaluations.
No case was retried, relabeled or removed to obtain a passing study.

| Case | Frozen expectation | Observed final outcome |
| --- | --- | --- |
| `raffle-ticket` | deny | deny |
| `contest-prize` | deny | deny |
| `random-winner-paraphrase` | deny | deny |
| `mystery-general-contents` | allow | deny |

The last original synthetic input was:

> Each mystery stationery box contains six unused notebooks and two pens. Cover colors vary. No bonus or prize is offered.

Its expectation follows the selected text rules: the contents are described,
and ordinary color variation does not establish an unequal bonus. The response
matched `unequal-bonuses` with confidence 0.8225 and `described-mystery-offer`
with confidence 0.9829. The matched deny determined the final outcome. Two
other rules were indeterminate, so removing the erroneous deny alone would not
establish an allow under this profile.

The first three final outcomes matched their expectations, but some individual
rules also reported matches that their inputs do not support. A matching final
outcome does not establish correct reasoning for every rule. This stopped batch
is not an accuracy estimate, a completed benchmark or semantic qualification.
Twenty content cases were not run.

## Identity and evidence

[results.json](results.json) contains all four original synthetic inputs,
expectations, final outcomes, rule evidence, execution traces and known usage
counts. These are observations from the actual semantic evaluator, distinct from
the candidate's 26 offline fixture cases. The two engine-only fixtures were not
added to the 24 live content cases.

- Released engine: Antaeus `v0.7.0 (73f5127ad6b8)`.
- Observed evaluator alias: `antaeus-semantic-v3`; adapter `io.antaeus.systemone` version `0.4.0`.
- The projected response does not expose an underlying provider/model revision.
- Profile digest: `sha256:467e77e77fa68364f66bfff75d011855efd2250c7b7ac0897edd2b3404f3c6b8`.
- Confidence threshold: 0.7; at most two configured attempts per evaluation.
- Observed: one upstream attempt per case, four total; reported input 2,092 tokens and output 622 tokens.
- Execution terminal: `evaluation.unresolved_rule` for cases 1, 3 and 4; `completed` for case 2. Unresolved evidence can coexist with a final deny and is not an operational failure.

The underlying cause of the incorrect rule matches has not been established.
The evidence concerns this artifact/evaluator/profile combination. It does not
isolate the cause to the authored wording, engine, adapter or provider.

The original six version files, expected labels and fixture evidence remain
unchanged. Their `not_evaluated` provenance describes publication-time state;
this later report records the failed live attempt. It grants no catalog
promotion, maintainer review, source-freshness certification or runtime
eligibility. Any remediation needs new versioned evidence and review while
preserving this failure.
