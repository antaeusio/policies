# Facebook selected spam text candidate

Version `2026-10-22.1` interprets selected parts of [Meta Spam](https://transparency.meta.com/policies/community-standards/spam/), observed publicly in English (US) on 22 October 2026. This is an **authored candidate**, with no platform endorsement, live semantic qualification, maintainer semantic approval or eligibility for hosted library checks.

## Selected scope

Supply English proposal text in `input.text`. Six rules cover described platform-asset trades, paid/bartered platform privileges, engagement exchanges, claimed or required engagement before promised content, and conditional positive exceptions for unpaid cross-promotion and interest-based moderation handovers. Other text defaults to `review`; evaluation errors remain `failure`.

Reciprocal sharing of promotional content can fall within unpaid cross-promotion when it is not triggered by third-party payment. Reciprocity alone cannot erase that exception. Pure follow-for-follow metric trading is distinct. Unresolved purpose, payment or overlapping exchange conditions require review. Describing interest does not turn a paid admin-role sale into a voluntary handover. A claim that engagement is required before promised content is selected even without a proven technical gate.

A relevant unverified Meta-approval/newsworthiness claim requires review, never permission. The deny conditions leave that external exception question unresolved rather than presenting a selected judgment as full platform enforcement. Warnings/quotations that are not themselves offers do not become trading proposals; instructions to the checker remain data.

Read [coverage.json](coverage.json). The whole monetary-content-exchange category and branded-content exception are deferred pending linked-policy review; a creator fee alone is not a selected violation. Frequency/history, deceptive destinations, cloaking, platform-mimic interfaces, actual authority and other account/link facts are unverified. An `allow` is only a judgment on the described proposal under selected checks, not Facebook or Meta approval, verified conduct, or full-source compliance. This does not qualify ads, Marketplace or other Meta products.

## Reproduce offline

Install the [released Antaeus v0.7.0 CLI](https://github.com/antaeusio/antaeus/releases/tag/v0.7.0). From a clean repository checkout:

```sh
policy_dir=policies/meta-spam/versions/2026-10-22.1
antaeus version
antaeus validate "$policy_dir/policy.json"
antaeus test --policy "$policy_dir/policy.json" \
  --suite "$policy_dir/cases.json" --fixture-set "$policy_dir/fixtures.json"
python3 scripts/verify.py --cli "$(command -v antaeus)"
```

Policy digest: `sha256:512717b449ea7909ac22b88d957869be825bd1822fea6e11051fda8550af99ee`.

The 26 original synthetic content cases include platform/privilege transactions, cash and item rewards, gate claims, ordinary goods, optional engagement, voluntary handovers, reciprocal promotional-sharing boundaries, deferred paid/branded content, quotations and checker instructions. Two additional synthetic engine scenarios check failure-over-allow and deny-over-uncertainty reduction. Fixtures supply exact rule evidence without credentials or network access: they do not classify text or establish semantic accuracy. Passing them is not live evaluation of these cases. State remains `candidate` / `not_evaluated`.

## Source observation and corrections

[provenance.json](provenance.json) records browser-observation format 2: selected Today tabpanel `[role="tabpanel"]`, index 0 of 1, `innerText`, no normalization, exact UTF-8 hash/size. Today and historical Jun 26, 2024 tab labels are not substituted for a full effective date. No source snapshot is redistributed; there is no linked HTTP response or automated retrieval/freshness certification. Format-1-only consumers must refuse this version until separately updated. Dependencies remain unresolved.

Report corrections with this version, a clause/rule and an original synthetic case through an issue or candidate pull request. Do not submit private account or customer data. Published bytes remain immutable: changes require a new version and fresh evidence. The project license covers original rules/metadata, not Meta's source text or marks.
