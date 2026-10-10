# Public Shadowrocket rule conversions

This public repository contains only conversions of 23 already-public upstream rule sets. It contains no personal configuration, custom routing domains, proxy group definitions, proxy server names, server credentials, user YAML or subscription tokens.

The data comes from MetaCubeX/meta-rules-dat and qichiyuhub/rule. All source URLs are listed in `sources.json`; `rules-manifest.json` records validation counts and checksums.

`update_rules.py` uses the Python standard library. It downloads and validates all sources before replacing existing rule files. An unsupported or failed response stops the run; the previously committed rules remain available.

The included GitHub Actions workflow requests updates daily at 05:00 Asia/Shanghai. Actual execution can be delayed by GitHub. It commits only changed rule data, uses the repository-scoped built-in GITHUB_TOKEN, and requires no personal access token. Scheduled workflows in inactive public repositories may be disabled by GitHub; monitor Actions and re-enable if necessary.

Shadowrocket must also have configuration automatic background updates enabled. For a locally imported configuration without `update-url`, that refreshes the referenced remote rule sets, while personal strategy groups and custom domains stay in the local configuration. Device and OS background-execution restrictions can delay or prevent refreshes.

Rule endpoints: `https://raw.githubusercontent.com/smkieye/smkie-shadowrocket-rules/main/rules/<name>.list`. Personal configurations are maintained separately in a private repository.
