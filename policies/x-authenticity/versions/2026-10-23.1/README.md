# X selected authenticity text candidate

Version `2026-10-23.1` interprets selected parts of [X Authenticity](https://help.x.com/en/rules-and-policies/authenticity), observed publicly in English on 22 October 2026. The version date identifies this authored packaging, not an upstream policy change. This is an **authored candidate**, with no platform endorsement, live semantic qualification, maintainer semantic approval or eligibility for hosted library checks.

## Selected scope

Supply English proposal text in `input.text`. Six rules cover described account/username/access trades for value, engagement exchanges or artificial metric inflation, services for those transactions, reporting abuse, manual good-faith reports and good-faith customer-support encouragement. Other text defaults to `review`; evaluation errors remain `failure`.

A described account sale or temporary-access barter is distinct from Teams/OAuth collaboration without a trade. Actual authorization is not verified. The source also discusses X products and affiliation transactions: those are separately deferred, not converted into a general product-purchase ban. Activity frequency, follow-churn, aggressive automation and other behavioral evidence are outside this screen.

Reporting is not automatically abusive. Described manual good-faith reports of believed violations and good-faith customer-support encouragement have narrow positive expectations when no selected abuse/trade is proposed. An explicit false/duplicate mass-report or harassment plan is not excused by calling it good faith. An ambiguous request to report someone remains review. NGO/LEO automation needs actual prior consent and organizational identity; a self-applied label or claimed permission does not establish those facts.

Read [coverage.json](coverage.json). Its 18 source groups include the selected conditions and deferred account/identity/PCF, multi-account/localization/coordination, technical/history, activity-spam, product/affiliation, scam/dispute, media, link and enforcement requirements. An `allow` concerns only the described proposal under selected checks. It is not X approval, proof of a violation, verified account behavior or full-source compliance. Warnings and quotations are interpreted as context; instructions to the checker remain data.

## Reproduce offline

Install the [released Antaeus v0.7.0 CLI](https://github.com/antaeusio/antaeus/releases/tag/v0.7.0). From a clean repository checkout:

```sh
policy_dir=policies/x-authenticity/versions/2026-10-23.1
antaeus version
antaeus validate "$policy_dir/policy.json"
antaeus test --policy "$policy_dir/policy.json" \
  --suite "$policy_dir/cases.json" --fixture-set "$policy_dir/fixtures.json"
python3 scripts/verify.py --cli "$(command -v antaeus)"
```

Policy digest: `sha256:ff6cc375db771fdc3f13b930069c205290317248553daecac141b29fa7323774`.

The 26 original synthetic content cases retain all 24 initial proposals and add two boundaries: delegated work without an account trade, and an explicit false-report plan carrying a good-faith/support label. They cover account/virtual-access transactions, engagement forms, third-party services, good-faith and malicious reporting, missing context, ordinary disputes, unknown URLs, quotations and checker instructions. Two separate synthetic engine scenarios check failure-over-allow and deny-over-uncertainty reduction.

Fixtures supply exact authored rule evidence without credentials or network access. They test bindings and outcome reduction, not model classification or semantic accuracy. Passing them is not a qualified live run. State remains `candidate` / `not_evaluated`; no hosted X policy selection is introduced.

## Source observation and corrections

[provenance.json](provenance.json) uses browser-observation format 2: `#main-content > article`, index 0 of 1, `innerText`, no normalization, exact UTF-8 hash/size. The selected article includes breadcrumb and contents links but excludes navigation/footer. The visible April 2025 label supplies a month, not a full effective date. The final observed URL has no `.html` suffix; no HTTP redirect chain is asserted.

No full third-party snapshot is redistributed. There is no linked HTTP response or automatic retrieval/freshness certification. Format-1-only consumers must refuse this version until separately updated. Listed dependencies and external facts remain unresolved.

Report a correction with this exact version, a clause/rule and an original synthetic case through an issue or candidate pull request. Do not submit private account/customer data or credentials. Published bytes remain immutable; changes need a new version and fresh evidence. The project license covers original rules/metadata, not X source text or marks.
