# langgenius/dify-2024-12-10-2024-12-12 更新摘要

# 更新摘要
本次更新主要集中在修复问题和增强功能，提升用户体验和系统稳定性。

## 主要更新
- 🐛 修复了PDF预览功能在构建中的问题 (#11621)
- 🐳 在开发容器中添加了停止Docker容器的别名功能 (#11616)

## 重要修复
- 🔧 修复了在流式生成异常发生时未释放RateLimit请求的问题 (#11540)
- 🔧 解决了并行模式下节点迭代的令牌计数错误 (#11539)

## 新增功能
- 🌙 为日志和注释添加了深色模式 (#11575)
- 🚀 集成了opendal存储功能 (#11508)

## 其他说明
- 更新了多个模型，包括添加Gemini 2.0 Flash Exp和llama-3.3模型 (#11604, #11533)
- 进行了多项国际化文件的翻译更新，提升了多语言支持 (#11577, #11545)

---

# 详细内容


## langgenius/dify

### No releases found

### Recent Commits
- [`3d803c2`] Fix/pdf preview in build (#11621) (by zxhlyh)
- [`fa3dcbb`] feat(devcontainer): add alias to stop Docker containers (#11616) (by Hiroshi Fujita)
- [`ee34206`] ci: better print version for ruff to check the change (#11587) (by yihong)
- [`bb3bc60`] feat(model): add vertex_ai Gemini 2.0 Flash Exp (#11604) (by JasonVV)
- [`e7a4cfa`] fix: name of llama-3.3-70b-specdec (#11596) (by crazywoola)
- [`6478aa1`] Added new models and Removed the deleted ones for Groq #11455 (#11456) (by Alok Shrivastwa)
- [`7b58393`] [ref] use one method to get boto client for aws bedrock (#11506) (by Warren Chen)
- [`a360af8`] chore: translate i18n files (#11577) (by github-actions[bot])
- [`36cb25b`] fix: support mdx files close #11557 (#11565) (by yihong)
- [`e565ecd`] fix: change workflow trace id (#11585) (by Joe)
- [`f96fdc2`] Feat: dark mode for logs and annotations (#11575) (by KVOJJJin)
- [`0d04cdc`] Lindorm vdb (#11574) (by Jiang)
- [`926f604`] feat: add gemini-2.0-flash-exp (#11570) (by 非法操作)
- [`1807436`] fix: better opendal tests (#11569) (by yihong)
- [`d05f189`] Fix: RateLimit requests were not released when a streaming generation exception occurred (#11540) (by liuzhenghua)
- [`ceaa9f1`] chore: translate i18n files (#11545) (by github-actions[bot])
- [`6f4cbe0`] fix: workflow continue on error doc link (#11554) (by zxhlyh)
- [`8d4bb9b`] feat: integrate opendal storage (#11508) (by -LAN-)
- [`1765fe2`] fix: iteration node in parallel mode token count error (#11539) (by Novice)
- [`79a710c`] Feat: continue on error (#11458) (by Novice)
- [`bec5451`] feat: workflow continue on error (#11474) (by zxhlyh)
- [`86dfdcb`] chore: update thai lang in app page (#11541) (by Yi Xiao)
- [`42d986b`] [Pixtral] Add new model ; add vision (#11231) (by Tommy)
- [`fbc4ca9`] fix: Remove duplicate 'response_format' parameter from model YAML files (#11531) (by zkyTech)
- [`80c52e0`] feat: Add llama-3.3 models for Groq (#11533) (by Paul van Oorschot)
- [`50b76dd`] fix: better error message for url add external knowledge (#11537) (by yihong)
- [`225fcd5`] Revert "fix: total tokens is wrong which is zero in inter way, close … (#11536) (by yihong)
- [`afffd34`] fix: can not start local by REMOTE_SETTINGS_SOURCE_NAME change it to … (#11535) (by yihong)
- [`7165760`] fix: issue 11247 that Completion mode content maybe list or str (#11504) (by yihong)
- [`28231d3`] Remove the processing of single quote when testing API tools. (#11390) (by Wei Mingzhi)

