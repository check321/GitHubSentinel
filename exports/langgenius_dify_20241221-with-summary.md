# langgenius/dify-2024-12-21 更新摘要

# 更新摘要
本次更新主要集中在修复错误和优化代码，以提高系统的稳定性和性能。

## 主要更新
- 增强类型提示及改进音频消息处理功能。
- 重构对话分页，采用SQLAlchemy会话管理。

## 重要修复
- 修复“dict_keys”对象不可下标引用的错误 (#11957)。
- 将多个异常类的基类更改为ValueError，以统一错误处理 (#11950, #11951, #11934)。

## 新增功能
- 在代码节点中添加更多检查功能 (#11949)。

## 其他说明
- 本次更新涉及多项错误处理的增强，确保系统在处理用户请求时更加稳定和友好。

---

# 详细内容


## langgenius/dify

### No releases found

### Recent Commits
- [`26c10b9`] fix: 'dict_keys' object is not subscriptable error (#11957) (by yihong)
- [`750662e`] fix(workflow): update updated_at default to use UTC timezone (#11960) (by -LAN-)
- [`6b49889`] fix: messagefeedbackapi support content (#11716) (by liuhaoran)
- [`03ddee3`] fix(variable_assigner): change VariableOperatorNodeError to inherit from ValueError (#11951) (by -LAN-)
- [`10caab1`] fix: change CredentialsValidateFailedError to inherit from ValueError (#11950) (by -LAN-)
- [`c6a72de`] fix(ops_trace_manager): handle None workflow_run in workflow_trace method and raise ValueError (#11953) (by -LAN-)
- [`21a31d7`] fix(base_node): change BaseNodeError exception type from Exception to ValueError (#11952) (by -LAN-)
- [`2c4df10`] fix: raise http request node error on httpx.request error (#11954) (by -LAN-)
- [`5db8add`] fix(core/errors): change base class of custom exceptions to ValueError (#11955) (by -LAN-)
- [`dd0e81d`] fix: enhance type hints and improve audio message handling in TTS pub… (#11947) (by -LAN-)
- [`90f093e`] fix(json_in_md_parser): improve error messages for JSON parsing failures (#11948) (by -LAN-)
- [`a056a9d`] feat(code_node): add more check (#11949) (by -LAN-)
- [`2ad2a40`] fix(app_dsl_service): handle missing app mode with a ValueError (#11945) (by -LAN-)
- [`3d07a94`] fix: refactor conversation pagination to use SQLAlchemy session manag… (#11956) (by -LAN-)
- [`366857c`] fix: gemini system prompt with variable raise error (#11946) (by 非法操作)
- [`9578246`] fix: The default updated_at when a workflow is created (#11709) (by jiangbo721)
- [`9ee9e9c`] fix: self.method should method in api_tool.py (#11926) (by yihong)
- [`e22cc28`] fix:log error(#11942) (#11943) (by 呆萌闷油瓶)
- [`a227af3`] fix(code_node): update type hints for string and number checks in Cod… (#11936) (by -LAN-)
- [`599d410`] fix: validate reranking model attributes before processing (#11930) (by -LAN-)
- [`5e37ab6`] fix: validate response type in transform_response method (#11931) (by -LAN-)
- [`0b06235`] fix: add RemoteFileUploadError for better error handling in remote fi… (#11933) (by -LAN-)
- [`b8d42cd`] fix: change MaxRetriesExceededError to inherit from ValueError (#11934) (by -LAN-)
- [`455791b`] fix(model_runtime): make invoke as ValueError (#11929) (by -LAN-)
- [`90323cd`] fix(tool_file_manager): raise ValueError when get timeout (#11928) (by -LAN-)
- [`c07d9e9`] fix(nodes): handle errors in question_classifier and parameter_extractor (#11927) (by -LAN-)
- [`810adb8`] fix: change OutputParserError to inherit from ValueError (#11935) (by -LAN-)
- [`606aadb`] refactor: update builtin tool provider methods to use session management (#11938) (by -LAN-)
- [`8f73670`] fix(file_factory): validate upload_file_id before querying UploadFile (#11937) (by -LAN-)
- [`8c559d6`] fix(retrieval_service): avoid to use exception (#11925) (by -LAN-)

