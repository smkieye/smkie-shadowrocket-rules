# Public Shadowrocket rule conversions

This public repository contains conversions of 23 public upstream rule sets and an owner-approved public copy of smkie-QCY.conf. The configuration includes personal group names, node names and custom routing domains, but no proxy server addresses, credentials, subscription URLs or tokens.

The data comes from MetaCubeX/meta-rules-dat and qichiyuhub/rule. All source URLs are listed in `sources.json`; `rules-manifest.json` records validation counts and checksums.

`update_rules.py` uses the Python standard library. It downloads and validates all sources before replacing existing rule files. An unsupported or failed response stops the run; the previously committed rules remain available.

The included GitHub Actions workflow requests updates daily at 05:00 Asia/Shanghai. Actual execution can be delayed by GitHub. It commits only changed rule data, uses the repository-scoped built-in GITHUB_TOKEN, and requires no personal access token. Scheduled workflows in inactive public repositories may be disabled by GitHub; monitor Actions and re-enable if necessary.

Shadowrocket must also have configuration automatic background updates enabled. For a locally imported configuration without `update-url`, that refreshes the referenced remote rule sets, while personal strategy groups and custom domains stay in the local configuration. Device and OS background-execution restrictions can delay or prevent refreshes.

Rule endpoints: `https://raw.githubusercontent.com/smkieye/smkie-shadowrocket-rules/main/rules/<name>.list`. The private repository remains available as a separate copy.

## 直接下载配置

[smkie-QCY.conf](https://raw.githubusercontent.com/smkieye/smkie-shadowrocket-rules/main/smkie-QCY.conf) 无需登录，可粘贴到 Shadowrocket 的配置下载地址。导入后启用该配置，并在“设置 → 配置 → 自动后台更新”选择“1 天”。规则库每日更新；本配置没有 update-url，策略组和自定义规则修改需手动重新下载。
