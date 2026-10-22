# Amazon product listing text candidate

Version `2026-10-22.1` packages two selected text checks adapted from
Amazon.com's [Product detail page rules](https://sellercentral.amazon.com/help/hub/reference/external/G200390640),
observed publicly in English-US for United States applicability on 22 October
2026. This is an **authored candidate**, without platform endorsement, maintainer
semantic approval or eligibility for hosted library checks.

## Scope and limitations

Supply English listing text in `input.text`. One rule denies included contact
numbers, mailing addresses, email addresses, website URLs or outside ordering /
payment instructions. The positive rule permits a clear physical-product
description with features/specifications and none of those selected issues.
Other text defaults to `review`; evaluation errors remain `failure`.

This preserves the exact existing two-rule demo policy identity. The source is
much broader. Read [coverage.json](coverage.json): other content restrictions,
style, price/availability/condition, claims, category rules, images, ownership,
identifiers, duplicates, editing history and account authority remain deferred.
An `allow` applies only to the selected checks. For example, the fixture
`price-outside-selected-scope` allows a product description containing a price,
even though the source separately excludes price details. It is not Amazon
approval or proof of overall compliance.

The positive physical-product boundary is deliberately narrower than the
source's product types. The outside-order/payment wording is a conservative
adaptation of the external ordering-link and advertising restrictions, including
instructions without a link. Contact details remain included when quoted in a
warning, and the URL rule has no same-platform exception. No linked page, image,
product truth or seller assertion is verified.

## Reproduce offline

Install the [released Antaeus v0.7.0 CLI](https://github.com/antaeusio/antaeus/releases/tag/v0.7.0).
From a clean repository checkout:

```sh
policy_dir=policies/amazon-product-detail-rules/versions/2026-10-22.1
antaeus version
antaeus validate "$policy_dir/policy.json"
antaeus test --policy "$policy_dir/policy.json" \
  --suite "$policy_dir/cases.json" --fixture-set "$policy_dir/fixtures.json"
python3 scripts/verify.py --cli "$(command -v antaeus)"
```

Policy digest:
`sha256:a638ac46976967809b263c17c0b6baef8df9128bf81a13f7043cf03d7afcab3e`.
The portable JSON identity matches the existing demo; its public library metadata
and expanded cases require their own qualification. The library state remains
`candidate` / `not_evaluated`.

The 22 original synthetic content cases cover contact types, numerical product
specifications, quotations, outside ordering, ambiguous text, instructions to
the checker and an explicit omitted-check example. Two additional synthetic
engine scenarios check failure-over-allow and deny-over-uncertainty reduction.
Fixtures supply exact rule evidence without credentials or network access;
they do not classify the input or measure semantic accuracy. Passing fixtures
must not be presented as successful live evaluation of these cases.

## Source observation and corrections

[provenance.json](provenance.json) uses browser-observation format 2. It records
the primary article's `.help-content` match index 0 of 2, `innerText`, no
normalization and the exact UTF-8 hash/size. No source snapshot is redistributed.
There is no linked HTTP response, automated retrieval qualification or freshness
certification. Consumers supporting only format 1 must refuse this version
until separately updated. Listed dependencies remain unresolved.

Report corrections with this exact version, a clause/rule and an original
synthetic case through an issue or candidate pull request. Do not submit private
listing or customer data. Published versions remain immutable; changed bytes
require a new version and fresh evidence. The project license covers its original
rules/metadata, not Amazon's policy text or marks.
