#include "umb.h"

#include <sstream>
#include <storm/io/CompressionMode.h>
#include <storm/models/ModelBase.h>
#include <storm/models/sparse/Model.h>
#include <storm/storage/umb/export/ExportOptions.h>
#include <storm/storage/umb/export/SparseModelToUmb.h>
#include <storm/storage/umb/export/UmbExport.h>
#include <storm/storage/umb/import/ImportOptions.h>
#include <storm/storage/umb/import/SparseModelFromUmb.h>
#include <storm/storage/umb/import/UmbImport.h>
#include <storm/storage/umb/model/UmbModel.h>

#include "src/helpers.h"

void define_umb(py::module& m) {
    py::native_enum<storm::io::CompressionMode>(m, "CompressionMode", "enum.Enum", "Compression mode for UMB archives")
        .value("Default", storm::io::CompressionMode::Default)
        .value("NoCompression", storm::io::CompressionMode::None)
        .value("Gzip", storm::io::CompressionMode::Gzip)
        .value("Xz", storm::io::CompressionMode::Xz)
        .finalize();

    py::native_enum<storm::umb::ImportOptions::ValueType>(m, "UmbImportValueType", "enum.Enum", "Value type for UMB import")
        .value("Default", storm::umb::ImportOptions::ValueType::Default)
        .value("Rational", storm::umb::ImportOptions::ValueType::Rational)
        .value("Double", storm::umb::ImportOptions::ValueType::Double)
        .finalize();

    py::class_<storm::umb::ImportOptions>(m, "UmbImportOptions", "Options for importing UMB models")
        .def(py::init<>())
        .def_readwrite("value_type", &storm::umb::ImportOptions::valueType, "Value type used for all model values")
        .def_readwrite("build_choice_labeling", &storm::umb::ImportOptions::buildChoiceLabeling, "Whether to build choice labelings")
        .def_readwrite("build_state_valuations", &storm::umb::ImportOptions::buildStateValuations, "Whether to build state valuations");

    py::native_enum<storm::umb::ExportOptions::ValueType>(m, "UmbExportValueType", "enum.Enum", "Value type for UMB export")
        .value("Default", storm::umb::ExportOptions::ValueType::Default)
        .value("Rational", storm::umb::ExportOptions::ValueType::Rational)
        .value("Double", storm::umb::ExportOptions::ValueType::Double)
        .value("DoubleInterval", storm::umb::ExportOptions::ValueType::DoubleInterval)
        .value("RationalInterval", storm::umb::ExportOptions::ValueType::RationalInterval)
        .finalize();

    py::class_<storm::umb::ExportOptions>(m, "UmbExportOptions", "Options for exporting UMB models")
        .def(py::init<>())
        .def_readwrite("value_type", &storm::umb::ExportOptions::valueType, "Value type used for all model values")
        .def_readwrite("allow_choice_origins_as_actions", &storm::umb::ExportOptions::allowChoiceOriginsAsActions,
                       "Whether choice origins may be exported as actions")
        .def_readwrite("allow_choice_labeling_as_actions", &storm::umb::ExportOptions::allowChoiceLabelingAsActions,
                       "Whether choice labelings may be exported as actions")
        .def_readwrite("compression", &storm::umb::ExportOptions::compression, "Compression mode for the UMB archive")
        .def_readwrite("canonicize_pomdp", &storm::umb::ExportOptions::canonicizePomdp, "Whether to canonicize POMDPs before export");

    py::class_<storm::umb::UmbModel>(m, "UmbModel", "Model in the UMB format")
        .def("get_short_model_information", &storm::umb::UmbModel::getShortModelInformation, "Short description of the model")
        .def("get_model_information", &storm::umb::UmbModel::getModelInformation, "Detailed description of the model")
        .def(
            "validate",
            [](storm::umb::UmbModel const& model) {
                std::ostringstream errors;
                bool valid = model.validate(errors);
                return std::make_pair(valid, errors.str());
            },
            "Validate the UMB model; returns (is_valid, error_string)")
        .def("validate_or_throw", &storm::umb::UmbModel::validateOrThrow, "Validate the UMB model or throw on error")
        .def("__str__", &storm::umb::UmbModel::getShortModelInformation);

    m.def(
        "import_umb",
        [](std::string const& path, storm::umb::ImportOptions const& options) { return storm::umb::importUmb(std::filesystem::path(path), options); },
        py::arg("path"), py::arg("options") = storm::umb::ImportOptions{}, "Import a UMB model from the given archive path");

    m.def(
        "umb_to_archive",
        [](storm::umb::UmbModel const& model, std::string const& path, storm::umb::ExportOptions const& options) {
            storm::umb::toArchive(model, std::filesystem::path(path), options);
        },
        py::arg("umb_model"), py::arg("path"), py::arg("options") = storm::umb::ExportOptions{}, "Export a UMB model to the given archive path");

    m.def(
        "sparse_model_from_umb",
        [](storm::umb::UmbModel const& umbModel, storm::umb::ImportOptions const& options) { return storm::umb::sparseModelFromUmb(umbModel, options); },
        py::arg("umb_model"), py::arg("options") = storm::umb::ImportOptions{}, "Build a sparse model from the given UMB model");

    m.def(
        "sparse_model_to_umb",
        [](std::shared_ptr<storm::models::ModelBase> const& model, storm::umb::ExportOptions const& options) -> storm::umb::UmbModel {
            using M = storm::models::sparse::Model<double>;
            using MExact = storm::models::sparse::Model<storm::RationalNumber>;
            using MInterval = storm::models::sparse::Model<storm::Interval>;
            using MRatInterval = storm::models::sparse::Model<storm::RationalInterval>;
            if (auto m = std::dynamic_pointer_cast<MExact>(model))
                return storm::umb::sparseModelToUmb(*m, options);
            if (auto m = std::dynamic_pointer_cast<MInterval>(model))
                return storm::umb::sparseModelToUmb(*m, options);
            if (auto m = std::dynamic_pointer_cast<MRatInterval>(model))
                return storm::umb::sparseModelToUmb(*m, options);
            if (auto m = std::dynamic_pointer_cast<M>(model))
                return storm::umb::sparseModelToUmb(*m, options);
            throw std::invalid_argument("Unsupported model type for UMB export");
        },
        py::arg("model"), py::arg("options") = storm::umb::ExportOptions{}, "Convert a sparse model to UMB format");
}