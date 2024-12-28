# langgenius/dify-2024-12-16 更新摘要

# 更新摘要
本次更新主要集中在增强模型支持和修复多项问题，以提升系统的稳定性和用户体验。

## 主要更新
- 📦 更新至版本 **0.14.0**，发布于 **2024-12-16**。
- 🔧 增强对 **doubao vision 系列模型** 的支持。

## 重要修复
- 🛠️ 修复了 **TiDB 服务** 在 Docker Compose 配置中的可选性问题。
- 🐛 修复了 **内存泄漏** 问题，可能由 **pypdfium2** 引起。
- 🚫 修复了 **图标无法显示** 的问题。

## 新增功能
- 🌙 添加了 **黑暗模式** 的样式支持。
- 🤖 新增了 **Gitee AI V&L 模型** 的支持。
- 🔒 使 **登录锁定时长** 可配置。

## 其他说明
- ⚠️ 修复了一些异常处理，增强了 **知识检索节点** 和 **工具节点** 的稳定性。

---

# 详细内容


## langgenius/dify

### Latest Release
- Version: 0.14.0
- Title: v0.14.0
- Published at: 2024-12-16T07:53:22Z
- URL: https://github.com/langgenius/dify/releases/tag/0.14.0

### Recent Commits
- [`900e93f`] chore: update comments in docker env file (#11705) (by -LAN-)
- [`99430a5`] feat(ark): support doubao vision series models (#11740) (by sino)
- [`c9b4029`] chore: the consistency of MultiModalPromptMessageContent (#11721) (by 非法操作)
- [`78c3051`] fix: make tidb service optional with proper profile in docker compose yaml (#11729) (by Bowen Liang)
- [`cd4310d`] chore:update azure api version (#11711) (by 呆萌闷油瓶)
- [`259cff9`] fix(api/ops_trace): avoid raise exception directly (#11732) (by -LAN-)
- [`7b7eb00`] Modify translation for error branch (#11731) (by Hanqing Zhao)
- [`62b9e5a`] feat(knowledge_retrieval_node): Suppress exceptions thrown by DatasetRetrieval (#11728) (by -LAN-)
- [`a399502`] Dark Mode: Workflow darkmode style (#11695) (by NFish)
- [`92a840f`] feat(tool_node): Suppress exceptions thrown by the Tool (#11724) (by -LAN-)
- [`74fdc16`] feat: enhance gemini models (#11497) (by 非法操作)
- [`56cfdce`] chore: update docker env close #11703 (#11706) (by yihong)
- [`efa8eb3`] fix: memory leak by pypdfium2 close(maybe) #11510 (#11700) (by yihong)
- [`7f095bd`] fix: image icon can not display (#11701) (by crazywoola)
- [`e20161b`] make login lockout duration configurable (#11699) (by Kazuhisa Wada)
- [`fc8fdba`] feat: add gitee ai vl models (#11697) (by 方程)
- [`7fde638`] fix: fix proxy for docker (#11681) (by longfengpili)
- [`be93c19`] chore: remove duplicate folder with case sensitivity issue (#11687) (by 非法操作)

