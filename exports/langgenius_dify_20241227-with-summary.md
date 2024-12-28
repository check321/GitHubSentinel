# AI 生成的更新摘要

# 更新摘要
本次更新主要集中在修复错误和添加新功能，改善用户体验。

## 主要更新
- 🛠️ 修正测试中允许的未使用导入设置，以清理未使用的导入。
- 💬 修改了英语（美国）翻译。

## 重要修复
- 🐞 修复工作流作为工具的输出文件引发的错误。
- ⚠️ 解决工作流页面的警告问题，避免访问失败。
- 🔍 修复头像下拉菜单的键盘导航问题。

## 新增功能
- 🚀 支持多版本工作流。
- 🆕 支持 Ernie-lite-pro-128k 模型。
- 💾 为 Anthropic Claude 模型添加了提示缓存功能（尚未合并）。

## 其他说明
- 当前存在一些未解决的问题，例如文本生成超时设置无效及密码重置功能未发送验证邮件等，这些问题仍需关注和解决。

---

# 原始更新内容


## langgenius/dify

### No releases found

### Recent Commits
- [`72ae414`] chore(lint): correct allowed-unused-imports settings for cleanup unused imports in tests (#11922) (by Bowen Liang)
- [`4c9618b`] [fix] modify en-US (#12169) (by Warren Chen)
- [`901028f`] [feat] Support Multi-Version Workflows (#11990) (by Warren Chen)
- [`adfbfc1`] Modify translation for error branch and update for the parent-child f… (#12127) (by Hanqing Zhao)
- [`b66c03d`] fix: workflow_as_tool output files raise error (#12061) (by 非法操作)
- [`2a909e6`] feat: support Ernie-lite-pro-128k (#12161) (by Kepler)
- [`9d86056`] chore: add cursor pointer for option card (#12119) (by AkaraChen)
- [`309fd76`] fix: comfyui output image's format (#12121) (by 非法操作)
- [`a3293b1`] fix: type is wrong issue (#12165) (by yihong)
- [`eb8963a`] fix: workflow page throw warning: Attempts to access this ref will fail (#12166) (by NFish)
- [`89ce9a5`] Fix: avatar dropdown keyboard navigation (#12155) (by NFish)
- [`f4f2567`] owner and admin have all permission of knowledge base (#12157) (by Jyong)
- [`5a3fe61`] disable all chunks status when disable document (#12149) (by Jyong)
- [`55c327f`] fix: handle case where member is not found in role update API (#12156) (by -LAN-)

### Recent Issues
- #12174 [Possible issue with # of words not being recalculated after retry](https://github.com/langgenius/dify/issues/12174) (open)
- #12170 [Web Timeout: Setting TEXT_GENERATION_TIMEOUT_MS Not Effective](https://github.com/langgenius/dify/issues/12170) (open)
- #12169 [[fix] modify en-US](https://github.com/langgenius/dify/pull/12169) (closed)
- #12167 [The workspace in the upper right corner cannot be pulled down and then opened the Google browser to check](https://github.com/langgenius/dify/issues/12167) (open)
- #12166 [fix: workflow page throw warning: Attempts to access this ref will fail](https://github.com/langgenius/dify/pull/12166) (closed)
- #12165 [fix: type is wrong issue](https://github.com/langgenius/dify/pull/12165) (closed)
- #12164 [feat(llm): Add prompt caching for Anthropic Claude models](https://github.com/langgenius/dify/pull/12164) (open)
- #12163 [Add new workspace](https://github.com/langgenius/dify/issues/12163) (closed)
- #12162 [Memory on-off function for answer node](https://github.com/langgenius/dify/issues/12162) (closed)
- #12161 [feat: support Ernie-lite-pro-128k](https://github.com/langgenius/dify/pull/12161) (closed)
- #12160 [fix: inputs variables value changed but not work on Chatflow App](https://github.com/langgenius/dify/pull/12160) (open)
- #12159 [api tool multiple server url](https://github.com/langgenius/dify/issues/12159) (open)
- #12158 [Vector database connection error when using Qwen text-embedding-vX](https://github.com/langgenius/dify/issues/12158) (open)
- #12157 [owner and admin have all permission of knowledge base](https://github.com/langgenius/dify/pull/12157) (closed)
- #12156 [fix: handle case where member is not found in role update API](https://github.com/langgenius/dify/pull/12156) (closed)
- #12155 [Fix: avatar dropdown keyboard navigation](https://github.com/langgenius/dify/pull/12155) (closed)
- #12154 [Forgot password feature not sending the verification code email](https://github.com/langgenius/dify/issues/12154) (open)

### Recent Pull Requests
- #12169 [[fix] modify en-US](https://github.com/langgenius/dify/pull/12169) by @warren830 (closed)
- #12166 [fix: workflow page throw warning: Attempts to access this ref will fail](https://github.com/langgenius/dify/pull/12166) by @douxc (closed)
- #12165 [fix: type is wrong issue](https://github.com/langgenius/dify/pull/12165) by @yihong0618 (closed)
- #12164 [feat(llm): Add prompt caching for Anthropic Claude models](https://github.com/langgenius/dify/pull/12164) by @Seayon (open)
- #12161 [feat: support Ernie-lite-pro-128k](https://github.com/langgenius/dify/pull/12161) by @bigfish49 (closed)
- #12160 [fix: inputs variables value changed but not work on Chatflow App](https://github.com/langgenius/dify/pull/12160) by @liuzhenghua (open)
- #12157 [owner and admin have all permission of knowledge base](https://github.com/langgenius/dify/pull/12157) by @JohnJyong (closed)
- #12156 [fix: handle case where member is not found in role update API](https://github.com/langgenius/dify/pull/12156) by @laipz8200 (closed)
- #12155 [Fix: avatar dropdown keyboard navigation](https://github.com/langgenius/dify/pull/12155) by @douxc (closed)
- #12150 [Fix: The topk parameter doesn't work in sagemaker rerank tool](https://github.com/langgenius/dify/pull/12150) by @ybalbert001 (closed)
- #12149 [disable all chunks status when disable document](https://github.com/langgenius/dify/pull/12149) by @JohnJyong (closed)
- #12139 [Fix Postgres user name in docker-compose.yaml](https://github.com/langgenius/dify/pull/12139) by @regnull (open)
- #12137 [feat: Add GROWI tool](https://github.com/langgenius/dify/pull/12137) by @miya (open)
- #12133 [fix: import jieba.analyse](https://github.com/langgenius/dify/pull/12133) by @laipz8200 (closed)
- #12131 [feat: Auto-switch to authorized workspace when accessing URL](https://github.com/langgenius/dify/pull/12131) by @aconeshana (open)
- #12127 [Modify translation for error branch and update for the parent-child f…](https://github.com/langgenius/dify/pull/12127) by @HanqingZ (closed)
- #12124 [fix: issue #11920 api docker build](https://github.com/langgenius/dify/pull/12124) by @kenwoodjw (closed)
- #12121 [fix: comfyui output image's format](https://github.com/langgenius/dify/pull/12121) by @hjlarry (closed)
- #12119 [chore: add cursor pointer for option card](https://github.com/langgenius/dify/pull/12119) by @AkaraChen (closed)

