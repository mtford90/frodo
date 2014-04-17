__author__ = 'mtford'

Reporter_TimestampKey = 'timestamp'

Reporter_Events_BeginAction = 'begin-action'
Reporter_Events_EndAction = 'end-action'
Reporter_Events_BeginOCUnit = 'begin-ocunit'
Reporter_Events_EndOCUnit = 'end-ocunit'
Reporter_Events_BeginTestSuite = 'begin-test-suite'
Reporter_Events_EndTestSuite = 'end-test-suite'
Reporter_Events_BeginTest = 'begin-test'
Reporter_Events_EndTest = 'end-test'
Reporter_Events_TestOuput = 'test-output'
Reporter_Events_BeginXcodebuild = 'begin-xcodebuild'
Reporter_Events_EndXcodebuild = 'end-xcodebuild'
Reporter_Events_BeginBuildCommand = 'begin-build-command'
Reporter_Events_EndBuildCommand = 'end-build-command'
Reporter_Events_BeginBuildTarget = 'begin-build-target'
Reporter_Events_EndBuildTarget = 'end-build-target'
Reporter_Events_BeginStatus = 'begin-status'
Reporter_Events_EndStatus = 'end-status'
Reporter_Events_AnalyzerResult = 'analyzer-result'
Reporter_Events_OutputBeforeTestBundleStarts = 'output-before-test-bundle-starts'

Reporter_BeginAction_NameKey = 'name'
Reporter_BeginAction_WorkspaceKey = 'workspace'
Reporter_BeginAction_ProjectKey = 'project'
Reporter_BeginAction_SchemeKey = 'scheme'

Reporter_EndAction_NameKey = 'name'
Reporter_EndAction_WorkspaceKey = 'workspace'
Reporter_EndAction_ProjectKey = 'project'
Reporter_EndAction_SchemeKey = 'scheme'
Reporter_EndAction_SucceededKey = 'succeeded'
Reporter_EndAction_DurationKey = 'duration'

Reporter_BeginOCUnit_BundleNameKey = 'bundleName'
Reporter_BeginOCUnit_SDKNameKey = 'sdkName'
Reporter_BeginOCUnit_TestTypeKey = 'testType'
Reporter_BeginOCUnit_TargetNameKey = 'targetName'

Reporter_EndOCUnit_BundleNameKey = 'bundleName'
Reporter_EndOCUnit_SDKNameKey = 'sdkName'
Reporter_EndOCUnit_TestTypeKey = 'testType'
Reporter_EndOCUnit_SucceededKey = 'succeeded'
Reporter_EndOCUnit_MessageKey = 'message'

Reporter_TestSuite_TopLevelSuiteName = 'Toplevel Test Suite'

Reporter_BeginTestSuite_SuiteKey = 'suite'

Reporter_EndTestSuite_SuiteKey = 'suite'
Reporter_EndTestSuite_TestCaseCountKey = 'testCaseCount'
Reporter_EndTestSuite_TotalFailureCountKey = 'totalFailureCount'
Reporter_EndTestSuite_UnexpectedExceptionCountKey = 'unexpectedExceptionCount'
Reporter_EndTestSuite_TestDurationKey = 'testDuration'
Reporter_EndTestSuite_TotalDurationKey = 'totalDuration'

Reporter_BeginTest_TestKey = 'test'
Reporter_BeginTest_ClassNameKey = 'className'
Reporter_BeginTest_MethodNameKey = 'methodName'

Reporter_EndTest_TestKey = 'test'
Reporter_EndTest_ClassNameKey = 'className'
Reporter_EndTest_MethodNameKey = 'methodName'
Reporter_EndTest_SucceededKey = 'succeeded'
Reporter_EndTest_ResultKey = 'result'
Reporter_EndTest_TotalDurationKey = 'totalDuration'
Reporter_EndTest_OutputKey = 'output'
Reporter_EndTest_ExceptionsKey = 'exceptions'
Reporter_EndTest_Exception_FilePathInProjectKey = 'filePathInProject'
Reporter_EndTest_Exception_LineNumberKey = 'lineNumber'
Reporter_EndTest_Exception_ReasonKey = 'reason'

Reporter_TestOutput_OutputKey = 'output'

Reporter_BeginBuildCommand_TitleKey = 'title'
Reporter_BeginBuildCommand_CommandKey = 'command'

Reporter_EndBuildCommand_TitleKey = 'title'
Reporter_EndBuildCommand_SucceededKey = 'succeeded'
Reporter_EndBuildCommand_EmittedOutputTextKey = 'emittedOutputText'
Reporter_EndBuildCommand_DurationKey = 'duration'
Reporter_EndBuildCommand_ResultCode = 'resultCode'
Reporter_EndBuildCommand_TotalNumberOfWarnings = 'totalNumberOfWarnings'
Reporter_EndBuildCommand_TotalNumberOfErrors = 'totalNumberOfErrors'

Reporter_BeginBuildTarget_ProjectKey = 'project'
Reporter_BeginBuildTarget_TargetKey = 'target'
Reporter_BeginBuildTarget_ConfigurationKey = 'configuration'

Reporter_EndBuildTarget_ProjectKey = 'project'
Reporter_EndBuildTarget_TargetKey = 'target'
Reporter_EndBuildTarget_ConfigurationKey = 'configuration'

Reporter_BeginXcodebuild_CommandKey = 'command'
Reporter_BeginXcodebuild_TitleKey = 'title'

Reporter_EndXcodebuild_CommandKey = 'command'
Reporter_EndXcodebuild_TitleKey = 'title'
Reporter_EndXcodebuild_SucceededKey = 'succeeded'
Reporter_EndXcodebuild_ErrorMessageKey = 'errorMessage'
Reporter_EndXcodebuild_ErrorCodeKey = 'errorCode'

Reporter_BeginStatus_MessageKey = 'message'
Reporter_BeginStatus_LevelKey = 'level'

Reporter_EndStatus_MessageKey = 'message'
Reporter_EndStatus_LevelKey = 'level'

Reporter_AnalyzerResult_ProjectKey = 'project'
Reporter_AnalyzerResult_TargetKey = 'target'
Reporter_AnalyzerResult_FileKey = 'file'
Reporter_AnalyzerResult_LineKey = 'line'
Reporter_AnalyzerResult_ColumnKey = 'col'
Reporter_AnalyzerResult_DescriptionKey = 'description'
Reporter_AnalyzerResult_ContextKey = 'context'
Reporter_AnalyzerResult_CategoryKey = 'category'
Reporter_AnalyzerResult_TypeKey = 'type'

Reporter_OutputBeforeTestBundleStarts_OutputKey = 'output'