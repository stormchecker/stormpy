#include "scheduler.h"
#include "src/helpers.h"

#include "storm/adapters/IntervalAdapter.h"
#include "storm/adapters/RationalFunctionAdapter.h"
#include "storm/storage/Scheduler.h"

template<typename ValueType>
void define_scheduler(py::module& m, std::string vt_suffix) {
    using Scheduler = storm::storage::Scheduler<ValueType>;
    using SchedulerChoice = storm::storage::SchedulerChoice<ValueType>;

    std::string schedulerClassName = std::string("Scheduler") + vt_suffix;
    py::class_<Scheduler, std::shared_ptr<storm::storage::Scheduler<ValueType>>> scheduler(m, schedulerClassName.c_str(), "A Finite Memory Scheduler");
    scheduler
            .def("__str__", [](Scheduler const& s) {
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
            .def("to_json_str", [](Scheduler const& s, std::shared_ptr<storm::models::sparse::Model<ValueType>> model, bool skipUniqueChoices,
                               bool skipDontCareStates) {
                    std::stringstream str;
                    s.printJsonToStream(str, model, skipUniqueChoices, skipDontCareStates);
                    return str.str();
                }, py::arg("model"), py::arg("skip_unique_choices") = false, py::arg("skip_dont_care_states") = false)
    ;

    if constexpr (!storm::IsIntervalType<ValueType>) {
        // Conversion from Interval not implemented
        scheduler
            .def("cast_to_double_datatype", &Scheduler::template toValueType<double>, "Construct the scheduler with `double` value type")
            .def("cast_to_exact_datatype", &Scheduler::template toValueType<storm::RationalNumber>, "Construct the scheduler with `exact` value type")
            .def("cast_to_parametric_datatype", &Scheduler::template toValueType<storm::RationalFunction>, "Construct the scheduler with `parametric` value type")
        ;
        if constexpr (!std::is_same_v<ValueType, storm::RationalFunction>) {
            // Conversion from RationalFunction to Interval not implemented
            scheduler.def("cast_to_interval_datatype", &Scheduler::template toValueType<storm::Interval>, "Construct the scheduler with `interval` value type");
        }
    }


    std::string schedulerChoiceClassName = std::string("SchedulerChoice") + vt_suffix;
    py::class_<SchedulerChoice> schedulerChoice(m, schedulerChoiceClassName.c_str(), "A choice of a finite memory scheduler");
    schedulerChoice
        .def(py::init<uint64_t>(), "choice"_a)
        .def_property_readonly("defined", &SchedulerChoice::isDefined, "Is the choice defined by the scheduler?")
        .def_property_readonly("deterministic", &SchedulerChoice::isDeterministic, "Is the choice deterministic (given by a Dirac distribution)?")
        .def("get_deterministic_choice", &SchedulerChoice::getDeterministicChoice, "Get the deterministic choice")
        .def("get_choice", &SchedulerChoice::getChoiceAsDistribution, "Get the distribution over the actions")
        .def("__str__", &streamToString<SchedulerChoice>);
}


template void define_scheduler<double>(py::module& m, std::string vt_suffix);
template void define_scheduler<storm::RationalNumber>(py::module& m, std::string vt_suffix);
template void define_scheduler<storm::Interval>(py::module& m, std::string vt_suffix);
template void define_scheduler<storm::RationalInterval>(py::module& m, std::string vt_suffix);
template void define_scheduler<storm::RationalFunction>(py::module& m, std::string vt_suffix);
