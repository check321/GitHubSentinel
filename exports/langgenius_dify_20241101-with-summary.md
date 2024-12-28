# langgenius/dify-2024-11-01-2024-11-05 更新摘要

# 更新摘要
本次更新涉及多个重要修复和功能增强，版本号更新至 0.11.0。

## 主要更新
- 更新了 CI 流程，提升构建速度和效率。
- 支持新的图像格式，包括 PNG、GIF 和 WEBP。

## 重要修复
- 修复了在 CleanProcessor.clean 中访问规则时的 KeyError 问题。
- 修复了 Claude 3.5 Haiku 模型在 Amazon Bedrock 上的 max_tokens 设置错误。

## 新增功能
- 新增对 anthropic/claude-3-5-haiku 模型的支持。
- 添加了 SSRF 请求超时配置项。

## 其他说明
- 更新了 README 文档，修正了多个文档中的错误链接。

---

# 详细内容


## langgenius/dify

### Latest Release
- Version: 0.11.0
- Title: v0.11.0
- Published at: 2024-11-05T09:55:23Z
- URL: https://github.com/langgenius/dify/releases/tag/0.11.0

### Recent Commits
- [`eafe5a9`] chore(ci): bring back poetry cache to speed up CI jobs (#10347) (by Bowen Liang)
- [`d45d90e`] chore: lazy import sagemaker (#10342) (by Bowen Liang)
- [`42a9374`] chore: update translation for 'account' from '계좌' to '계정' (#10350) (by comfuture)
- [`82a775e`] chore(ci): separate vector store tests into new workflow (#10354) (by -LAN-)
- [`1dae1a7`] fix(api): remove fixed source attribute from FileApi (#10353) (by -LAN-)
- [`ac0fed6`] feat: support png, gif, webp (#7947) (by Nam Vu)
- [`fb656d4`] Update README.md (#10332) (by Chenhe Gu)
- [`2b7341a`] Gitee AI tools (#10314) (by 方程)
- [`ce1f9d9`] feat: The SSRF request timeout configuration item is added (#10292) (by Summer-Gu)
- [`bdadca1`] feat: add support for anthropic/claude-3-5-haiku through OpenRouter (#10331) (by Infinitnet)
- [`d7b4d07`] feat(vannaai): add base_url configuration (#10294) (by Benjamin)
- [`1279e27`] docs: remove the TOC part (#10324) (by -LAN-)
- [`d92e3bd`] fix: special prompt not work for comfyUI tool (#10307) (by 非法操作)
- [`7f583ec`] chore: update version to 0.11.0 across all relevant files (#10278) (by -LAN-)
- [`7962101`] fix: iteration none output error (#10295) (by Novice)
- [`ae254f0`] fix(http_request): improve parameter initialization and reorganize tests (#10297) (by -LAN-)
- [`68e0b0a`] fix typo: writeOpner to writeOpener (#10290) (by Matsuda)
- [`5f21d13`] fix: handle KeyError when accessing rules in CleanProcessor.clean (#10258) (by pinsily)
- [`233bffd`] fix: borken faq url in CONTRIBUTING.md (#10275) (by eux)
- [`bf9349c`] feat: add xAI model provider (#10272) (by 非法操作)
- [`4847548`] feat(model_runtime): add new model 'claude-3-5-haiku-20241022' (#10285) (by Matsuda)
- [`cb245b5`] fix(model_runtime): fix wrong max_tokens for Claude 3.5 Haiku on Amazon Bedrock (#10286) (by Matsuda)
- [`249b897`] feat(model): add validation for custom disclaimer length (#10287) (by -LAN-)
- [`08c731f`] fix(node): correct file property name in function switch (#10284) (by -LAN-)
- [`302f440`] refactor the logic of refreshing access_token (#10068) (by NFish)
- [`de5dfd9`] chore: translate i18n files (#10273) (by github-actions[bot])
- [`acb22f0`] Updates: Add mplfonts library for customizing matplotlib fonts and Va… (#9903) (by Benjamin)
- [`d1505b1`] feat: Iteration node support parallel mode (#9493) (by Novice)
- [`cca2e78`] fix(workflow):  handle else condition branch addition error in if-else node (#10257) (by GeorgeCaoJ)
- [`2c4d8db`] feat(document_extractor): support tool file in document extractor (#10217) (by -LAN-)

