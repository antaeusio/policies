# eBay chance listings text candidate

Version `2026-10-22.1` is an independent authored interpretation of selected
requirements in eBay's [Chance listings policy](https://www.ebay.com/help/policies/prohibited-restricted-items/chance-listings-policy?id=4311),
observed in English on 22 October 2026. It is a **candidate**, not an official,
endorsed, maintainer-reviewed or currently servable platform policy.

## Scope

The six rules screen the offer described by a complete English listing title
and description supplied as `input.text`. They cover chance entries, bonus
uniformity, mystery-box contents disclosures and the valuable-item exception.
Breaks, trading-card repacks and giveaways/sweepstakes need separate approval
facts and are excluded from positive rules. Other agreements and restrictions
still apply. Read [coverage.json](coverage.json) before reuse.

An `allow` describes the supplied wording under these selected rules. It does
not verify delivery, account approval, product authenticity, images, external
links or the truth of seller statements. An unrelated listing defaults to
`review`. Unresolved conditions also require review; evaluation errors remain
`failure`.

## Reproduce offline

Install the [released Antaeus v0.7.0 CLI](https://github.com/antaeusio/antaeus/releases/tag/v0.7.0).
From a clean checkout of this repository:

```sh
policy_dir=policies/ebay-chance-listings/versions/2026-10-22.1
antaeus version
antaeus validate "$policy_dir/policy.json"
antaeus test --policy "$policy_dir/policy.json" \
  --suite "$policy_dir/cases.json" --fixture-set "$policy_dir/fixtures.json"
python3 scripts/verify.py --cli "$(command -v antaeus)"
```

The policy digest is
`sha256:9d57f466cdf2a9db06672befdb4bbf8c99bb88acfb6df59f2cc4c856da330f3f`.
`policy.json` uses the released JSON form of the portable policy contract;
there is no second YAML copy to drift.

The suite has 24 synthetic content cases and two explicit engine-reduction
scenarios. Fixture-backed execution supplies exact rule evidence, without
credentials or network access. It verifies bindings and outcome reduction;
it **does not classify the text or measure semantic accuracy**. Live semantic
evaluation is not qualified for this version.

The suite includes a mystery box with a collectible included in every purchase,
a selectively included collectible, vague descriptions, approval claims,
quotations and attempts to instruct the checker. The additional failure and
deny-over-uncertainty scenarios are engine fixtures, not listing classifications.

## Source identity and corrections

[provenance.json](provenance.json) records the research response/article hashes
and authoring method. No source snapshot is redistributed. The research
extractor is not the hosted extractor; a fresh page may differ. These hashes
identify an observation, not source authenticity or permission to redistribute.

Report errors with the exact version, clause/rule and an original synthetic case
through an issue or candidate pull request. Do not submit private listing or
customer data. New policy bytes require a new immutable version; review cannot
carry over automatically. The project license covers original rules/metadata,
not eBay's source text or marks.
