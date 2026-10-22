# Migration helper: Stormpy 1.* to Stormpy 2.0

This table lists all changes from Stormpy 1.* to Stormpy 2.0.

## Renamed symbols

| v1 name(s) | v2 name / expression | Migration note |
| --- | --- | --- |
| `stormpy.ActionMaskDouble` | `stormpy.developer.ActionMask[float]` | Becomes a template. |
| `stormpy.AddIterator_Sylvan_Double`<br>`stormpy.storage.AddIterator_Sylvan_Double` | `stormpy.developer.storage.AddIterator[stormpy.models.DdType.Sylvan, float]` | Explicit decision-diagram backend and value type parameters. |
| `stormpy.AddUncertaintyDouble` | `stormpy.developer.AddUncertainty[float]` | Becomes a template. |
| `stormpy.AddUncertaintyExact` | `stormpy.developer.AddUncertainty[stormpy.Rational]` | Becomes a template. |
| `stormpy.Add_Sylvan_Double`<br>`stormpy.storage.Add_Sylvan_Double` | `stormpy.developer.storage.Add[stormpy.models.DdType.Sylvan, float]` | Explicit decision-diagram backend and value type parameters. |
| `stormpy.ArrayType`<br>`stormpy.storage.ArrayType` | `stormpy.io.ArrayType` |  |
| `stormpy.AtomicExpressionFormula`<br>`stormpy.logic.AtomicExpressionFormula` | `stormpy.logic.AtomicExpressionFormula` |  |
| `stormpy.AtomicLabelFormula`<br>`stormpy.logic.AtomicLabelFormula` | `stormpy.logic.AtomicLabelFormula` |  |
| `stormpy.BasicType`<br>`stormpy.storage.BasicType` | `stormpy.io.BasicType` |  |
| `stormpy.Bdd_Sylvan`<br>`stormpy.storage.Bdd_Sylvan` | `stormpy.developer.storage.Bdd[stormpy.models.DdType.Sylvan]` | Explicit decision-diagram backend and value type parameters. |
| `stormpy.BinaryBooleanOperatorType`<br>`stormpy.logic.BinaryBooleanOperatorType` | `stormpy.logic.BinaryBooleanOperatorType` |  |
| `stormpy.BinaryPathFormula`<br>`stormpy.logic.BinaryPathFormula` | `stormpy.logic.BinaryPathFormula` |  |
| `stormpy.BinaryStateFormula`<br>`stormpy.logic.BinaryStateFormula` | `stormpy.logic.BinaryStateFormula` |  |
| `stormpy.BisimulationOptionsDd` | `stormpy.developer.DdBisimulationOptions` | Renamed raw DD options; public BisimulationOptions is a different type. |
| `stormpy.BisimulationType` | `stormpy.transformations.BisimulationType` |  |
| `stormpy.BitVector`<br>`stormpy.storage.BitVector` | `stormpy.datastructures.BitVector` |  |
| `stormpy.BooleanBinaryStateFormula`<br>`stormpy.logic.BooleanBinaryStateFormula` | `stormpy.logic.BinaryBooleanStateFormula` | Renamed. |
| `stormpy.BooleanLiteralFormula`<br>`stormpy.logic.BooleanLiteralFormula` | `stormpy.logic.BooleanLiteralFormula` |  |
| `stormpy.BoundedType`<br>`stormpy.storage.BoundedType` | `stormpy.io.BoundedType` |  |
| `stormpy.BoundedUntilFormula`<br>`stormpy.logic.BoundedUntilFormula` | `stormpy.logic.BoundedUntilFormula` |  |
| `stormpy.BuilderOptions` | `stormpy.BuilderOptions` |  |
| `stormpy.CheckTask` | `stormpy.developer.CheckTask[float]` | Becomes a template. |
| `stormpy.ChoiceLabeling`<br>`stormpy.storage.ChoiceLabeling` | `stormpy.models.ChoiceLabeling` |  |
| `stormpy.ChoiceOrigins`<br>`stormpy.storage.ChoiceOrigins` | `stormpy.models.ChoiceOrigins` |  |
| `stormpy.ClockType`<br>`stormpy.storage.ClockType` | `stormpy.io.ClockType` |  |
| `stormpy.ComparisonType`<br>`stormpy.logic.ComparisonType` | `stormpy.logic.ComparisonType` |  |
| `stormpy.CompressionMode`<br>`stormpy.storage.CompressionMode` | `stormpy.io.CompressionMode` |  |
| `stormpy.ConditionalAlgorithmSetting` | `stormpy.environments.ConditionalAlgorithmSetting` |  |
| `stormpy.ConditionalFormula`<br>`stormpy.logic.ConditionalFormula` | `stormpy.logic.ConditionalFormula` |  |
| `stormpy.ConditionalModelCheckerEnvironment` | `stormpy.environments.ConditionalModelCheckerEnvironment` |  |
| `stormpy.ConstraintCollector` | `stormpy.pars.ConstraintCollector` |  |
| `stormpy.ContinuousType`<br>`stormpy.storage.ContinuousType` | `stormpy.io.ContinuousType` |  |
| `stormpy.CuddDdManagerEnvironment` | `stormpy.environments.CuddDdManagerEnvironment` |  |
| `stormpy.CuddReorderingTechnique` | `stormpy.environments.CuddReorderingTechnique` |  |
| `stormpy.CumulativeRewardFormula`<br>`stormpy.logic.CumulativeRewardFormula` | `stormpy.logic.CumulativeRewardFormula` |  |
| `stormpy.DdEnvironment` | `stormpy.environments.DdEnvironment` |  |
| `stormpy.DdManager_Sylvan`<br>`stormpy.storage.DdManager_Sylvan` | `stormpy.developer.storage.DdManager[stormpy.models.DdType.Sylvan]` | Explicit decision-diagram backend and value type parameters. |
| `stormpy.DdMetaVariableType`<br>`stormpy.storage.DdMetaVariableType` | `stormpy.developer.storage.DdMetaVariableType` |  |
| `stormpy.DdMetaVariable_Sylvan`<br>`stormpy.storage.DdMetaVariable_Sylvan` | `stormpy.developer.storage.DdMetaVariable[stormpy.models.DdType.Sylvan]` | Explicit decision-diagram backend and value type parameters. |
| `stormpy.Dd_Sylvan`<br>`stormpy.storage.Dd_Sylvan` | `stormpy.developer.storage.Dd[stormpy.models.DdType.Sylvan]` | Explicit decision-diagram backend and value type parameters. |
| `stormpy.DiceStringVisitor`<br>`stormpy.storage.DiceStringVisitor` | `stormpy.developer.storage.DiceStringVisitor` |  |
| `stormpy.DirectEncodingExporterOptions` | `stormpy.io.DirectEncodingExporterOptions` |  |
| `stormpy.DirectEncodingParserOptions` | `stormpy.io.DirectEncodingParserOptions` |  |
| `stormpy.Distribution`<br>`stormpy.storage.Distribution` | `stormpy.datastructures.Distribution[float]` | Becomes a template. |
| `stormpy.DistributionExact`<br>`stormpy.storage.DistributionExact` | `stormpy.datastructures.Distribution[stormpy.Rational]` | Becomes a template. |
| `stormpy.DistributionInterval`<br>`stormpy.storage.DistributionInterval` | `stormpy.datastructures.Distribution[stormpy.Interval]` | Becomes a template. |
| `stormpy.DistributionRationalInterval`<br>`stormpy.storage.DistributionRationalInterval` | `stormpy.datastructures.Distribution[stormpy.RationalInterval]` | Becomes a template. |
| `stormpy.EliminationLabelBehavior` | `stormpy.transformations.EliminationLabelBehavior` |  |
| `stormpy.EndComponentEliminatorReturnTypeDouble` | `stormpy.developer.EndComponentEliminatorReturnType[float]` | Becomes a template. |
| `stormpy.EndComponentEliminatorReturnTypeExact` | `stormpy.developer.EndComponentEliminatorReturnType[stormpy.Rational]` | Becomes a template. |
| `stormpy.EndComponentEliminatorReturnTypeInterval` | `stormpy.developer.EndComponentEliminatorReturnType[stormpy.Interval]` | Becomes a template. |
| `stormpy.EndComponentEliminatorReturnTypeRatFunc` | `stormpy.developer.EndComponentEliminatorReturnType[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.EndComponentEliminatorReturnTypeRationalInterval` | `stormpy.developer.EndComponentEliminatorReturnType[stormpy.RationalInterval]` | Becomes a template. |
| `stormpy.Environment` | `stormpy.Environment` |  |
| `stormpy.EquationSolverType` | `stormpy.environments.EquationSolverType` |  |
| `stormpy.EventuallyFormula`<br>`stormpy.logic.EventuallyFormula` | `stormpy.logic.EventuallyFormula` |  |
| `stormpy.ExactCheckTask` | `stormpy.developer.CheckTask[stormpy.Rational]` | Becomes a template. |
| `stormpy.ExactParetoCurveCheckResult` | `stormpy.results.ParetoCurveCheckResult[stormpy.Rational]` | Becomes a template. |
| `stormpy.ExactSparseMatrix`<br>`stormpy.storage.ExactSparseMatrix` | `stormpy.datastructures.SparseMatrix[stormpy.Rational]` | Becomes a template. |
| `stormpy.ExactSparseMatrixBuilder`<br>`stormpy.storage.ExactSparseMatrixBuilder` | `stormpy.datastructures.SparseMatrixBuilder[stormpy.Rational]` | Becomes a template. |
| `stormpy.ExactSparseMatrixEntry`<br>`stormpy.storage.ExactSparseMatrixEntry` | `stormpy.datastructures.SparseMatrixEntry[stormpy.Rational]` | Becomes a template. |
| `stormpy.ExactSparseMatrixRows`<br>`stormpy.storage.ExactSparseMatrixRows` | `stormpy.datastructures.SparseMatrixRows[stormpy.Rational]` | Becomes a template. |
| `stormpy.ExplicitExactIntervalModelBuilderOptions` | `stormpy.developer.ExplicitModelBuilderOptions[stormpy.RationalInterval]` | Renamed generic family. |
| `stormpy.ExplicitExactModelBuilderOptions` | `stormpy.developer.ExplicitModelBuilderOptions[stormpy.Rational]` | Becomes a template. |
| `stormpy.ExplicitExactParetoCurveCheckResult` | `stormpy.results.ExplicitParetoCurveCheckResult[stormpy.Rational]` | Becomes a template. |
| `stormpy.ExplicitExactQualitativeCheckResult` | `stormpy.results.ExplicitQualitativeCheckResult[stormpy.Rational]` | Becomes a template. |
| `stormpy.ExplicitExactQuantitativeCheckResult` | `stormpy.results.ExplicitQuantitativeCheckResult[stormpy.Rational]` | Becomes a template. |
| `stormpy.ExplicitIntervalModelBuilderOptions` | `stormpy.developer.ExplicitModelBuilderOptions[stormpy.Interval]` | Becomes a template. |
| `stormpy.ExplicitModelBuilder` | `stormpy.developer.ExplicitModelBuilder[float]` | Becomes a template. |
| `stormpy.ExplicitModelBuilderOptions` | `stormpy.developer.ExplicitModelBuilderOptions[float]` | Becomes a template. |
| `stormpy.ExplicitModelCheckerHintDouble` | `stormpy.ExplicitModelCheckerHint[float]` | Becomes a template. |
| `stormpy.ExplicitModelParserOptions` | `stormpy.io.ExplicitModelParserOptions` |  |
| `stormpy.ExplicitParametricModelBuilder` | `stormpy.developer.ExplicitModelBuilder[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.ExplicitParametricModelBuilderOptions` | `stormpy.developer.ExplicitModelBuilderOptions[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.ExplicitParametricQualitativeCheckResult` | `stormpy.results.ExplicitQualitativeCheckResult[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.ExplicitParametricQuantitativeCheckResult` | `stormpy.results.ExplicitQuantitativeCheckResult[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.ExplicitParetoCurveCheckResult` | `stormpy.results.ExplicitParetoCurveCheckResult[float]` | Becomes a template. |
| `stormpy.ExplicitQualitativeCheckResult` | `stormpy.results.ExplicitQualitativeCheckResult[float]` | Becomes a template. |
| `stormpy.ExplicitQuantitativeCheckResult` | `stormpy.results.ExplicitQuantitativeCheckResult[float]` | Becomes a template. |
| `stormpy.ExplicitStateLookup` | `stormpy.developer.ExplicitStateLookup` |  |
| `stormpy.ExplorationOrder` | `stormpy.developer.ExplorationOrder` |  |
| `stormpy.Expression`<br>`stormpy.storage.Expression` | `stormpy.expressions.Expression` |  |
| `stormpy.ExpressionManager`<br>`stormpy.storage.ExpressionManager` | `stormpy.expressions.ExpressionManager` |  |
| `stormpy.ExpressionParser`<br>`stormpy.storage.ExpressionParser` | `stormpy.expressions.ExpressionParser` |  |
| `stormpy.ExpressionType`<br>`stormpy.storage.ExpressionType` | `stormpy.expressions.ExpressionType` |  |
| `stormpy.FactorizedPolynomial` | `stormpy.Polynomial` | Renamed numeric type; v2 Polynomial is factorized. |
| `stormpy.FactorizedRationalFunction` | `stormpy.RationalFunction` | Renamed numeric type; selects the Storm rational-function type. |
| `stormpy.FlatSet` | `stormpy.developer.FlatSet` |  |
| `stormpy.Formula`<br>`stormpy.logic.Formula` | `stormpy.logic.Formula` |  |
| `stormpy.GameFormula`<br>`stormpy.logic.GameFormula` | `stormpy.logic.GameFormula` |  |
| `stormpy.GloballyFormula`<br>`stormpy.logic.GloballyFormula` | `stormpy.logic.GloballyFormula` |  |
| `stormpy.HybridExactQuantitativeCheckResult` | `stormpy.results.HybridQuantitativeCheckResult[stormpy.models.DdType.Sylvan, stormpy.Rational]` | Becomes a template. |
| `stormpy.HybridParametricQuantitativeCheckResult` | `stormpy.results.HybridQuantitativeCheckResult[stormpy.models.DdType.Sylvan, stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.HybridQuantitativeCheckResult` | `stormpy.results.HybridQuantitativeCheckResult[stormpy.models.DdType.Sylvan, float]` | Becomes a template. |
| `stormpy.InstantaneousRewardFormula`<br>`stormpy.logic.InstantaneousRewardFormula` | `stormpy.logic.InstantaneousRewardFormula` |  |
| `stormpy.IntervalSparseMatrix`<br>`stormpy.storage.IntervalSparseMatrix` | `stormpy.datastructures.SparseMatrix[stormpy.Interval]` | Becomes a template. |
| `stormpy.IntervalSparseMatrixBuilder`<br>`stormpy.storage.IntervalSparseMatrixBuilder` | `stormpy.datastructures.SparseMatrixBuilder[stormpy.Interval]` | Becomes a template. |
| `stormpy.IntervalSparseMatrixEntry`<br>`stormpy.storage.IntervalSparseMatrixEntry` | `stormpy.datastructures.SparseMatrixEntry[stormpy.Interval]` | Becomes a template. |
| `stormpy.IntervalSparseMatrixRows`<br>`stormpy.storage.IntervalSparseMatrixRows` | `stormpy.datastructures.SparseMatrixRows[stormpy.Interval]` | Becomes a template. |
| `stormpy.ItemLabeling`<br>`stormpy.storage.ItemLabeling` | `stormpy.developer.storage.ItemLabeling` |  |
| `stormpy.JaniAssignment`<br>`stormpy.storage.JaniAssignment` | `stormpy.io.JaniAssignment` |  |
| `stormpy.JaniAutomaton`<br>`stormpy.storage.JaniAutomaton` | `stormpy.io.JaniAutomaton` |  |
| `stormpy.JaniChoiceOrigins`<br>`stormpy.storage.JaniChoiceOrigins` | `stormpy.models.JaniChoiceOrigins` |  |
| `stormpy.JaniConstant`<br>`stormpy.storage.JaniConstant` | `stormpy.io.JaniConstant` |  |
| `stormpy.JaniEdge`<br>`stormpy.storage.JaniEdge` | `stormpy.io.JaniEdge` |  |
| `stormpy.JaniEdgeDestination`<br>`stormpy.storage.JaniEdgeDestination` | `stormpy.io.JaniEdgeDestination` |  |
| `stormpy.JaniInformationObject`<br>`stormpy.storage.JaniInformationObject` | `stormpy.developer.storage.JaniInformationObject` |  |
| `stormpy.JaniLocation`<br>`stormpy.storage.JaniLocation` | `stormpy.io.JaniLocation` |  |
| `stormpy.JaniLocationExpander`<br>`stormpy.storage.JaniLocationExpander` | `stormpy.developer.storage.JaniLocationExpander` |  |
| `stormpy.JaniModel`<br>`stormpy.storage.JaniModel` | `stormpy.io.JaniModel` |  |
| `stormpy.JaniModelType` | `stormpy.io.JaniModelType` |  |
| `stormpy.JaniOrderedAssignments`<br>`stormpy.storage.JaniOrderedAssignments` | `stormpy.io.JaniOrderedAssignments` |  |
| `stormpy.JaniScopeChanger`<br>`stormpy.storage.JaniScopeChanger` | `stormpy.developer.storage.JaniScopeChanger` |  |
| `stormpy.JaniTemplateEdge`<br>`stormpy.storage.JaniTemplateEdge` | `stormpy.io.JaniTemplateEdge` |  |
| `stormpy.JaniTemplateEdgeDestination`<br>`stormpy.storage.JaniTemplateEdgeDestination` | `stormpy.io.JaniTemplateEdgeDestination` |  |
| `stormpy.JaniType`<br>`stormpy.storage.JaniType` | `stormpy.io.JaniType` |  |
| `stormpy.JaniVariable`<br>`stormpy.storage.JaniVariable` | `stormpy.io.JaniVariable` |  |
| `stormpy.JaniVariableSet`<br>`stormpy.storage.JaniVariableSet` | `stormpy.io.JaniVariableSet` |  |
| `stormpy.LongRunAvarageOperator`<br>`stormpy.logic.LongRunAvarageOperator` | `stormpy.logic.LongRunAverageOperatorFormula` | Corrected spelling and added Formula suffix. |
| `stormpy.LongRunAverageRewardFormula`<br>`stormpy.logic.LongRunAverageRewardFormula` | `stormpy.logic.LongRunAverageRewardFormula` |  |
| `stormpy.MaximalEndComponent`<br>`stormpy.storage.MaximalEndComponent` | `stormpy.analysis.MaximalEndComponent` |  |
| `stormpy.MaximalEndComponentDecomposition_double`<br>`stormpy.storage.MaximalEndComponentDecomposition_double` | `stormpy.analysis.MaximalEndComponentDecomposition[float]` | Becomes a template. |
| `stormpy.MaximalEndComponentDecomposition_exact`<br>`stormpy.storage.MaximalEndComponentDecomposition_exact` | `stormpy.analysis.MaximalEndComponentDecomposition[stormpy.Rational]` | Becomes a template. |
| `stormpy.MaximalEndComponentDecomposition_interval`<br>`stormpy.storage.MaximalEndComponentDecomposition_interval` | `stormpy.analysis.MaximalEndComponentDecomposition[stormpy.Interval]` | Becomes a template. |
| `stormpy.MaximalEndComponentDecomposition_ratfunc`<br>`stormpy.storage.MaximalEndComponentDecomposition_ratfunc` | `stormpy.analysis.MaximalEndComponentDecomposition[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.MaximalEndComponentDecomposition_ratinterval`<br>`stormpy.storage.MaximalEndComponentDecomposition_ratinterval` | `stormpy.analysis.MaximalEndComponentDecomposition[stormpy.RationalInterval]` | Becomes a template. |
| `stormpy.MemoryStructure`<br>`stormpy.storage.MemoryStructure` | `stormpy.models.MemoryStructure` |  |
| `stormpy.MemoryStructureBuilder`<br>`stormpy.storage.MemoryStructureBuilder` | `stormpy.models.MemoryStructureBuilder[float]` | Becomes a template. |
| `stormpy.MemoryStructureBuilderExact`<br>`stormpy.storage.MemoryStructureBuilderExact` | `stormpy.models.MemoryStructureBuilder[stormpy.Rational]` | Becomes a template. |
| `stormpy.MemoryStructureBuilderInterval`<br>`stormpy.storage.MemoryStructureBuilderInterval` | `stormpy.models.MemoryStructureBuilder[stormpy.Interval]` | Becomes a template. |
| `stormpy.MemoryStructureBuilderParametric`<br>`stormpy.storage.MemoryStructureBuilderParametric` | `stormpy.models.MemoryStructureBuilder[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.MemoryStructureProduct`<br>`stormpy.storage.MemoryStructureProduct` | `stormpy.developer.storage.MemoryStructureProduct[float]` | Becomes a template. |
| `stormpy.MemoryStructureProductExact`<br>`stormpy.storage.MemoryStructureProductExact` | `stormpy.developer.storage.MemoryStructureProduct[stormpy.Rational]` | Becomes a template. |
| `stormpy.MemoryStructureProductInterval`<br>`stormpy.storage.MemoryStructureProductInterval` | `stormpy.developer.storage.MemoryStructureProduct[stormpy.Interval]` | Becomes a template. |
| `stormpy.MemoryStructureProductParametric`<br>`stormpy.storage.MemoryStructureProductParametric` | `stormpy.developer.storage.MemoryStructureProduct[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.MinMaxMethod` | `stormpy.environments.MinMaxMethod` |  |
| `stormpy.MinMaxSolverEnvironment` | `stormpy.environments.MinMaxSolverEnvironment` |  |
| `stormpy.ModelCheckerEnvironment` | `stormpy.environments.ModelCheckerEnvironment` |  |
| `stormpy.ModelCheckerHint` | `stormpy.ModelCheckerHint` |  |
| `stormpy.ModelType`<br>`stormpy.storage.ModelType` | `stormpy.models.ModelType` |  |
| `stormpy.MultiObjectiveEncodingType` | `stormpy.environments.MultiObjectiveEncodingType` |  |
| `stormpy.MultiObjectiveFormula`<br>`stormpy.logic.MultiObjectiveFormula` | `stormpy.logic.MultiObjectiveFormula` |  |
| `stormpy.MultiObjectiveMethod` | `stormpy.environments.MultiObjectiveMethod` |  |
| `stormpy.MultiObjectiveModelCheckerEnvironment` | `stormpy.environments.MultiObjectiveModelCheckerEnvironment` |  |
| `stormpy.MultiObjectivePrecisionType` | `stormpy.environments.MultiObjectivePrecisionType` |  |
| `stormpy.NativeLinearEquationSolverMethod` | `stormpy.environments.NativeLinearEquationSolverMethod` |  |
| `stormpy.NativeSolverEnvironment` | `stormpy.environments.NativeSolverEnvironment` |  |
| `stormpy.OperatorFormula`<br>`stormpy.logic.OperatorFormula` | `stormpy.logic.OperatorFormula` |  |
| `stormpy.OperatorType`<br>`stormpy.storage.OperatorType` | `stormpy.expressions.OperatorType` |  |
| `stormpy.OptimizationDirection` | `stormpy.logic.OptimizationDirection` |  |
| `stormpy.OverlappingGuardAnalyser`<br>`stormpy.storage.OverlappingGuardAnalyser` | `stormpy.developer.storage.OverlappingGuardAnalyser` |  |
| `stormpy.ParametricCheckTask` | `stormpy.developer.CheckTask[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.ParametricSparseMatrix`<br>`stormpy.storage.ParametricSparseMatrix` | `stormpy.datastructures.SparseMatrix[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.ParametricSparseMatrixBuilder`<br>`stormpy.storage.ParametricSparseMatrixBuilder` | `stormpy.datastructures.SparseMatrixBuilder[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.ParametricSparseMatrixEntry`<br>`stormpy.storage.ParametricSparseMatrixEntry` | `stormpy.datastructures.SparseMatrixEntry[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.ParametricSparseMatrixRows`<br>`stormpy.storage.ParametricSparseMatrixRows` | `stormpy.datastructures.SparseMatrixRows[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.ParetoCurveCheckResult` | `stormpy.results.ParetoCurveCheckResult[float]` | Becomes a template. |
| `stormpy.PathFormula`<br>`stormpy.logic.PathFormula` | `stormpy.logic.PathFormula` |  |
| `stormpy.Polynomial` | `stormpy.RawPolynomial` | Renamed numeric type; v1 Polynomial was non-factorized. |
| `stormpy.PolytopeDouble`<br>`stormpy.storage.PolytopeDouble` | `stormpy.developer.storage.Polytope[float]` | Becomes a template. |
| `stormpy.PolytopeExact`<br>`stormpy.storage.PolytopeExact` | `stormpy.developer.storage.Polytope[stormpy.Rational]` | Becomes a template. |
| `stormpy.PrismAssignment`<br>`stormpy.storage.PrismAssignment` | `stormpy.io.PrismAssignment` |  |
| `stormpy.PrismBooleanVariable`<br>`stormpy.storage.PrismBooleanVariable` | `stormpy.io.PrismBooleanVariable` |  |
| `stormpy.PrismChoiceOrigins`<br>`stormpy.storage.PrismChoiceOrigins` | `stormpy.models.PrismChoiceOrigins` |  |
| `stormpy.PrismCommand`<br>`stormpy.storage.PrismCommand` | `stormpy.io.PrismCommand` |  |
| `stormpy.PrismConstant`<br>`stormpy.storage.PrismConstant` | `stormpy.io.PrismConstant` |  |
| `stormpy.PrismIntegerVariable`<br>`stormpy.storage.PrismIntegerVariable` | `stormpy.io.PrismIntegerVariable` |  |
| `stormpy.PrismLabel`<br>`stormpy.storage.PrismLabel` | `stormpy.io.PrismLabel` |  |
| `stormpy.PrismModelType`<br>`stormpy.storage.PrismModelType` | `stormpy.io.PrismModelType` |  |
| `stormpy.PrismModule`<br>`stormpy.storage.PrismModule` | `stormpy.io.PrismModule` |  |
| `stormpy.PrismProgram`<br>`stormpy.storage.PrismProgram` | `stormpy.io.PrismProgram` |  |
| `stormpy.PrismRewardModel`<br>`stormpy.storage.PrismRewardModel` | `stormpy.io.PrismRewardModel` |  |
| `stormpy.PrismUpdate`<br>`stormpy.storage.PrismUpdate` | `stormpy.io.PrismUpdate` |  |
| `stormpy.PrismVariable`<br>`stormpy.storage.PrismVariable` | `stormpy.io.PrismVariable` |  |
| `stormpy.ProbabilityOperator`<br>`stormpy.logic.ProbabilityOperator` | `stormpy.logic.ProbabilityOperatorFormula` | Added Formula suffix. |
| `stormpy.Property` | `stormpy.logic.Property` |  |
| `stormpy.QuotientFormat` | `stormpy.transformations.QuotientFormat` |  |
| `stormpy.Rational` | `stormpy.Rational` |  |
| `stormpy.RationalFunction` | `stormpy.numbers.developer.cln.RationalFunction`<br>`stormpy.numbers.developer.gmp.RationalFunction` | Unfactorized rational function remains in the numeric backend; v2 stormpy.RationalFunction denotes the factorized type. |
| `stormpy.RationalIntervalSparseMatrix`<br>`stormpy.storage.RationalIntervalSparseMatrix` | `stormpy.datastructures.SparseMatrix[stormpy.RationalInterval]` | Becomes a template. |
| `stormpy.RationalIntervalSparseMatrixBuilder`<br>`stormpy.storage.RationalIntervalSparseMatrixBuilder` | `stormpy.datastructures.SparseMatrixBuilder[stormpy.RationalInterval]` | Becomes a template. |
| `stormpy.RationalIntervalSparseMatrixEntry`<br>`stormpy.storage.RationalIntervalSparseMatrixEntry` | `stormpy.datastructures.SparseMatrixEntry[stormpy.RationalInterval]` | Becomes a template. |
| `stormpy.RationalIntervalSparseMatrixRows`<br>`stormpy.storage.RationalIntervalSparseMatrixRows` | `stormpy.datastructures.SparseMatrixRows[stormpy.RationalInterval]` | Becomes a template. |
| `stormpy.RationalRF` | `stormpy.numbers.RationalFunctionCoefficient` | Renamed numeric type. |
| `stormpy.RewardOperator`<br>`stormpy.logic.RewardOperator` | `stormpy.logic.RewardOperatorFormula` | Added Formula suffix. |
| `stormpy.SMTCounterExampleGenerator` | `stormpy.developer.SMTMinimalLabelSetGenerator[float]` | Renamed generic family. |
| `stormpy.SMTCounterExampleGeneratorOptions` | `stormpy.developer.SMTMinimalLabelSetGeneratorOptions[float]` | Renamed generic family. |
| `stormpy.SMTCounterExampleGeneratorStats` | `stormpy.developer.SMTMinimalLabelSetGeneratorStats[float]` | Renamed generic family. |
| `stormpy.SMTCounterExampleInput` | `stormpy.developer.SMTMinimalLabelSetGeneratorCexInput[float]` | Renamed generic family. |
| `stormpy.Scheduler`<br>`stormpy.storage.Scheduler` | `stormpy.models.Scheduler[float]` | Becomes a template. |
| `stormpy.SchedulerChoice`<br>`stormpy.storage.SchedulerChoice` | `stormpy.models.SchedulerChoice[float]` | Becomes a template. |
| `stormpy.SchedulerChoiceExact`<br>`stormpy.storage.SchedulerChoiceExact` | `stormpy.models.SchedulerChoice[stormpy.Rational]` | Becomes a template. |
| `stormpy.SchedulerChoiceInterval`<br>`stormpy.storage.SchedulerChoiceInterval` | `stormpy.models.SchedulerChoice[stormpy.Interval]` | Becomes a template. |
| `stormpy.SchedulerChoiceParametric`<br>`stormpy.storage.SchedulerChoiceParametric` | `stormpy.models.SchedulerChoice[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.SchedulerChoiceRationalInterval`<br>`stormpy.storage.SchedulerChoiceRationalInterval` | `stormpy.models.SchedulerChoice[stormpy.RationalInterval]` | Becomes a template. |
| `stormpy.SchedulerClass` | `stormpy.developer.SchedulerClass` |  |
| `stormpy.SchedulerExact`<br>`stormpy.storage.SchedulerExact` | `stormpy.models.Scheduler[stormpy.Rational]` | Becomes a template. |
| `stormpy.SchedulerInterval`<br>`stormpy.storage.SchedulerInterval` | `stormpy.models.Scheduler[stormpy.Interval]` | Becomes a template. |
| `stormpy.SchedulerMemoryPattern` | `stormpy.developer.SchedulerMemoryPattern` |  |
| `stormpy.SchedulerParametric`<br>`stormpy.storage.SchedulerParametric` | `stormpy.models.Scheduler[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.SchedulerRationalInterval`<br>`stormpy.storage.SchedulerRationalInterval` | `stormpy.models.Scheduler[stormpy.RationalInterval]` | Becomes a template. |
| `stormpy.SimpleValuation`<br>`stormpy.storage.SimpleValuation` | `stormpy.models.SimpleValuation` |  |
| `stormpy.SolverEnvironment` | `stormpy.environments.SolverEnvironment` |  |
| `stormpy.SparseCtmc`<br>`stormpy.storage.SparseCtmc` | `stormpy.models.SparseCtmc[float]` | Becomes a template. |
| `stormpy.SparseDtmc`<br>`stormpy.storage.SparseDtmc` | `stormpy.models.SparseDtmc[float]` | Becomes a template. |
| `stormpy.SparseExactCtmc`<br>`stormpy.storage.SparseExactCtmc` | `stormpy.models.SparseCtmc[stormpy.Rational]` | Becomes a template. |
| `stormpy.SparseExactDtmc`<br>`stormpy.storage.SparseExactDtmc` | `stormpy.models.SparseDtmc[stormpy.Rational]` | Becomes a template. |
| `stormpy.SparseExactMA`<br>`stormpy.storage.SparseExactMA` | `stormpy.models.SparseMA[stormpy.Rational]` | Becomes a template. |
| `stormpy.SparseExactMdp`<br>`stormpy.storage.SparseExactMdp` | `stormpy.models.SparseMdp[stormpy.Rational]` | Becomes a template. |
| `stormpy.SparseExactModelAction`<br>`stormpy.storage.SparseExactModelAction` | `stormpy.models.SparseModelAction[stormpy.Rational]` | Becomes a template. |
| `stormpy.SparseExactModelActions`<br>`stormpy.storage.SparseExactModelActions` | `stormpy.models.SparseModelActions[stormpy.Rational]` | Becomes a template. |
| `stormpy.SparseExactModelComponents`<br>`stormpy.storage.SparseExactModelComponents` | `stormpy.models.SparseModelComponents[stormpy.Rational]` | Becomes a template. |
| `stormpy.SparseExactModelState`<br>`stormpy.storage.SparseExactModelState` | `stormpy.models.SparseModelState[stormpy.Rational]` | Becomes a template. |
| `stormpy.SparseExactModelStates`<br>`stormpy.storage.SparseExactModelStates` | `stormpy.models.SparseModelStates[stormpy.Rational]` | Becomes a template. |
| `stormpy.SparseExactPomdp`<br>`stormpy.storage.SparseExactPomdp` | `stormpy.models.SparsePomdp[stormpy.Rational]` | Becomes a template. |
| `stormpy.SparseExactRewardModel`<br>`stormpy.storage.SparseExactRewardModel` | `stormpy.models.SparseRewardModel[stormpy.Rational]` | Becomes a template. |
| `stormpy.SparseExactSmg`<br>`stormpy.storage.SparseExactSmg` | `stormpy.models.SparseSmg[stormpy.Rational]` | Becomes a template. |
| `stormpy.SparseIntervalCtmc`<br>`stormpy.storage.SparseIntervalCtmc` | `stormpy.models.SparseCtmc[stormpy.Interval]` | Becomes a template. |
| `stormpy.SparseIntervalDtmc`<br>`stormpy.storage.SparseIntervalDtmc` | `stormpy.models.SparseDtmc[stormpy.Interval]` | Becomes a template. |
| `stormpy.SparseIntervalMA`<br>`stormpy.storage.SparseIntervalMA` | `stormpy.models.SparseMA[stormpy.Interval]` | Becomes a template. |
| `stormpy.SparseIntervalMdp`<br>`stormpy.storage.SparseIntervalMdp` | `stormpy.models.SparseMdp[stormpy.Interval]` | Becomes a template. |
| `stormpy.SparseIntervalModelAction`<br>`stormpy.storage.SparseIntervalModelAction` | `stormpy.models.SparseModelAction[stormpy.Interval]` | Becomes a template. |
| `stormpy.SparseIntervalModelActions`<br>`stormpy.storage.SparseIntervalModelActions` | `stormpy.models.SparseModelActions[stormpy.Interval]` | Becomes a template. |
| `stormpy.SparseIntervalModelComponents`<br>`stormpy.storage.SparseIntervalModelComponents` | `stormpy.models.SparseModelComponents[stormpy.Interval]` | Becomes a template. |
| `stormpy.SparseIntervalModelState`<br>`stormpy.storage.SparseIntervalModelState` | `stormpy.models.SparseModelState[stormpy.Interval]` | Becomes a template. |
| `stormpy.SparseIntervalModelStates`<br>`stormpy.storage.SparseIntervalModelStates` | `stormpy.models.SparseModelStates[stormpy.Interval]` | Becomes a template. |
| `stormpy.SparseIntervalPomdp`<br>`stormpy.storage.SparseIntervalPomdp` | `stormpy.models.SparsePomdp[stormpy.Interval]` | Becomes a template. |
| `stormpy.SparseIntervalRewardModel`<br>`stormpy.storage.SparseIntervalRewardModel` | `stormpy.models.SparseRewardModel[stormpy.Interval]` | Becomes a template. |
| `stormpy.SparseIntervalSmg`<br>`stormpy.storage.SparseIntervalSmg` | `stormpy.models.SparseSmg[stormpy.Interval]` | Becomes a template. |
| `stormpy.SparseMA`<br>`stormpy.storage.SparseMA` | `stormpy.models.SparseMA[float]` | Becomes a template. |
| `stormpy.SparseMatrix`<br>`stormpy.storage.SparseMatrix` | `stormpy.datastructures.SparseMatrix[float]` | Becomes a template. |
| `stormpy.SparseMatrixBuilder`<br>`stormpy.storage.SparseMatrixBuilder` | `stormpy.datastructures.SparseMatrixBuilder[float]` | Becomes a template. |
| `stormpy.SparseMatrixEntry`<br>`stormpy.storage.SparseMatrixEntry` | `stormpy.datastructures.SparseMatrixEntry[float]` | Becomes a template. |
| `stormpy.SparseMatrixRows`<br>`stormpy.storage.SparseMatrixRows` | `stormpy.datastructures.SparseMatrixRows[float]` | Becomes a template. |
| `stormpy.SparseMdp`<br>`stormpy.storage.SparseMdp` | `stormpy.models.SparseMdp[float]` | Becomes a template. |
| `stormpy.SparseModelAction`<br>`stormpy.storage.SparseModelAction` | `stormpy.models.SparseModelAction[float]` | Becomes a template. |
| `stormpy.SparseModelActions`<br>`stormpy.storage.SparseModelActions` | `stormpy.models.SparseModelActions[float]` | Becomes a template. |
| `stormpy.SparseModelComponents`<br>`stormpy.storage.SparseModelComponents` | `stormpy.models.SparseModelComponents[float]` | Becomes a template. |
| `stormpy.SparseModelMemoryProductReverseData`<br>`stormpy.storage.SparseModelMemoryProductReverseData` | `stormpy.developer.storage.SparseModelMemoryProductReverseData` |  |
| `stormpy.SparseModelState`<br>`stormpy.storage.SparseModelState` | `stormpy.models.SparseModelState[float]` | Becomes a template. |
| `stormpy.SparseModelStates`<br>`stormpy.storage.SparseModelStates` | `stormpy.models.SparseModelStates[float]` | Becomes a template. |
| `stormpy.SparseParametricCtmc`<br>`stormpy.storage.SparseParametricCtmc` | `stormpy.models.SparseCtmc[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.SparseParametricDtmc`<br>`stormpy.storage.SparseParametricDtmc` | `stormpy.models.SparseDtmc[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.SparseParametricMA`<br>`stormpy.storage.SparseParametricMA` | `stormpy.models.SparseMA[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.SparseParametricMdp`<br>`stormpy.storage.SparseParametricMdp` | `stormpy.models.SparseMdp[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.SparseParametricModelAction`<br>`stormpy.storage.SparseParametricModelAction` | `stormpy.models.SparseModelAction[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.SparseParametricModelActions`<br>`stormpy.storage.SparseParametricModelActions` | `stormpy.models.SparseModelActions[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.SparseParametricModelComponents`<br>`stormpy.storage.SparseParametricModelComponents` | `stormpy.models.SparseModelComponents[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.SparseParametricModelState`<br>`stormpy.storage.SparseParametricModelState` | `stormpy.models.SparseModelState[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.SparseParametricModelStates`<br>`stormpy.storage.SparseParametricModelStates` | `stormpy.models.SparseModelStates[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.SparseParametricPomdp`<br>`stormpy.storage.SparseParametricPomdp` | `stormpy.models.SparsePomdp[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.SparseParametricRewardModel`<br>`stormpy.storage.SparseParametricRewardModel` | `stormpy.models.SparseRewardModel[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.SparseParametricSmg`<br>`stormpy.storage.SparseParametricSmg` | `stormpy.models.SparseSmg[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.SparsePomdp`<br>`stormpy.storage.SparsePomdp` | `stormpy.models.SparsePomdp[float]` | Becomes a template. |
| `stormpy.SparseRationalIntervalCtmc`<br>`stormpy.storage.SparseRationalIntervalCtmc` | `stormpy.models.SparseCtmc[stormpy.RationalInterval]` | Becomes a template. |
| `stormpy.SparseRationalIntervalDtmc`<br>`stormpy.storage.SparseRationalIntervalDtmc` | `stormpy.models.SparseDtmc[stormpy.RationalInterval]` | Becomes a template. |
| `stormpy.SparseRationalIntervalMA`<br>`stormpy.storage.SparseRationalIntervalMA` | `stormpy.models.SparseMA[stormpy.RationalInterval]` | Becomes a template. |
| `stormpy.SparseRationalIntervalMdp`<br>`stormpy.storage.SparseRationalIntervalMdp` | `stormpy.models.SparseMdp[stormpy.RationalInterval]` | Becomes a template. |
| `stormpy.SparseRationalIntervalModelAction`<br>`stormpy.storage.SparseRationalIntervalModelAction` | `stormpy.models.SparseModelAction[stormpy.RationalInterval]` | Becomes a template. |
| `stormpy.SparseRationalIntervalModelActions`<br>`stormpy.storage.SparseRationalIntervalModelActions` | `stormpy.models.SparseModelActions[stormpy.RationalInterval]` | Becomes a template. |
| `stormpy.SparseRationalIntervalModelComponents`<br>`stormpy.storage.SparseRationalIntervalModelComponents` | `stormpy.models.SparseModelComponents[stormpy.RationalInterval]` | Becomes a template. |
| `stormpy.SparseRationalIntervalModelState`<br>`stormpy.storage.SparseRationalIntervalModelState` | `stormpy.models.SparseModelState[stormpy.RationalInterval]` | Becomes a template. |
| `stormpy.SparseRationalIntervalModelStates`<br>`stormpy.storage.SparseRationalIntervalModelStates` | `stormpy.models.SparseModelStates[stormpy.RationalInterval]` | Becomes a template. |
| `stormpy.SparseRationalIntervalPomdp`<br>`stormpy.storage.SparseRationalIntervalPomdp` | `stormpy.models.SparsePomdp[stormpy.RationalInterval]` | Becomes a template. |
| `stormpy.SparseRationalIntervalRewardModel`<br>`stormpy.storage.SparseRationalIntervalRewardModel` | `stormpy.models.SparseRewardModel[stormpy.RationalInterval]` | Becomes a template. |
| `stormpy.SparseRationalIntervalSmg`<br>`stormpy.storage.SparseRationalIntervalSmg` | `stormpy.models.SparseSmg[stormpy.RationalInterval]` | Becomes a template. |
| `stormpy.SparseRewardModel`<br>`stormpy.storage.SparseRewardModel` | `stormpy.models.SparseRewardModel[float]` | Becomes a template. |
| `stormpy.SparseSmg`<br>`stormpy.storage.SparseSmg` | `stormpy.models.SparseSmg[float]` | Becomes a template. |
| `stormpy.StateFormula`<br>`stormpy.logic.StateFormula` | `stormpy.logic.StateFormula` |  |
| `stormpy.StateLabeling`<br>`stormpy.storage.StateLabeling` | `stormpy.models.StateLabeling` |  |
| `stormpy.StateValuation`<br>`stormpy.storage.StateValuation` | `stormpy.models.Valuations` | Removed deprecated alias; use Valuations. |
| `stormpy.StateValuationFunctionActionMaskDouble` | `stormpy.developer.StateValuationFunctionMask[float]` | Renamed generic family. |
| `stormpy.StateValuationTransformer`<br>`stormpy.storage.StateValuationTransformer` | `stormpy.models.ValuationTransformer` | Removed deprecated shim; revised interface. |
| `stormpy.StateValuationsBuilder`<br>`stormpy.storage.StateValuationsBuilder` | `stormpy.models.ValuationDescriptionBuilder` | Replacement for the deprecated shim; combine ValuationDescriptionBuilder with Valuations. Not a drop-in rename. |
| `stormpy.SteadyStateDistributionAlgorithm` | `stormpy.environments.SteadyStateDistributionAlgorithm` |  |
| `stormpy.SubsystemBuilderOptions` | `stormpy.transformations.SubsystemBuilderOptions` |  |
| `stormpy.SubsystemBuilderReturnTypeDouble` | `stormpy.transformations.SubsystemBuilderReturnType[float]` | Becomes a template. |
| `stormpy.SubsystemBuilderReturnTypeExact` | `stormpy.transformations.SubsystemBuilderReturnType[stormpy.Rational]` | Becomes a template. |
| `stormpy.SubsystemBuilderReturnTypeInterval` | `stormpy.transformations.SubsystemBuilderReturnType[stormpy.Interval]` | Becomes a template. |
| `stormpy.SubsystemBuilderReturnTypeRatFunc` | `stormpy.transformations.SubsystemBuilderReturnType[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.SubsystemBuilderReturnTypeRationalInterval` | `stormpy.transformations.SubsystemBuilderReturnType[stormpy.RationalInterval]` | Becomes a template. |
| `stormpy.SylvanDdManagerEnvironment` | `stormpy.environments.SylvanDdManagerEnvironment` |  |
| `stormpy.SymbolicExactQuantitativeCheckResult` | `stormpy.results.SymbolicQuantitativeCheckResult[stormpy.models.DdType.Sylvan, stormpy.Rational]` | Becomes a template. |
| `stormpy.SymbolicModelDescription` | `stormpy.io.SymbolicModelDescription` |  |
| `stormpy.SymbolicParametricQuantitativeCheckResult` | `stormpy.results.SymbolicQuantitativeCheckResult[stormpy.models.DdType.Sylvan, stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.SymbolicQualitativeCheckResult` | `stormpy.results.SymbolicQualitativeCheckResult[stormpy.models.DdType.Sylvan]` | Becomes a template. |
| `stormpy.SymbolicQuantitativeCheckResult` | `stormpy.results.SymbolicQuantitativeCheckResult[stormpy.models.DdType.Sylvan, float]` | Becomes a template. |
| `stormpy.SymbolicSylvanCtmc`<br>`stormpy.storage.SymbolicSylvanCtmc` | `stormpy.models.SymbolicCtmc[stormpy.models.DdType.Sylvan, float]` | Becomes a template. |
| `stormpy.SymbolicSylvanDtmc`<br>`stormpy.storage.SymbolicSylvanDtmc` | `stormpy.models.SymbolicDtmc[stormpy.models.DdType.Sylvan, float]` | Becomes a template. |
| `stormpy.SymbolicSylvanExactCtmc`<br>`stormpy.storage.SymbolicSylvanExactCtmc` | `stormpy.models.SymbolicCtmc[stormpy.models.DdType.Sylvan, stormpy.Rational]` | Becomes a template. |
| `stormpy.SymbolicSylvanExactDtmc`<br>`stormpy.storage.SymbolicSylvanExactDtmc` | `stormpy.models.SymbolicDtmc[stormpy.models.DdType.Sylvan, stormpy.Rational]` | Becomes a template. |
| `stormpy.SymbolicSylvanExactMA`<br>`stormpy.storage.SymbolicSylvanExactMA` | `stormpy.models.SymbolicMA[stormpy.models.DdType.Sylvan, stormpy.Rational]` | Becomes a template. |
| `stormpy.SymbolicSylvanExactMdp`<br>`stormpy.storage.SymbolicSylvanExactMdp` | `stormpy.models.SymbolicMdp[stormpy.models.DdType.Sylvan, stormpy.Rational]` | Becomes a template. |
| `stormpy.SymbolicSylvanExactRewardModel`<br>`stormpy.storage.SymbolicSylvanExactRewardModel` | `stormpy.models.SymbolicRewardModel[stormpy.models.DdType.Sylvan, stormpy.Rational]` | Becomes a template. |
| `stormpy.SymbolicSylvanMA`<br>`stormpy.storage.SymbolicSylvanMA` | `stormpy.models.SymbolicMA[stormpy.models.DdType.Sylvan, float]` | Becomes a template. |
| `stormpy.SymbolicSylvanMdp`<br>`stormpy.storage.SymbolicSylvanMdp` | `stormpy.models.SymbolicMdp[stormpy.models.DdType.Sylvan, float]` | Becomes a template. |
| `stormpy.SymbolicSylvanParametricCtmc`<br>`stormpy.storage.SymbolicSylvanParametricCtmc` | `stormpy.models.SymbolicCtmc[stormpy.models.DdType.Sylvan, stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.SymbolicSylvanParametricDtmc`<br>`stormpy.storage.SymbolicSylvanParametricDtmc` | `stormpy.models.SymbolicDtmc[stormpy.models.DdType.Sylvan, stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.SymbolicSylvanParametricMA`<br>`stormpy.storage.SymbolicSylvanParametricMA` | `stormpy.models.SymbolicMA[stormpy.models.DdType.Sylvan, stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.SymbolicSylvanParametricMdp`<br>`stormpy.storage.SymbolicSylvanParametricMdp` | `stormpy.models.SymbolicMdp[stormpy.models.DdType.Sylvan, stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.SymbolicSylvanParametricRewardModel`<br>`stormpy.storage.SymbolicSylvanParametricRewardModel` | `stormpy.models.SymbolicRewardModel[stormpy.models.DdType.Sylvan, stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.SymbolicSylvanRewardModel`<br>`stormpy.storage.SymbolicSylvanRewardModel` | `stormpy.models.SymbolicRewardModel[stormpy.models.DdType.Sylvan, float]` | Becomes a template. |
| `stormpy.TimeOperator`<br>`stormpy.logic.TimeOperator` | `stormpy.logic.TimeOperatorFormula` | Added Formula suffix. |
| `stormpy.UmbExportOptions`<br>`stormpy.storage.UmbExportOptions` | `stormpy.io.UmbExportOptions` |  |
| `stormpy.UmbExportValueType`<br>`stormpy.storage.UmbExportValueType` | `stormpy.io.UmbExportValueType` |  |
| `stormpy.UmbImportOptions`<br>`stormpy.storage.UmbImportOptions` | `stormpy.io.UmbImportOptions` |  |
| `stormpy.UmbImportValueType`<br>`stormpy.storage.UmbImportValueType` | `stormpy.io.UmbImportValueType` |  |
| `stormpy.UmbModel`<br>`stormpy.storage.UmbModel` | `stormpy.io.UmbModel` |  |
| `stormpy.UnaryBooleanStateFormula`<br>`stormpy.logic.UnaryBooleanStateFormula` | `stormpy.logic.UnaryBooleanStateFormula` |  |
| `stormpy.UnaryPathFormula`<br>`stormpy.logic.UnaryPathFormula` | `stormpy.logic.UnaryPathFormula` |  |
| `stormpy.UnaryStateFormula`<br>`stormpy.logic.UnaryStateFormula` | `stormpy.logic.UnaryStateFormula` |  |
| `stormpy.UncertaintyResolutionMode` | `stormpy.UncertaintyResolutionMode` |  |
| `stormpy.UntilFormula`<br>`stormpy.logic.UntilFormula` | `stormpy.logic.UntilFormula` |  |
| `stormpy.Valuation`<br>`stormpy.storage.Valuation` | `stormpy.developer.storage.Valuation` |  |
| `stormpy.ValuationClassDescription`<br>`stormpy.storage.ValuationClassDescription` | `stormpy.models.ValuationClassDescription` |  |
| `stormpy.ValuationDescriptionBuilder`<br>`stormpy.storage.ValuationDescriptionBuilder` | `stormpy.models.ValuationDescriptionBuilder` |  |
| `stormpy.ValuationTransformer`<br>`stormpy.storage.ValuationTransformer` | `stormpy.models.ValuationTransformer` |  |
| `stormpy.Valuations`<br>`stormpy.storage.Valuations` | `stormpy.models.Valuations` |  |
| `stormpy.Variable`<br>`stormpy.storage.Variable` | `stormpy.expressions.Variable` |  |
| `stormpy.WeightedObjectiveMdpModelCheckerDouble` | `stormpy.developer.PcaaWeightVectorChecker[float]` | Renamed raw checker; construct via create_weight_vector_checker. |
| `stormpy.WeightedObjectiveMdpModelCheckerExact` | `stormpy.developer.PcaaWeightVectorChecker[stormpy.Rational]` | Renamed raw checker; construct via create_weight_vector_checker. |
| `stormpy.build_exact_interval_model_from_drn` | `stormpy.build_model_from_drn[stormpy.RationalInterval]` | options is keyword-only. |
| `stormpy.build_from_umb` | `stormpy.build_model_from_umb` | Renamed; options is keyword-only. |
| `stormpy.build_interval_model_from_drn` | `stormpy.build_model_from_drn[stormpy.Interval]` | options is keyword-only. |
| `stormpy.build_model` | `stormpy.build_model[float]` | Default remains float; build_model(...) is also valid. Value type is selected by; builder options and engine are keyword-only. |
| `stormpy.build_model_from_drn` | `stormpy.build_model_from_drn[float]` | Default remains float; options is keyword-only. Use a value-type for other numeric types. |
| `stormpy.build_parametric_model` | `stormpy.build_model[stormpy.RationalFunction]` | Select the value type using a. |
| `stormpy.build_parametric_model_from_drn` | `stormpy.build_model_from_drn[stormpy.RationalFunction]` | options is keyword-only. |
| `stormpy.build_parametric_sparse_matrix`<br>`stormpy.storage.build_parametric_sparse_matrix` | `stormpy.datastructures.build_sparse_matrix[stormpy.RationalFunction]` | Unified templated matrix builder. |
| `stormpy.build_sparse_exact_interval_model` | `stormpy.build_model[stormpy.RationalInterval]` | Select the value type using a. |
| `stormpy.build_sparse_exact_interval_model_with_options` | `stormpy.build_model[stormpy.RationalInterval]` | Pass builder options via options=... . |
| `stormpy.build_sparse_exact_model` | `stormpy.build_model[stormpy.Rational]` | Select the value type using a. |
| `stormpy.build_sparse_exact_model_with_options` | `stormpy.build_model[stormpy.Rational]` | Pass builder options via options=... . |
| `stormpy.build_sparse_interval_model` | `stormpy.build_model[stormpy.Interval]` | Select the value type using a. |
| `stormpy.build_sparse_interval_model_with_options` | `stormpy.build_model[stormpy.Interval]` | Pass builder options via options=... . |
| `stormpy.build_sparse_matrix`<br>`stormpy.storage.build_sparse_matrix` | `stormpy.datastructures.build_sparse_matrix[float]` | Becomes a template. |
| `stormpy.build_sparse_model` | `stormpy.build_model[float]` | Sparse is the default engine. |
| `stormpy.build_sparse_model_from_explicit` | `stormpy.build_model_from_explicit` | Renamed; optional arguments are keyword-only. |
| `stormpy.build_sparse_model_with_options` | `stormpy.build_model[float]` | Pass builder options via options=... . |
| `stormpy.build_sparse_parametric_model` | `stormpy.build_model[stormpy.RationalFunction]` | Select the value type using a. |
| `stormpy.build_sparse_parametric_model_with_options` | `stormpy.build_model[stormpy.RationalFunction]` | Pass builder options via options=... . |
| `stormpy.build_symbolic_model` | `stormpy.build_symbolic_model[float]` | Default remains float; environment is keyword-only. Use a value-type for parametric or exact models. |
| `stormpy.build_symbolic_parametric_model` | `stormpy.build_symbolic_model[stormpy.RationalFunction]` | Select the value type using a. |
| `stormpy.check_exact_interval_dtmc` | `stormpy.model_checking` | Unified wrapper; supply uncertainty_resolution_mode explicitly for interval models. Optional arguments are keyword-only. Defaults to a sound/exact environment selected for the model; numerical result access changed. |
| `stormpy.check_exact_interval_mdp` | `stormpy.model_checking` | Unified wrapper; supply uncertainty_resolution_mode explicitly for interval models. Optional arguments are keyword-only. Defaults to a sound/exact environment selected for the model; numerical result access changed. |
| `stormpy.check_interval_dtmc` | `stormpy.model_checking` | Unified wrapper; supply uncertainty_resolution_mode explicitly for interval models. Optional arguments are keyword-only. Defaults to a sound/exact environment selected for the model; numerical result access changed. |
| `stormpy.check_interval_mdp` | `stormpy.model_checking` | Unified wrapper; supply uncertainty_resolution_mode explicitly for interval models. Optional arguments are keyword-only. Defaults to a sound/exact environment selected for the model; numerical result access changed. |
| `stormpy.check_model_dd` | `stormpy.model_checking` | Use engine=stormpy.Engine.DD. Optional arguments are keyword-only. Optional arguments are keyword-only. Defaults to a sound/exact environment selected for the model; numerical result access changed. |
| `stormpy.check_model_hybrid` | `stormpy.model_checking` | Use engine=stormpy.Engine.HYBRID. Optional arguments are keyword-only. Optional arguments are keyword-only. Defaults to a sound/exact environment selected for the model; numerical result access changed. |
| `stormpy.check_model_sparse` | `stormpy.model_checking` | Use engine=stormpy.Engine.SPARSE. Optional arguments are keyword-only. Optional arguments are keyword-only. Defaults to a sound/exact environment selected for the model; numerical result access changed. |
| `stormpy.collect_information`<br>`stormpy.storage.collect_information` | `stormpy.developer.storage.collect_model_information` | Renamed raw binding. |
| `stormpy.compute_all_until_probabilities` | `stormpy.developer.compute_all_until_probabilities` |  |
| `stormpy.compute_expected_number_of_visits` | `stormpy.analysis.compute_expected_number_of_visits` | Changed from (environment, model) to (model, *, environment=None); returns a CheckResult instead of a vector. |
| `stormpy.compute_prob01_states` | `stormpy.analysis.compute_prob01_states` | Changed from (model, phi_states, psi_states) to (model, property). Raw bitvector API remains at developer.perform_prob01 / perform_prob01_min / perform_prob01_max. |
| `stormpy.compute_prob01max_states` | `stormpy.analysis.compute_prob01_states` | Unified wrapper takes a property; use Pmin or Pmax in that property. Raw bitvector API: developer.perform_prob01_min / perform_prob01_max. Changed from (model, phi_states, psi_states) to (model, property). Raw bitvector API remains at developer.perform_prob01 / perform_prob01_min / perform_prob01_max. |
| `stormpy.compute_prob01min_states` | `stormpy.analysis.compute_prob01_states` | Unified wrapper takes a property; use Pmin or Pmax in that property. Raw bitvector API: developer.perform_prob01_min / perform_prob01_max. Changed from (model, phi_states, psi_states) to (model, property). Raw bitvector API remains at developer.perform_prob01 / perform_prob01_min / perform_prob01_max. |
| `stormpy.compute_steady_state_distribution` | `stormpy.analysis.compute_steady_state_distribution` | Changed from (environment, model) to (model, *, environment=None); returns a CheckResult instead of a vector. |
| `stormpy.compute_transient_probabilities` | `stormpy.developer.compute_all_transient_probabilities` | Renamed raw binding. |
| `stormpy.construct_submodel` | `stormpy.transformations.build_submodel` | Renamed and changed interface; inspect build_submodel signature. |
| `stormpy.create_filter_initial_states_sparse` | `stormpy.create_filter_initial_states` | Unified wrapper deduces model representation and value type. |
| `stormpy.create_filter_initial_states_sparseExact` | `stormpy.create_filter_initial_states` | Unified wrapper deduces model representation and value type. |
| `stormpy.create_filter_initial_states_symbolic` | `stormpy.create_filter_initial_states` | Unified wrapper deduces model representation and value type. |
| `stormpy.create_filter_initial_states_symbolicExact` | `stormpy.create_filter_initial_states` | Unified wrapper deduces model representation and value type. |
| `stormpy.create_filter_symbolic` | `stormpy.create_filter` | Unified wrapper deduces model representation and value type. |
| `stormpy.create_filter_symbolicExact` | `stormpy.create_filter` | Unified wrapper deduces model representation and value type. |
| `stormpy.dft.ApproximationHeuristic` | `stormpy.dft.ApproximationHeuristic` |  |
| `stormpy.dft.DFTBE_double` | `stormpy.dft.DFTBE[float]` | Becomes a template. |
| `stormpy.dft.DFTBE_ratfunc` | `stormpy.dft.DFTBE[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.dft.DFTDependency_double` | `stormpy.dft.DFTDependency[float]` | Becomes a template. |
| `stormpy.dft.DFTDependency_ratfunc` | `stormpy.dft.DFTDependency[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.dft.DFTElementType` | `stormpy.dft.DFTElementType` |  |
| `stormpy.dft.DFTElement_double` | `stormpy.dft.DFTElement[float]` | Becomes a template. |
| `stormpy.dft.DFTElement_ratfunc` | `stormpy.dft.DFTElement[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.dft.DFTInstantiator` | `stormpy.dft.DftInstantiator[stormpy.RationalFunction, float]` | Changed capitalization and added source/target type parameters. |
| `stormpy.dft.DFTSimulator_double` | `stormpy.dft.developer.DFTTraceSimulator[float]` | Renamed native simulator. Public DFTSimulator is a Python wrapper. |
| `stormpy.dft.DFTSimulator_ratfunc` | `stormpy.dft.developer.DFTTraceSimulator[stormpy.RationalFunction]` | Renamed native simulator. Public DFTSimulator is a Python wrapper. |
| `stormpy.dft.DFTStateInfo` | `stormpy.dft.developer.DFTStateGenerationInfo` | Renamed raw binding. |
| `stormpy.dft.DFTState_double` | `stormpy.dft.DFTState[float]` | Becomes a template. |
| `stormpy.dft.DFTState_ratfunc` | `stormpy.dft.DFTState[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.dft.DFT_double` | `stormpy.dft.DFT[float]` | Becomes a template. |
| `stormpy.dft.DFT_ratfunc` | `stormpy.dft.DFT[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.dft.DftIndependentModule` | `stormpy.dft.DftIndependentModule` |  |
| `stormpy.dft.DftSymmetries` | `stormpy.dft.DftSymmetries` |  |
| `stormpy.dft.ExplicitDFTModelBuilder_double` | `stormpy.dft.developer.ExplicitDFTModelBuilder[float]` | Becomes a template. |
| `stormpy.dft.ExplicitDFTModelBuilder_ratfunc` | `stormpy.dft.developer.ExplicitDFTModelBuilder[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.dft.FailableElement` | `stormpy.dft.developer.FailableElement` |  |
| `stormpy.dft.FailableElements` | `stormpy.dft.developer.FailableElements` |  |
| `stormpy.dft.FailableIterator` | `stormpy.dft.developer.FailableIterator` |  |
| `stormpy.dft.RandomGenerator` | `stormpy.dft.developer.RandomGenerator` |  |
| `stormpy.dft.RelevantEvents` | `stormpy.dft.RelevantEvents` |  |
| `stormpy.dft.SimulationStepResult` | `stormpy.dft.SimulationStepResult` |  |
| `stormpy.dft.SimulationTraceResult` | `stormpy.dft.SimulationTraceResult` |  |
| `stormpy.dft.analyze_dft` | `stormpy.dft.analyze_dft` | Same path, revised environment-based interface. |
| `stormpy.dft.build_model` | `stormpy.dft.build_model` | Same path, revised environment-based interface. |
| `stormpy.dft.compute_dependency_conflicts` | `stormpy.dft.developer.compute_dependency_conflicts` |  |
| `stormpy.dft.compute_relevant_events` | `stormpy.dft.compute_relevant_events` |  |
| `stormpy.dft.export_dft_json_file` | `stormpy.dft.export_dft_json_file` |  |
| `stormpy.dft.export_dft_json_string` | `stormpy.dft.export_dft_json_string` |  |
| `stormpy.dft.export_parametric_dft_json_file` | `stormpy.dft.export_dft_json_file` | Unified wrapper deduces the value type from the DFT. |
| `stormpy.dft.export_parametric_dft_json_string` | `stormpy.dft.export_dft_json_string` | Unified wrapper deduces the value type from the DFT. |
| `stormpy.dft.get_parameters` | `stormpy.dft.developer.get_parameters` |  |
| `stormpy.dft.has_potential_modeling_issues` | `stormpy.dft.developer.has_potential_modeling_issues` |  |
| `stormpy.dft.is_well_formed` | `stormpy.dft.developer.is_well_formed` |  |
| `stormpy.dft.load_dft_galileo_file` | `stormpy.dft.load_dft_galileo_file[float]` | Becomes a template. |
| `stormpy.dft.load_dft_json_file` | `stormpy.dft.load_dft_json_file[float]` | Becomes a template. |
| `stormpy.dft.load_dft_json_string` | `stormpy.dft.load_dft_json_string[float]` | Becomes a template. |
| `stormpy.dft.load_parametric_dft_galileo_file` | `stormpy.dft.load_dft_galileo_file[stormpy.RationalFunction]` | Select parametric DFT values with a. |
| `stormpy.dft.load_parametric_dft_json_file` | `stormpy.dft.load_dft_json_file[stormpy.RationalFunction]` | Select parametric DFT values with a. |
| `stormpy.dft.load_parametric_dft_json_string` | `stormpy.dft.load_dft_json_string[stormpy.RationalFunction]` | Select parametric DFT values with a. |
| `stormpy.dft.modules.modules_json` | `stormpy.dft.modules_json` | Use the public DFT module helper. Still public; module decomposition implementation changed. |
| `stormpy.dft.modules_json` | `stormpy.dft.modules_json` | Still public; module decomposition implementation changed. |
| `stormpy.dft.prepare_for_analysis` | `stormpy.dft.prepare_for_analysis` | Same path, revised environment-based transformation settings. |
| `stormpy.dft.simulator.DftSimulator` | `stormpy.dft.DFTSimulator` | Renamed to DFTSimulator and exported directly by stormpy.dft; constructor options are keyword-only. |
| `stormpy.dft.transform_dft` | `stormpy.dft.developer.transform_dft` |  |
| `stormpy.eliminate_ECs` | `stormpy.developer.EndComponentEliminator` | Use the templated eliminator class; changed interface. |
| `stormpy.eliminate_non_markovian_chains` | `stormpy.transformations.eliminate_non_markovian_chains` |  |
| `stormpy.eliminate_reward_accumulations`<br>`stormpy.storage.eliminate_reward_accumulations` | `stormpy.developer.storage.RewardAccumulationEliminationVisitor` | Use the visitor and its eliminate_reward_accumulations method. Changed interface. |
| `stormpy.exceptions.StormError` | `stormpy.exceptions.StormError` |  |
| `stormpy.export_jani_to_file`<br>`stormpy.storage.export_jani_to_file` | `stormpy.io.export_jani_to_file` |  |
| `stormpy.export_to_drn` | `stormpy.io.export_to_drn` |  |
| `stormpy.export_to_umb` | `stormpy.io.export_to_umb` |  |
| `stormpy.get_maximal_end_components`<br>`stormpy.storage.get_maximal_end_components` | `stormpy.analysis.get_maximal_end_components` |  |
| `stormpy.get_reachable_states` | `stormpy.developer.get_reachable_states` | Raw binding; changed signature. |
| `stormpy.gspn.GSPN` | `stormpy.gspn.GSPN` |  |
| `stormpy.gspn.GSPNBuilder` | `stormpy.gspn.GspnBuilder` | Changed capitalization. |
| `stormpy.gspn.GSPNParser` | `stormpy.gspn.developer.GspnParser` | Changed capitalization; public loading entry point is load_gspn_file. |
| `stormpy.gspn.GSPNToJaniBuilder` | `stormpy.gspn.developer.JaniGSPNBuilder` | Renamed raw builder; public wrapper is build_jani_model. |
| `stormpy.gspn.ImmediateTransition` | `stormpy.gspn.ImmediateTransition` |  |
| `stormpy.gspn.LayoutInfo` | `stormpy.gspn.LayoutInfo` |  |
| `stormpy.gspn.Place` | `stormpy.gspn.Place` |  |
| `stormpy.gspn.TimedTransition` | `stormpy.gspn.TimedTransition` |  |
| `stormpy.gspn.Transition` | `stormpy.gspn.Transition` |  |
| `stormpy.gspn.TransitionPartition` | `stormpy.gspn.TransitionPartition` |  |
| `stormpy.import_umb`<br>`stormpy.storage.import_umb` | `stormpy.io.import_umb` |  |
| `stormpy.info.Version` | `stormpy.developer.info.StormVersion` | Renamed raw version object; member names changed. Prefer stormpy.info helpers. |
| `stormpy.info.storm_build_type` | `stormpy.info.storm_build_type` |  |
| `stormpy.info.storm_development_version` | `stormpy.info.storm_development_version` |  |
| `stormpy.info.storm_directory` | `stormpy.info.storm_directory` |  |
| `stormpy.info.storm_exact_use_cln` | `stormpy.info.storm_exact_use_cln` |  |
| `stormpy.info.storm_from_system` | `stormpy.info.storm_from_system` |  |
| `stormpy.info.storm_origin_info` | `stormpy.info.storm_origin_info` |  |
| `stormpy.info.storm_ratfunc_use_cln` | `stormpy.info.storm_ratfunc_use_cln` |  |
| `stormpy.info.storm_version` | `stormpy.info.storm_version` |  |
| `stormpy.install_signal_handlers` | `stormpy.developer.install_signal_handler` | Renamed raw binding. |
| `stormpy.make_sparse_model_builder` | `stormpy.developer.make_explicit_model_builder[float]` | Renamed templated factory. |
| `stormpy.make_sparse_model_builder_exact` | `stormpy.developer.make_explicit_model_builder[stormpy.Rational]` | Renamed templated factory. |
| `stormpy.make_sparse_model_builder_parametric` | `stormpy.developer.make_explicit_model_builder[stormpy.RationalFunction]` | Renamed templated factory. |
| `stormpy.make_weighted_objective_mdp_model_checker` | `stormpy.developer.create_weight_vector_checker` | Revised factory and interface. |
| `stormpy.model_checking` | `stormpy.model_checking` | Optional arguments are keyword-only. Defaults to a sound/exact environment selected for the model; numerical result access changed. |
| `stormpy.pars.DtmcParameterLiftingModelChecker` | `stormpy.pars.developer.SparseDtmcParameterLiftingModelChecker` | Renamed and revised raw checker. |
| `stormpy.pars.MdpParameterLiftingModelChecker` | `stormpy.pars.developer.SparseMdpParameterLiftingModelChecker` | Renamed and revised raw checker. |
| `stormpy.pars.ModelInstantiator` | `stormpy.pars.ModelInstantiator` | Now a generic family indexed by ModelType and target ValueType; model kind is deduced and target defaults to float when called without a. |
| `stormpy.pars.PCtmcExactInstantiationChecker` | `stormpy.pars.developer.SparseInstantiationModelChecker[stormpy.models.ModelType.CTMC, stormpy.Rational]` | Renamed generic family with model kind and result type parameters. |
| `stormpy.pars.PCtmcInstantiationChecker` | `stormpy.pars.developer.SparseInstantiationModelChecker[stormpy.models.ModelType.CTMC, float]` | Renamed generic family with model kind and result type parameters. |
| `stormpy.pars.PCtmcInstantiator` | `stormpy.pars.ModelInstantiator[stormpy.models.ModelType.CTMC, float]` | Model kind and target value type are explicit parameters. |
| `stormpy.pars.PDtmcExactInstantiationChecker` | `stormpy.pars.developer.SparseInstantiationModelChecker[stormpy.models.ModelType.DTMC, stormpy.Rational]` | Renamed generic family with model kind and result type parameters. |
| `stormpy.pars.PDtmcInstantiationChecker` | `stormpy.pars.developer.SparseInstantiationModelChecker[stormpy.models.ModelType.DTMC, float]` | Renamed generic family with model kind and result type parameters. |
| `stormpy.pars.PDtmcInstantiator` | `stormpy.pars.ModelInstantiator[stormpy.models.ModelType.DTMC, float]` | Model kind and target value type are explicit parameters. |
| `stormpy.pars.PMaInstantiator` | `stormpy.pars.ModelInstantiator[stormpy.models.ModelType.MA, float]` | Model kind and target value type are explicit parameters. |
| `stormpy.pars.PMdpExactInstantiationChecker` | `stormpy.pars.developer.SparseInstantiationModelChecker[stormpy.models.ModelType.MDP, stormpy.Rational]` | Renamed generic family with model kind and result type parameters. |
| `stormpy.pars.PMdpInstantiationChecker` | `stormpy.pars.developer.SparseInstantiationModelChecker[stormpy.models.ModelType.MDP, float]` | Renamed generic family with model kind and result type parameters. |
| `stormpy.pars.PMdpInstantiator` | `stormpy.pars.ModelInstantiator[stormpy.models.ModelType.MDP, float]` | Model kind and target value type are explicit parameters. |
| `stormpy.pars.ParameterRegion` | `stormpy.pars.ParameterRegion` |  |
| `stormpy.pars.PartialPCtmcInstantiator` | `stormpy.pars.ModelInstantiator[stormpy.models.ModelType.CTMC, stormpy.RationalFunction]` | Model kind and target value type are explicit parameters. |
| `stormpy.pars.PartialPDtmcInstantiator` | `stormpy.pars.ModelInstantiator[stormpy.models.ModelType.DTMC, stormpy.RationalFunction]` | Model kind and target value type are explicit parameters. |
| `stormpy.pars.PartialPMaInstantiator` | `stormpy.pars.ModelInstantiator[stormpy.models.ModelType.MA, stormpy.RationalFunction]` | Model kind and target value type are explicit parameters. |
| `stormpy.pars.PartialPMdpInstantiator` | `stormpy.pars.ModelInstantiator[stormpy.models.ModelType.MDP, stormpy.RationalFunction]` | Model kind and target value type are explicit parameters. |
| `stormpy.pars.RegionModelChecker` | `stormpy.pars.developer.RegionModelChecker` |  |
| `stormpy.pars.RegionRefinementChecker` | `stormpy.pars.developer.RegionRefinementChecker` |  |
| `stormpy.pars.RegionResult` | `stormpy.pars.RegionResult` |  |
| `stormpy.pars.RegionResultHypothesis` | `stormpy.pars.developer.RegionResultHypothesis` |  |
| `stormpy.pars.create_region_checker` | `stormpy.pars.developer.initialize_region_model_checker` | Revised raw factory and signature; use pars.verify for the public API. |
| `stormpy.pars.create_region_refinement_checker` | `stormpy.pars.developer.initialize_region_refinement_checker` | Revised raw factory and signature. |
| `stormpy.pars.gather_derivatives` | `stormpy.pars.gather_derivatives` |  |
| `stormpy.pars.simplify_model` | `stormpy.pars.developer.SparseParametricModelSimplifier` | Use the generic simplifier class; instantiate with a model, call simplify, then read simplified_model and simplified_formula. |
| `stormpy.parse_constants_string` | `stormpy.developer.parse_constant_definition_string` | Renamed raw binding. |
| `stormpy.parse_jani_model` | `stormpy.parse_jani_model` |  |
| `stormpy.parse_jani_model_from_string` | `stormpy.parse_jani_model_from_string` |  |
| `stormpy.parse_prism_program` | `stormpy.parse_prism_program` |  |
| `stormpy.parse_properties` | `stormpy.parse_properties` |  |
| `stormpy.parse_properties_for_jani_model` | `stormpy.developer.parse_properties_for_jani_model` |  |
| `stormpy.parse_properties_for_prism_program` | `stormpy.developer.parse_properties_for_prism_program` |  |
| `stormpy.parse_properties_without_context` | `stormpy.logic.parse_properties` | Use parse_properties without a context. |
| `stormpy.perform_bisimulation` | `stormpy.transformations.perform_bisimulation` | Sparse and symbolic wrappers unified; bisimulation_type, options and quotient_format are keyword-only. Sparse options use BisimulationOptions; raw DD options remain developer.DdBisimulationOptions. |
| `stormpy.perform_sparse_bisimulation` | `stormpy.transformations.perform_bisimulation` | Unified wrapper; configure options instead of the v1 positional parameters. Sparse and symbolic wrappers unified; bisimulation_type, options and quotient_format are keyword-only. Sparse options use BisimulationOptions; raw DD options remain developer.DdBisimulationOptions. |
| `stormpy.perform_symbolic_bisimulation` | `stormpy.transformations.perform_bisimulation` | Unified wrapper; configure options instead of the v1 positional parameters. Sparse and symbolic wrappers unified; bisimulation_type, options and quotient_format are keyword-only. Sparse options use BisimulationOptions; raw DD options remain developer.DdBisimulationOptions. |
| `stormpy.pomdp.BeliefExplorationModelCheckerDouble` | **Removed: no direct export** | Removed class binding. Use stormpy.pomdp.verify_with_belief_unfolding or verify_with_belief_discretization; no direct class replacement. |
| `stormpy.pomdp.BeliefExplorationModelCheckerOptionsDouble` | `stormpy.pomdp.developer.BeliefBasedModelCheckerOptions[float]` | Renamed and revised options. |
| `stormpy.pomdp.BeliefExplorationPomdpModelCheckerResultDouble` | `stormpy.pomdp.BeliefBasedModelCheckerResult[float]` | Renamed and revised result. |
| `stormpy.pomdp.BeliefMdpExplorerDouble` | **Removed: no direct export** | Removed class binding; no direct exported equivalent. |
| `stormpy.pomdp.BeliefSupportTrackerDouble` | `stormpy.pomdp.BeliefSupportTracker[float]` | Becomes a template. |
| `stormpy.pomdp.BeliefSupportTrackerExact` | `stormpy.pomdp.BeliefSupportTracker[stormpy.Rational]` | Becomes a template. |
| `stormpy.pomdp.BeliefSupportWinningRegion` | `stormpy.pomdp.WinningRegion` | Renamed. |
| `stormpy.pomdp.BeliefSupportWinningRegionQueryInterfaceDouble` | `stormpy.pomdp.WinningRegionQueryInterface[float]` | Renamed generic family. |
| `stormpy.pomdp.GenerateMonitorVerifierDouble` | `stormpy.pomdp.developer.GenerateMonitorVerifier[float]` | Becomes a template. |
| `stormpy.pomdp.GenerateMonitorVerifierDoubleOptions` | `stormpy.pomdp.developer.GenerateMonitorVerifierOptions[float]` | Generic type parameter replaces embedded type suffix. |
| `stormpy.pomdp.GenerateMonitorVerifierExact` | `stormpy.pomdp.developer.GenerateMonitorVerifier[stormpy.Rational]` | Becomes a template. |
| `stormpy.pomdp.GenerateMonitorVerifierExactOptions` | `stormpy.pomdp.developer.GenerateMonitorVerifierOptions[stormpy.Rational]` | Generic type parameter replaces embedded type suffix. |
| `stormpy.pomdp.IterativeQualitativeSearchOptions` | `stormpy.pomdp.developer.MemlessSearchOptions` | Renamed and revised options. |
| `stormpy.pomdp.IterativeQualitativeSearchSolverDouble` | `stormpy.pomdp.IterativePolicySearch[float]` | Renamed and revised policy search interface. |
| `stormpy.pomdp.MonitorVerifierDouble` | `stormpy.pomdp.MonitorVerifier[float]` | Becomes a template. |
| `stormpy.pomdp.MonitorVerifierExact` | `stormpy.pomdp.MonitorVerifier[stormpy.Rational]` | Becomes a template. |
| `stormpy.pomdp.NondeterministicBeliefTrackerDoubleSparse` | `stormpy.pomdp.NondeterministicBeliefTracker[float]` | Renamed generic family. |
| `stormpy.pomdp.NondeterministicBeliefTrackerDoubleSparseOptions` | `stormpy.pomdp.developer.NondeterministicBeliefTrackerOptions[float]` | Renamed generic family. |
| `stormpy.pomdp.NondeterministicBeliefTrackerExactSparse` | `stormpy.pomdp.NondeterministicBeliefTracker[stormpy.Rational]` | Renamed generic family. |
| `stormpy.pomdp.NondeterministicBeliefTrackerExactSparseOptions` | `stormpy.pomdp.developer.NondeterministicBeliefTrackerOptions[stormpy.Rational]` | Renamed generic family. |
| `stormpy.pomdp.ObservationTraceUnfolderDouble` | `stormpy.pomdp.ObservationTraceUnfolder[float]` | Becomes a template. |
| `stormpy.pomdp.ObservationTraceUnfolderExact` | `stormpy.pomdp.ObservationTraceUnfolder[stormpy.Rational]` | Becomes a template. |
| `stormpy.pomdp.ObservationTraceUnfolderOptions` | `stormpy.pomdp.developer.ObservationTraceUnfolderOptions` |  |
| `stormpy.pomdp.ObservationTraceUnfolderRf` | `stormpy.pomdp.ObservationTraceUnfolder[stormpy.RationalFunction]` | Becomes a template. |
| `stormpy.pomdp.PomdpFscApplicationMode` | `stormpy.pomdp.PomdpFscApplicationMode` |  |
| `stormpy.pomdp.PomdpMemory` | `stormpy.pomdp.PomdpMemory` |  |
| `stormpy.pomdp.PomdpMemoryBuilder` | `stormpy.pomdp.developer.PomdpMemoryBuilder` |  |
| `stormpy.pomdp.PomdpMemoryPattern` | `stormpy.pomdp.PomdpMemoryPattern` |  |
| `stormpy.pomdp.SparseBeliefStateDouble` | `stormpy.pomdp.SparseBeliefState[float]` | Becomes a template. |
| `stormpy.pomdp.SparseBeliefStateExact` | `stormpy.pomdp.SparseBeliefState[stormpy.Rational]` | Becomes a template. |
| `stormpy.pomdp.apply_unknown_fsc` | `stormpy.pomdp.apply_unknown_fsc` |  |
| `stormpy.pomdp.create_interactive_mc` | **Removed: no direct export** | Removed binding; no direct exported equivalent. |
| `stormpy.pomdp.create_iterative_qualitative_search_solver_Double` | `stormpy.pomdp.developer.create_iterative_policy_search` | Revised raw factory; see public create_iterative_policy_search. |
| `stormpy.pomdp.create_nondeterminstic_belief_tracker` | `stormpy.pomdp.create_nondeterministic_belief_tracker` | Fixed nondeterminstic spelling; timeouts are keyword-only. |
| `stormpy.pomdp.create_observation_trace_unfolder` | `stormpy.pomdp.create_observation_trace_unfolder` | risk_assessment/expr_manager are now risk/expression_manager; public options are exposed as use_restart_semantics=... . |
| `stormpy.pomdp.make_canonic` | `stormpy.pomdp.make_canonic` |  |
| `stormpy.pomdp.make_simple` | `stormpy.pomdp.make_simple` | keep_state_valuations is keyword-only. |
| `stormpy.pomdp.prepare_pomdp_for_qualitative_search_Double` | `stormpy.pomdp.prepare_for_qualitative_search` | Public wrapper takes model and property. |
| `stormpy.pomdp.unfold_memory` | `stormpy.pomdp.unfold_memory` | add_memory_labels and keep_state_valuations are keyword-only. |
| `stormpy.preprocess_symbolic_input` | `stormpy.instantiate_constants` | Use instantiate_constants(model, constant_definitions, properties); returns (instantiated model, instantiated properties). The input model kind is preserved. |
| `stormpy.prob01max_states` | `stormpy.analysis.compute_prob01_states` | Unified wrapper takes a property; use Pmin or Pmax in that property. Raw bitvector API: developer.perform_prob01_min / perform_prob01_max. Changed from (model, phi_states, psi_states) to (model, property). Raw bitvector API remains at developer.perform_prob01 / perform_prob01_min / perform_prob01_max. |
| `stormpy.prob01min_states` | `stormpy.analysis.compute_prob01_states` | Unified wrapper takes a property; use Pmin or Pmax in that property. Raw bitvector API: developer.perform_prob01_min / perform_prob01_max. Changed from (model, phi_states, psi_states) to (model, property). Raw bitvector API remains at developer.perform_prob01 / perform_prob01_min / perform_prob01_max. |
| `stormpy.product_model`<br>`stormpy.storage.product_model` | `stormpy.models.MemoryStructure.product_model` | Use memory.product_model(model); no module-level function. |
| `stormpy.pycarl.BoundType` | `stormpy.numbers.developer.BoundType` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.Interval` | `stormpy.numbers.developer.Interval` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.Monomial` | `stormpy.numbers.developer.Monomial` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.NoPicklingSupport` | `stormpy.numbers.developer.NoPicklingSupport` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.Variable` | `stormpy.numbers.developer.Variable` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.VariableType` | `stormpy.numbers.developer.VariableType` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.abs` | `stormpy.numbers.developer.abs` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.carl_version` | `stormpy.numbers.developer.carl_version` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.ceil` | `stormpy.numbers.developer.ceil` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.clear_monomial_pool` | `stormpy.numbers.developer.clear_monomial_pool` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.clear_pools` | `stormpy.numbers.developer.clear_pools` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.clear_variable_pool` | `stormpy.numbers.developer.clear_variable_pool` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.cln.Factorization` | `stormpy.numbers.developer.cln.Factorization` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.cln.FactorizedPolynomial` | `stormpy.numbers.developer.cln.FactorizedPolynomial` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.cln.FactorizedRationalFunction` | `stormpy.numbers.developer.cln.FactorizedRationalFunction` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.cln.Integer` | `stormpy.numbers.developer.cln.Integer` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.cln.Interval` | `stormpy.numbers.developer.cln.Interval` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.cln.Polynomial` | `stormpy.numbers.developer.cln.Polynomial` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.cln.Rational` | `stormpy.numbers.developer.cln.Rational` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.cln.RationalFunction` | `stormpy.numbers.developer.cln.RationalFunction` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.cln.Term` | `stormpy.numbers.developer.cln.Term` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.cln.abs` | `stormpy.numbers.developer.cln.abs` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.cln.ceil` | `stormpy.numbers.developer.cln.ceil` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.cln.create_factorized_polynomial` | `stormpy.numbers.developer.cln.create_factorized_polynomial` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.cln.denominator` | `stormpy.numbers.developer.cln.denominator` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.cln.div` | `stormpy.numbers.developer.cln.div` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.cln.expand` | `stormpy.numbers.developer.cln.expand` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.cln.factorization_cache` | `stormpy.numbers.developer.cln.factorization_cache` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.cln.floor` | `stormpy.numbers.developer.cln.floor` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.cln.formula.Constraint` | `stormpy.numbers.developer.cln.formula.Constraint` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.cln.formula.Formula` | `stormpy.numbers.developer.cln.formula.Formula` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.cln.formula.SimpleConstraint` | `stormpy.numbers.developer.cln.formula.SimpleConstraint` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.cln.formula.SimpleConstraintRatFunc` | `stormpy.numbers.developer.cln.formula.SimpleConstraintRatFunc` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.cln.isInteger` | `stormpy.numbers.developer.cln.isInteger` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.cln.numerator` | `stormpy.numbers.developer.cln.numerator` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.cln.pow` | `stormpy.numbers.developer.cln.pow` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.cln.quotient` | `stormpy.numbers.developer.cln.quotient` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.convert.convert_to_cln` | `stormpy.numbers.developer.convert.convert_to_cln` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.convert.convert_to_gmp` | `stormpy.numbers.developer.convert.convert_to_gmp` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.create_monomial` | `stormpy.numbers.developer.create_monomial` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.div` | `stormpy.numbers.developer.div` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.floor` | `stormpy.numbers.developer.floor` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.formula.FormulaType` | `stormpy.numbers.developer.formula.FormulaType` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.formula.Relation` | `stormpy.numbers.developer.formula.Relation` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.gmp.Factorization` | `stormpy.numbers.developer.gmp.Factorization` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.gmp.FactorizedPolynomial` | `stormpy.numbers.developer.gmp.FactorizedPolynomial` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.gmp.FactorizedRationalFunction` | `stormpy.numbers.developer.gmp.FactorizedRationalFunction` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.gmp.Integer` | `stormpy.numbers.developer.gmp.Integer` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.gmp.Interval` | `stormpy.numbers.developer.gmp.Interval` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.gmp.Polynomial` | `stormpy.numbers.developer.gmp.Polynomial` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.gmp.Rational` | `stormpy.numbers.developer.gmp.Rational` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.gmp.RationalFunction` | `stormpy.numbers.developer.gmp.RationalFunction` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.gmp.Term` | `stormpy.numbers.developer.gmp.Term` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.gmp.abs` | `stormpy.numbers.developer.gmp.abs` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.gmp.ceil` | `stormpy.numbers.developer.gmp.ceil` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.gmp.create_factorized_polynomial` | `stormpy.numbers.developer.gmp.create_factorized_polynomial` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.gmp.denominator` | `stormpy.numbers.developer.gmp.denominator` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.gmp.div` | `stormpy.numbers.developer.gmp.div` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.gmp.expand` | `stormpy.numbers.developer.gmp.expand` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.gmp.factorization_cache` | `stormpy.numbers.developer.gmp.factorization_cache` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.gmp.floor` | `stormpy.numbers.developer.gmp.floor` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.gmp.formula.Constraint` | `stormpy.numbers.developer.gmp.formula.Constraint` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.gmp.formula.Formula` | `stormpy.numbers.developer.gmp.formula.Formula` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.gmp.formula.SimpleConstraint` | `stormpy.numbers.developer.gmp.formula.SimpleConstraint` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.gmp.formula.SimpleConstraintRatFunc` | `stormpy.numbers.developer.gmp.formula.SimpleConstraintRatFunc` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.gmp.isInteger` | `stormpy.numbers.developer.gmp.isInteger` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.gmp.numerator` | `stormpy.numbers.developer.gmp.numerator` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.gmp.pow` | `stormpy.numbers.developer.gmp.pow` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.gmp.quotient` | `stormpy.numbers.developer.gmp.quotient` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.has_cln` | `stormpy.numbers.developer.has_cln` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.inf` | `stormpy.numbers.developer.inf` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.infinity.Infinity` | `stormpy.numbers.developer.infinity.Infinity` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.isInteger` | `stormpy.numbers.developer.isInteger` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.parse.ParserError` | `stormpy.numbers.developer.parse.ParserError` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.parse.deserialize` | `stormpy.numbers.developer.parse.deserialize` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.pow` | `stormpy.numbers.developer.pow` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.quotient` | `stormpy.numbers.developer.quotient` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.pycarl.variable_with_name` | `stormpy.numbers.developer.variable_with_name` | Numeric binding namespace moved; backend type names retain their meaning. |
| `stormpy.reset_timeout` | `stormpy.developer.reset_timeout_alarm` | Renamed raw binding. |
| `stormpy.set_loglevel_debug` | `stormpy.developer.set_log_level` | Pass stormpy.developer.LogLevel.DEBUG. |
| `stormpy.set_loglevel_error` | `stormpy.developer.set_log_level` | Pass stormpy.developer.LogLevel.ERROR. |
| `stormpy.set_loglevel_trace` | `stormpy.developer.set_log_level` | Pass stormpy.developer.LogLevel.TRACE. |
| `stormpy.set_settings` | `stormpy.developer.set_from_exploded_string` | Legacy raw settings entry point; prefer environments. |
| `stormpy.set_state_valuations` | `stormpy.transformations.set_state_valuations` |  |
| `stormpy.set_timeout` | `stormpy.developer.set_timeout_alarm` | Renamed raw binding. |
| `stormpy.simulator.PrismSimulator` | `stormpy.simulator.PrismSimulator` | Module and exported name retained; inspect v2 method signatures. |
| `stormpy.simulator.Simulator` | `stormpy.simulator.Simulator` | Module and exported name retained; inspect v2 method signatures. |
| `stormpy.simulator.SimulatorActionMode` | `stormpy.simulator.SimulatorActionMode` | Module and exported name retained; inspect v2 method signatures. |
| `stormpy.simulator.SimulatorObservationMode` | `stormpy.simulator.SimulatorObservationMode` | Module and exported name retained; inspect v2 method signatures. |
| `stormpy.simulator.SparseSimulator` | `stormpy.simulator.SparseSimulator` | Module and exported name retained; inspect v2 method signatures. |
| `stormpy.simulator.create_simulator` | `stormpy.simulator.create_simulator` | Module and exported name retained; inspect v2 method signatures. |
| `stormpy.sparse_model_from_umb`<br>`stormpy.storage.sparse_model_from_umb` | `stormpy.developer.storage.sparse_model_from_umb` |  |
| `stormpy.sparse_model_to_umb`<br>`stormpy.storage.sparse_model_to_umb` | `stormpy.io.sparse_model_to_umb` |  |
| `stormpy.storage.umb_to_archive`<br>`stormpy.umb_to_archive` | `stormpy.io.umb_to_archive` |  |
| `stormpy.topological_sort` | `stormpy.analysis.topological_sort` | forward and initial are keyword-only. |
| `stormpy.transform_to_discrete_time_model` | `stormpy.transformations.transform_to_discrete_time_model` |  |
| `stormpy.transform_to_sparse_model` | `stormpy.transformations.transform_to_sparse_model` |  |
| `stormpy.utility.JsonContainerDouble` | `stormpy.datastructures.JsonContainer[float]` | Becomes a template. |
| `stormpy.utility.JsonContainerRational` | `stormpy.datastructures.JsonContainer[stormpy.Rational]` | Becomes a template. |
| `stormpy.utility.MatrixFormat` | `stormpy.developer.utility.MatrixFormat` |  |
| `stormpy.utility.ModelReference` | `stormpy.developer.ModelReference` |  |
| `stormpy.utility.Path` | `stormpy.analysis.Path[float]` | Becomes a template. |
| `stormpy.utility.ShortestPathsGenerator` | `stormpy.developer.utility.ShortestPathsGenerator[float]` | Becomes a template. |
| `stormpy.utility.SmtCheckResult` | `stormpy.developer.SmtCheckResult` |  |
| `stormpy.utility.SmtSolver` | `stormpy.developer.SmtSolver` |  |
| `stormpy.utility.SmtSolverFactory` | `stormpy.developer.SmtSolverFactory` |  |
| `stormpy.utility.Z3SmtSolver` | `stormpy.developer.Z3SmtSolver` |  |
| `stormpy.utility.Z3SmtSolverFactory` | `stormpy.developer.Z3SmtSolverFactory` |  |
| `stormpy.utility.milliseconds` | `stormpy.developer.utility.milliseconds` |  |
| `stormpy.utility.multiobjective_plotting.plot_convex_pareto_curve_demo` | `stormpy.plotting.plot_convex_pareto_curve_demo` | Plotting module moved; requires optional plotting dependencies. |
| `stormpy.utility.multiobjective_plotting.prepare_multiobjective_result_for_plotting` | `stormpy.plotting.prepare_multiobjective_result_for_plotting` | Plotting module moved; requires optional plotting dependencies. |
| `stormpy.utility.sharpen` | `stormpy.developer.utility.sharpen` |  |

## Enum-member changes

| v1 member(s) | v2 member |
| --- | --- |
| `stormpy.BinaryBooleanOperatorType.AND` | `stormpy.logic.BinaryBooleanOperatorType.AND` |
| `stormpy.BinaryBooleanOperatorType.OR` | `stormpy.logic.BinaryBooleanOperatorType.OR` |
| `stormpy.BisimulationType.STRONG` | `stormpy.transformations.BisimulationType.STRONG` |
| `stormpy.BisimulationType.WEAK` | `stormpy.transformations.BisimulationType.WEAK` |
| `stormpy.ComparisonType.GEQ` | `stormpy.logic.ComparisonType.GEQ` |
| `stormpy.ComparisonType.GREATER` | `stormpy.logic.ComparisonType.GREATER` |
| `stormpy.ComparisonType.LEQ` | `stormpy.logic.ComparisonType.LEQ` |
| `stormpy.ComparisonType.LESS` | `stormpy.logic.ComparisonType.LESS` |
| `stormpy.storage.CompressionMode.Default`<br>`stormpy.CompressionMode.Default` | `stormpy.io.CompressionMode.DEFAULT` |
| `stormpy.storage.CompressionMode.Gzip`<br>`stormpy.CompressionMode.Gzip` | `stormpy.io.CompressionMode.GZIP` |
| `stormpy.storage.CompressionMode.NoCompression`<br>`stormpy.CompressionMode.NoCompression` | `stormpy.io.CompressionMode.NO_COMPRESSION` |
| `stormpy.storage.CompressionMode.Xz`<br>`stormpy.CompressionMode.Xz` | `stormpy.io.CompressionMode.XZ` |
| `stormpy.ConditionalAlgorithmSetting.bisection` | `stormpy.environments.ConditionalAlgorithmSetting.BISECTION` |
| `stormpy.ConditionalAlgorithmSetting.bisection_advanced` | `stormpy.environments.ConditionalAlgorithmSetting.BISECTION_ADVANCED` |
| `stormpy.ConditionalAlgorithmSetting.bisection_advanced_pt` | `stormpy.environments.ConditionalAlgorithmSetting.BISECTION_ADVANCED_PT` |
| `stormpy.ConditionalAlgorithmSetting.bisection_pt` | `stormpy.environments.ConditionalAlgorithmSetting.BISECTION_PT` |
| `stormpy.ConditionalAlgorithmSetting.default` | `stormpy.environments.ConditionalAlgorithmSetting.DEFAULT` |
| `stormpy.ConditionalAlgorithmSetting.policy_iteration` | `stormpy.environments.ConditionalAlgorithmSetting.POLICY_ITERATION` |
| `stormpy.ConditionalAlgorithmSetting.restart` | `stormpy.environments.ConditionalAlgorithmSetting.RESTART` |
| `stormpy.CuddReorderingTechnique.ANNEALING` | `stormpy.environments.CuddReorderingTechnique.ANNEALING` |
| `stormpy.CuddReorderingTechnique.EXACT` | `stormpy.environments.CuddReorderingTechnique.EXACT` |
| `stormpy.CuddReorderingTechnique.GENETIC` | `stormpy.environments.CuddReorderingTechnique.GENETIC` |
| `stormpy.CuddReorderingTechnique.GROUP_SIFT` | `stormpy.environments.CuddReorderingTechnique.GROUP_SIFT` |
| `stormpy.CuddReorderingTechnique.GROUP_SIFT_CONV` | `stormpy.environments.CuddReorderingTechnique.GROUP_SIFT_CONV` |
| `stormpy.CuddReorderingTechnique.NONE` | `stormpy.environments.CuddReorderingTechnique.NONE` |
| `stormpy.CuddReorderingTechnique.RANDOM` | `stormpy.environments.CuddReorderingTechnique.RANDOM` |
| `stormpy.CuddReorderingTechnique.RANDOM_PIVOT` | `stormpy.environments.CuddReorderingTechnique.RANDOM_PIVOT` |
| `stormpy.CuddReorderingTechnique.SIFT` | `stormpy.environments.CuddReorderingTechnique.SIFT` |
| `stormpy.CuddReorderingTechnique.SIFT_CONV` | `stormpy.environments.CuddReorderingTechnique.SIFT_CONV` |
| `stormpy.CuddReorderingTechnique.SYMMETRIC_SIFT` | `stormpy.environments.CuddReorderingTechnique.SYMMETRIC_SIFT` |
| `stormpy.CuddReorderingTechnique.SYMMETRIC_SIFT_CONV` | `stormpy.environments.CuddReorderingTechnique.SYMMETRIC_SIFT_CONV` |
| `stormpy.CuddReorderingTechnique.WIN2` | `stormpy.environments.CuddReorderingTechnique.WIN2` |
| `stormpy.CuddReorderingTechnique.WIN2_CONV` | `stormpy.environments.CuddReorderingTechnique.WIN2_CONV` |
| `stormpy.CuddReorderingTechnique.WIN3` | `stormpy.environments.CuddReorderingTechnique.WIN3` |
| `stormpy.CuddReorderingTechnique.WIN3_CONV` | `stormpy.environments.CuddReorderingTechnique.WIN3_CONV` |
| `stormpy.CuddReorderingTechnique.WIN4` | `stormpy.environments.CuddReorderingTechnique.WIN4` |
| `stormpy.CuddReorderingTechnique.WIN4_CONV` | `stormpy.environments.CuddReorderingTechnique.WIN4_CONV` |
| `stormpy.storage.DdMetaVariableType.Bitvector`<br>`stormpy.DdMetaVariableType.Bitvector` | `stormpy.developer.storage.DdMetaVariableType.BITVECTOR` |
| `stormpy.storage.DdMetaVariableType.Bool`<br>`stormpy.DdMetaVariableType.Bool` | `stormpy.developer.storage.DdMetaVariableType.BOOL` |
| `stormpy.storage.DdMetaVariableType.Int`<br>`stormpy.DdMetaVariableType.Int` | `stormpy.developer.storage.DdMetaVariableType.INT` |
| `stormpy.EliminationLabelBehavior.DELETE_LABELS` | `stormpy.transformations.EliminationLabelBehavior.DELETE_LABELS` |
| `stormpy.EliminationLabelBehavior.KEEP_LABELS` | `stormpy.transformations.EliminationLabelBehavior.KEEP_LABELS` |
| `stormpy.EliminationLabelBehavior.MERGE_LABELS` | `stormpy.transformations.EliminationLabelBehavior.MERGE_LABELS` |
| `stormpy.EquationSolverType.eigen` | `stormpy.environments.EquationSolverType.EIGEN` |
| `stormpy.EquationSolverType.elimination` | `stormpy.environments.EquationSolverType.ELIMINATION` |
| `stormpy.EquationSolverType.gmmxx` | `stormpy.environments.EquationSolverType.GMMXX` |
| `stormpy.EquationSolverType.native` | `stormpy.environments.EquationSolverType.NATIVE` |
| `stormpy.EquationSolverType.topological` | `stormpy.environments.EquationSolverType.TOPOLOGICAL` |
| `stormpy.ExplorationOrder.BFS` | `stormpy.developer.ExplorationOrder.BFS` |
| `stormpy.ExplorationOrder.DFS` | `stormpy.developer.ExplorationOrder.DFS` |
| `stormpy.JaniModelType.CTMC` | `stormpy.io.JaniModelType.CTMC` |
| `stormpy.JaniModelType.CTMDP` | `stormpy.io.JaniModelType.CTMDP` |
| `stormpy.JaniModelType.DTMC` | `stormpy.io.JaniModelType.DTMC` |
| `stormpy.JaniModelType.HA` | `stormpy.io.JaniModelType.HA` |
| `stormpy.JaniModelType.LTS` | `stormpy.io.JaniModelType.LTS` |
| `stormpy.JaniModelType.MA` | `stormpy.io.JaniModelType.MA` |
| `stormpy.JaniModelType.MDP` | `stormpy.io.JaniModelType.MDP` |
| `stormpy.JaniModelType.PHA` | `stormpy.io.JaniModelType.PHA` |
| `stormpy.JaniModelType.PTA` | `stormpy.io.JaniModelType.PTA` |
| `stormpy.JaniModelType.SHA` | `stormpy.io.JaniModelType.SHA` |
| `stormpy.JaniModelType.STA` | `stormpy.io.JaniModelType.STA` |
| `stormpy.JaniModelType.TA` | `stormpy.io.JaniModelType.TA` |
| `stormpy.JaniModelType.UNDEFINED` | `stormpy.io.JaniModelType.UNDEFINED` |
| `stormpy.MinMaxMethod.interval_iteration` | `stormpy.environments.MinMaxMethod.INTERVAL_ITERATION` |
| `stormpy.MinMaxMethod.linear_programming` | `stormpy.environments.MinMaxMethod.LINEAR_PROGRAMMING` |
| `stormpy.MinMaxMethod.optimistic_value_iteration` | `stormpy.environments.MinMaxMethod.OPTIMISTIC_VALUE_ITERATION` |
| `stormpy.MinMaxMethod.policy_iteration` | `stormpy.environments.MinMaxMethod.POLICY_ITERATION` |
| `stormpy.MinMaxMethod.rational_search` | `stormpy.environments.MinMaxMethod.RATIONAL_SEARCH` |
| `stormpy.MinMaxMethod.sound_value_iteration` | `stormpy.environments.MinMaxMethod.SOUND_VALUE_ITERATION` |
| `stormpy.MinMaxMethod.topological` | `stormpy.environments.MinMaxMethod.TOPOLOGICAL` |
| `stormpy.MinMaxMethod.value_iteration` | `stormpy.environments.MinMaxMethod.VALUE_ITERATION` |
| `stormpy.storage.ModelType.CTMC`<br>`stormpy.ModelType.CTMC` | `stormpy.models.ModelType.CTMC` |
| `stormpy.storage.ModelType.DTMC`<br>`stormpy.ModelType.DTMC` | `stormpy.models.ModelType.DTMC` |
| `stormpy.storage.ModelType.MA`<br>`stormpy.ModelType.MA` | `stormpy.models.ModelType.MA` |
| `stormpy.storage.ModelType.MDP`<br>`stormpy.ModelType.MDP` | `stormpy.models.ModelType.MDP` |
| `stormpy.storage.ModelType.POMDP`<br>`stormpy.ModelType.POMDP` | `stormpy.models.ModelType.POMDP` |
| `stormpy.storage.ModelType.SMG`<br>`stormpy.ModelType.SMG` | `stormpy.models.ModelType.SMG` |
| `stormpy.MultiObjectiveEncodingType.auto` | `stormpy.environments.MultiObjectiveEncodingType.AUTO` |
| `stormpy.MultiObjectiveEncodingType.classic` | `stormpy.environments.MultiObjectiveEncodingType.CLASSIC` |
| `stormpy.MultiObjectiveEncodingType.flow` | `stormpy.environments.MultiObjectiveEncodingType.FLOW` |
| `stormpy.MultiObjectiveMethod.constraint_based` | `stormpy.environments.MultiObjectiveMethod.CONSTRAINT_BASED` |
| `stormpy.MultiObjectiveMethod.pcaa` | `stormpy.environments.MultiObjectiveMethod.PCAA` |
| `stormpy.MultiObjectivePrecisionType.absolute` | `stormpy.environments.MultiObjectivePrecisionType.ABSOLUTE` |
| `stormpy.MultiObjectivePrecisionType.relative_to_diff` | `stormpy.environments.MultiObjectivePrecisionType.RELATIVE_TO_DIFF` |
| `stormpy.NativeLinearEquationSolverMethod.SOR` | `stormpy.environments.NativeLinearEquationSolverMethod.SOR` |
| `stormpy.NativeLinearEquationSolverMethod.gauss_seidel` | `stormpy.environments.NativeLinearEquationSolverMethod.GAUSS_SEIDEL` |
| `stormpy.NativeLinearEquationSolverMethod.interval_iteration` | `stormpy.environments.NativeLinearEquationSolverMethod.INTERVAL_ITERATION` |
| `stormpy.NativeLinearEquationSolverMethod.jacobi` | `stormpy.environments.NativeLinearEquationSolverMethod.JACOBI` |
| `stormpy.NativeLinearEquationSolverMethod.optimistic_value_iteration` | `stormpy.environments.NativeLinearEquationSolverMethod.OPTIMISTIC_VALUE_ITERATION` |
| `stormpy.NativeLinearEquationSolverMethod.power_iteration` | `stormpy.environments.NativeLinearEquationSolverMethod.POWER` |
| `stormpy.NativeLinearEquationSolverMethod.rational_search` | `stormpy.environments.NativeLinearEquationSolverMethod.RATIONAL_SEARCH` |
| `stormpy.NativeLinearEquationSolverMethod.sound_value_iteration` | `stormpy.environments.NativeLinearEquationSolverMethod.SOUND_VALUE_ITERATION` |
| `stormpy.NativeLinearEquationSolverMethod.walker_chae` | `stormpy.environments.NativeLinearEquationSolverMethod.WALKER_CHAE` |
| `stormpy.storage.OperatorType.And`<br>`stormpy.OperatorType.And` | `stormpy.expressions.OperatorType.AND` |
| `stormpy.storage.OperatorType.Ceil`<br>`stormpy.OperatorType.Ceil` | `stormpy.expressions.OperatorType.CEIL` |
| `stormpy.storage.OperatorType.Divide`<br>`stormpy.OperatorType.Divide` | `stormpy.expressions.OperatorType.DIVIDE` |
| `stormpy.storage.OperatorType.Equal`<br>`stormpy.OperatorType.Equal` | `stormpy.expressions.OperatorType.EQUAL` |
| `stormpy.storage.OperatorType.Floor`<br>`stormpy.OperatorType.Floor` | `stormpy.expressions.OperatorType.FLOOR` |
| `stormpy.storage.OperatorType.Greater`<br>`stormpy.OperatorType.Greater` | `stormpy.expressions.OperatorType.GREATER` |
| `stormpy.storage.OperatorType.GreaterOrEqual`<br>`stormpy.OperatorType.GreaterOrEqual` | `stormpy.expressions.OperatorType.GREATER_OR_EQUAL` |
| `stormpy.storage.OperatorType.Iff`<br>`stormpy.OperatorType.Iff` | `stormpy.expressions.OperatorType.IFF` |
| `stormpy.storage.OperatorType.Implies`<br>`stormpy.OperatorType.Implies` | `stormpy.expressions.OperatorType.IMPLIES` |
| `stormpy.storage.OperatorType.Ite`<br>`stormpy.OperatorType.Ite` | `stormpy.expressions.OperatorType.ITE` |
| `stormpy.storage.OperatorType.Less`<br>`stormpy.OperatorType.Less` | `stormpy.expressions.OperatorType.LESS` |
| `stormpy.storage.OperatorType.LessOrEqual`<br>`stormpy.OperatorType.LessOrEqual` | `stormpy.expressions.OperatorType.LESS_OR_EQUAL` |
| `stormpy.storage.OperatorType.Max`<br>`stormpy.OperatorType.Max` | `stormpy.expressions.OperatorType.MAX` |
| `stormpy.storage.OperatorType.Min`<br>`stormpy.OperatorType.Min` | `stormpy.expressions.OperatorType.MIN` |
| `stormpy.storage.OperatorType.Minus`<br>`stormpy.OperatorType.Minus` | `stormpy.expressions.OperatorType.MINUS` |
| `stormpy.storage.OperatorType.Modulo`<br>`stormpy.OperatorType.Modulo` | `stormpy.expressions.OperatorType.MODULO` |
| `stormpy.storage.OperatorType.Not`<br>`stormpy.OperatorType.Not` | `stormpy.expressions.OperatorType.NOT` |
| `stormpy.storage.OperatorType.NotEqual`<br>`stormpy.OperatorType.NotEqual` | `stormpy.expressions.OperatorType.NOT_EQUAL` |
| `stormpy.storage.OperatorType.Or`<br>`stormpy.OperatorType.Or` | `stormpy.expressions.OperatorType.OR` |
| `stormpy.storage.OperatorType.Plus`<br>`stormpy.OperatorType.Plus` | `stormpy.expressions.OperatorType.PLUS` |
| `stormpy.storage.OperatorType.Power`<br>`stormpy.OperatorType.Power` | `stormpy.expressions.OperatorType.POWER` |
| `stormpy.storage.OperatorType.Times`<br>`stormpy.OperatorType.Times` | `stormpy.expressions.OperatorType.TIMES` |
| `stormpy.storage.OperatorType.Xor`<br>`stormpy.OperatorType.Xor` | `stormpy.expressions.OperatorType.XOR` |
| `stormpy.OptimizationDirection.Maximize` | `stormpy.logic.OptimizationDirection.MAXIMIZE` |
| `stormpy.OptimizationDirection.Minimize` | `stormpy.logic.OptimizationDirection.MINIMIZE` |
| `stormpy.storage.PrismModelType.CTMC`<br>`stormpy.PrismModelType.CTMC` | `stormpy.io.PrismModelType.CTMC` |
| `stormpy.storage.PrismModelType.CTMDP`<br>`stormpy.PrismModelType.CTMDP` | `stormpy.io.PrismModelType.CTMDP` |
| `stormpy.storage.PrismModelType.DTMC`<br>`stormpy.PrismModelType.DTMC` | `stormpy.io.PrismModelType.DTMC` |
| `stormpy.storage.PrismModelType.MA`<br>`stormpy.PrismModelType.MA` | `stormpy.io.PrismModelType.MA` |
| `stormpy.storage.PrismModelType.MDP`<br>`stormpy.PrismModelType.MDP` | `stormpy.io.PrismModelType.MDP` |
| `stormpy.storage.PrismModelType.POMDP`<br>`stormpy.PrismModelType.POMDP` | `stormpy.io.PrismModelType.POMDP` |
| `stormpy.storage.PrismModelType.UNDEFINED`<br>`stormpy.PrismModelType.UNDEFINED` | `stormpy.io.PrismModelType.UNDEFINED` |
| `stormpy.QuotientFormat.DD` | `stormpy.transformations.QuotientFormat.DD` |
| `stormpy.QuotientFormat.SPARSE` | `stormpy.transformations.QuotientFormat.SPARSE` |
| `stormpy.SchedulerMemoryPattern.arbitrary` | `stormpy.developer.SchedulerMemoryPattern.ARBITRARY` |
| `stormpy.SchedulerMemoryPattern.counter` | `stormpy.developer.SchedulerMemoryPattern.COUNTER` |
| `stormpy.SchedulerMemoryPattern.goal_memory` | `stormpy.developer.SchedulerMemoryPattern.GOAL_MEMORY` |
| `stormpy.SteadyStateDistributionAlgorithm.automatic` | `stormpy.environments.SteadyStateDistributionAlgorithm.AUTOMATIC` |
| `stormpy.SteadyStateDistributionAlgorithm.classic` | `stormpy.environments.SteadyStateDistributionAlgorithm.CLASSIC` |
| `stormpy.SteadyStateDistributionAlgorithm.equation_system` | `stormpy.environments.SteadyStateDistributionAlgorithm.EQUATION_SYSTEM` |
| `stormpy.SteadyStateDistributionAlgorithm.expected_visiting_times` | `stormpy.environments.SteadyStateDistributionAlgorithm.EXPECTED_VISITING_TIMES` |
| `stormpy.storage.UmbExportValueType.Default`<br>`stormpy.UmbExportValueType.Default` | `stormpy.io.UmbExportValueType.DEFAULT` |
| `stormpy.storage.UmbExportValueType.Double`<br>`stormpy.UmbExportValueType.Double` | `stormpy.io.UmbExportValueType.DOUBLE` |
| `stormpy.storage.UmbExportValueType.DoubleInterval`<br>`stormpy.UmbExportValueType.DoubleInterval` | `stormpy.io.UmbExportValueType.DOUBLE_INTERVAL` |
| `stormpy.storage.UmbExportValueType.Rational`<br>`stormpy.UmbExportValueType.Rational` | `stormpy.io.UmbExportValueType.RATIONAL` |
| `stormpy.storage.UmbExportValueType.RationalInterval`<br>`stormpy.UmbExportValueType.RationalInterval` | `stormpy.io.UmbExportValueType.RATIONAL_INTERVAL` |
| `stormpy.storage.UmbImportValueType.Default`<br>`stormpy.UmbImportValueType.Default` | `stormpy.io.UmbImportValueType.DEFAULT` |
| `stormpy.storage.UmbImportValueType.Double`<br>`stormpy.UmbImportValueType.Double` | `stormpy.io.UmbImportValueType.DOUBLE` |
| `stormpy.storage.UmbImportValueType.Rational`<br>`stormpy.UmbImportValueType.Rational` | `stormpy.io.UmbImportValueType.RATIONAL` |
| `stormpy.dft.ApproximationHeuristic.BOUNDDIFFERENCE` | `stormpy.dft.ApproximationHeuristic.BOUND_DIFFERENCE` |
| `stormpy.pars.RegionResult.ALLSAT` | `stormpy.pars.RegionResult.ALL_SAT` |
| `stormpy.pars.RegionResult.ALLVIOLATED` | `stormpy.pars.RegionResult.ALL_VIOLATED` |
| `stormpy.pars.RegionResult.CENTERSAT` | `stormpy.pars.RegionResult.CENTER_SAT` |
| `stormpy.pars.RegionResult.CENTERVIOLATED` | `stormpy.pars.RegionResult.CENTER_VIOLATED` |
| `stormpy.pars.RegionResult.EXISTSBOTH` | `stormpy.pars.RegionResult.EXISTS_BOTH` |
| `stormpy.pars.RegionResult.EXISTSSAT` | `stormpy.pars.RegionResult.EXISTS_SAT` |
| `stormpy.pars.RegionResult.EXISTSVIOLATED` | `stormpy.pars.RegionResult.EXISTS_VIOLATED` |
| `stormpy.pars.RegionResultHypothesis.ALLSAT` | `stormpy.pars.developer.RegionResultHypothesis.ALL_SAT` |
| `stormpy.pars.RegionResultHypothesis.ALLVIOLATED` | `stormpy.pars.developer.RegionResultHypothesis.ALL_VIOLATED` |
| `stormpy.pars.RegionResultHypothesis.UNKNOWN` | `stormpy.pars.developer.RegionResultHypothesis.UNKNOWN` |
| `stormpy.pomdp.PomdpFscApplicationMode.full` | `stormpy.pomdp.PomdpFscApplicationMode.FULL` |
| `stormpy.pomdp.PomdpFscApplicationMode.simple_linear` | `stormpy.pomdp.PomdpFscApplicationMode.SIMPLE_LINEAR` |
| `stormpy.pomdp.PomdpFscApplicationMode.simple_linear_inverse` | `stormpy.pomdp.PomdpFscApplicationMode.SIMPLE_LINEAR_INVERSE` |
| `stormpy.pomdp.PomdpFscApplicationMode.simple_log` | `stormpy.pomdp.PomdpFscApplicationMode.SIMPLE_LOG` |
| `stormpy.pomdp.PomdpFscApplicationMode.standard` | `stormpy.pomdp.PomdpFscApplicationMode.STANDARD` |
| `stormpy.pomdp.PomdpMemoryPattern.fixed_counter` | `stormpy.pomdp.PomdpMemoryPattern.FIXED_COUNTER` |
| `stormpy.pomdp.PomdpMemoryPattern.fixed_ring` | `stormpy.pomdp.PomdpMemoryPattern.FIXED_RING` |
| `stormpy.pomdp.PomdpMemoryPattern.full` | `stormpy.pomdp.PomdpMemoryPattern.FULL` |
| `stormpy.pomdp.PomdpMemoryPattern.selective_counter` | `stormpy.pomdp.PomdpMemoryPattern.SELECTIVE_COUNTER` |
| `stormpy.pomdp.PomdpMemoryPattern.selective_ring` | `stormpy.pomdp.PomdpMemoryPattern.SELECTIVE_RING` |
| `stormpy.pomdp.PomdpMemoryPattern.settable_bits` | `stormpy.pomdp.PomdpMemoryPattern.SETTABLE_BITS` |
| `stormpy.pomdp.PomdpMemoryPattern.trivial` | `stormpy.pomdp.PomdpMemoryPattern.TRIVIAL` |
| `stormpy.utility.MatrixFormat.I_Minus_P` | `stormpy.developer.utility.MatrixFormat.I_MINUS_P` |
| `stormpy.utility.MatrixFormat.Straight` | `stormpy.developer.utility.MatrixFormat.STRAIGHT` |
| `stormpy.utility.SmtCheckResult.Sat` | `stormpy.developer.SmtCheckResult.SAT` |
| `stormpy.utility.SmtCheckResult.Unknown` | `stormpy.developer.SmtCheckResult.UNKNOWN` |
| `stormpy.utility.SmtCheckResult.Unsat` | `stormpy.developer.SmtCheckResult.UNSAT` |