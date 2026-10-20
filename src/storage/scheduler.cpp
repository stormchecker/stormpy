#include "scheduler.h"

#include <storm/adapters/IntervalAdapter.h>
#include <storm/adapters/RationalFunctionAdapter.h>
#include <storm/storage/scheduler/Scheduler.h>

#include "src/binding_type_index.h"
#include "src/helpers.h"

// The return value's type cannot be deduced from the scheduler argument.
// Register one function family per target type, with overloads for the source types.
template<typename SourceType, typename TargetType>
void bind_scheduler_conversion(py::module& m) {
    auto const index = stormpy::bindings::typeIndex<TargetType>();
    auto convert = [](storm::storage::Scheduler<SourceType> const& scheduler) { return scheduler.template toValueType<TargetType>(); };
    if constexpr (std::is_same_v<SourceType, double>) {
        stormpy::bindings::bindTemplateFunction(m, "to_value_type", index, convert, "Convert a scheduler to another value type", py::arg("scheduler"));
    } else {
        stormpy::bindings::bindInternalFunction(m, stormpy::bindings::templateClassName("to_value_type", index), convert,
                                                "Convert a scheduler to another value type", py::arg("scheduler"));
    }
}

template<typename ValueType>
void define_scheduler(py::module& m) {
    using Scheduler = storm::storage::Scheduler<ValueType>;
    using SchedulerChoice = storm::storage::SchedulerChoice<ValueType>;

    auto const index = stormpy::bindings::typeIndex<ValueType>();
    auto scheduler = stormpy::bindings::bindTemplateClass<Scheduler>(m, "Scheduler", index, "A Finite Memory Scheduler");
    scheduler
        .def("__str__",
             [](Scheduler const& s) {
                 std::stringstream str;
                 s.printToStream(str);
                 return str.str();
             })
        .def_property_readonly("memoryless", &Scheduler::isMemorylessScheduler, "Is the scheduler memoryless?")
        .def_property_readonly("memory_size", &Scheduler::getNumberOfMemoryStates, "How much memory does the scheduler take?")
        .def_property_readonly("deterministic", &Scheduler::isDeterministicScheduler, "Is the scheduler deterministic?")
        .def_property_readonly("partial", &Scheduler::isPartialScheduler, "Is the scheduler partial?")
        .def("get_choice", &Scheduler::getChoice, py::arg("state_index"), py::arg("memory_index") = 0)
        .def("set_choice", &Scheduler::setChoice, py::arg("choice"), py::arg("state"), py::arg("memory_index") = 0)
        .def("compute_action_support", &Scheduler::computeActionSupport, "nondeterministic_choice_indices"_a)
        .def(
            "to_json_str",
            [](Scheduler const& s, std::shared_ptr<storm::models::sparse::Model<ValueType>> model, bool skipUniqueChoices, bool skipDontCareStates) {
                std::stringstream str;
                s.printJsonToStream(str, model, skipUniqueChoices, skipDontCareStates);
                return str.str();
            },
            py::arg("model"), py::arg("skip_unique_choices") = false, py::arg("skip_dont_care_states") = false)
        .def(
            "to_str",
            [](Scheduler const& s, std::shared_ptr<storm::models::sparse::Model<ValueType>> model, bool skipUniqueChoices, bool skipDontCareStates) {
                std::stringstream str;
                s.printToStream(str, model, skipUniqueChoices, skipDontCareStates);
                return str.str();
            },
            py::arg("model") = nullptr, py::arg("skip_unique_choices") = false, py::arg("skip_dont_care_states") = false)
        .def("get_memoryless_scheduler_for_memory_state", &Scheduler::getMemorylessSchedulerForMemoryState, py::arg("memory_state") = 0,
             "Get the memoryless scheduler corresponding to the given memory state");

    if constexpr (!storm::IsIntervalType<ValueType>) {
        bind_scheduler_conversion<ValueType, double>(m);
        bind_scheduler_conversion<ValueType, storm::RationalNumber>(m);
        bind_scheduler_conversion<ValueType, storm::RationalFunction>(m);
        if constexpr (!std::is_same_v<ValueType, storm::RationalFunction>) {
            bind_scheduler_conversion<ValueType, storm::Interval>(m);
            bind_scheduler_conversion<ValueType, storm::RationalInterval>(m);
        }
    }

    auto schedulerChoice = stormpy::bindings::bindTemplateClass<SchedulerChoice>(m, "SchedulerChoice", index, "A choice of a finite memory scheduler");
    schedulerChoice.def(py::init<uint64_t>(), "choice"_a)
        .def_property_readonly("defined", &SchedulerChoice::isDefined, "Is the choice defined by the scheduler?")
        .def_property_readonly("deterministic", &SchedulerChoice::isDeterministic, "Is the choice deterministic (given by a Dirac distribution)?")
        .def("get_deterministic_choice", &SchedulerChoice::getDeterministicChoice, "Get the deterministic choice")
        .def("get_choice_as_distribution", &SchedulerChoice::getChoiceAsDistribution, "Get the distribution over the actions")
        .def("__str__", &streamToString<SchedulerChoice>);
}

template void define_scheduler<double>(py::module& m);
template void define_scheduler<storm::RationalNumber>(py::module& m);
template void define_scheduler<storm::Interval>(py::module& m);
template void define_scheduler<storm::RationalInterval>(py::module& m);
template void define_scheduler<storm::RationalFunction>(py::module& m);
