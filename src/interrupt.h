#pragma once

#include "common.h"

#include <chrono>
#include <exception>
#include <functional>
#include <optional>
#include <storm/utility/SignalHandler.h>
#include <thread>
#include <type_traits>
#include <utility>

namespace stormpy {
namespace detail {

/*!
 * Termination check invoked by Storm via storm::utility::resources::isTerminate().
 * Pending Python signals are processed at most once per check interval, because Storm may call isTerminate() very often
 * and each check needs to acquire the GIL.
 */
class InterruptCheck {
   public:
    static constexpr std::chrono::milliseconds checkInterval{100};

    InterruptCheck() : owner(std::this_thread::get_id()), lastCheck(std::chrono::steady_clock::now()) {}

    /*!
     * @return True iff the computation should be aborted because a Python signal handler raised an exception.
     */
    bool operator()() {
        if (interrupted) {
            return true;
        }
        if (std::this_thread::get_id() != owner) {
            // Only the thread which started the computation can process Python signals.
            return false;
        }
        auto const now = std::chrono::steady_clock::now();
        if (now - lastCheck < checkInterval) {
            return false;
        }
        lastCheck = now;
        py::gil_scoped_acquire acquire;
        // Checks the Python signal handlers
        if (PyErr_CheckSignals() != 0) {
            interrupted = true;
        }
        return interrupted;
    }

    bool isInterrupted() const {
        return interrupted;
    }

   private:
    std::thread::id owner;
    std::chrono::steady_clock::time_point lastCheck;
    bool interrupted = false;
};

/*!
 * Invoke the given function without holding the GIL, while allowing Python signals to abort the computation in Storm.
 * Must be called with the GIL held.
 *
 * If a Python signal handler raised an exception during the computation, that exception is raised.
 */
template<typename Function, typename... Args>
auto invokeInterruptible(Function const& function, Args&&... args) {
    using Result = std::invoke_result_t<Function const&, Args&&...>;
    static_assert(!std::is_reference_v<Result>, "Interruptible functions must return by value.");

    auto threading = py::module_::import("threading");
    bool mainThread = threading.attr("current_thread")().is(threading.attr("main_thread")());
    if (!mainThread) {
        // Signals cannot be processed on this thread
        py::gil_scoped_release release;
        return std::invoke(function, std::forward<Args>(args)...);
    }

    InterruptCheck check;
    std::exception_ptr error;
    std::conditional_t<std::is_void_v<Result>, bool, std::optional<Result>> result{};
    {
        storm::utility::resources::ScopedTerminationCallback guard([&check]() { return check(); });
        py::gil_scoped_release release;
        try {
            if constexpr (std::is_void_v<Result>) {
                std::invoke(function, std::forward<Args>(args)...);
            } else {
                result.emplace(std::invoke(function, std::forward<Args>(args)...));
            }
        } catch (...) {
            error = std::current_exception();
        }
        // GIL is reacquired before the termination callback is removed
    }

    if (check.isInterrupted()) {
        // The termination flag in Storm is latched; clear it such that subsequent computations are not aborted immediately.
        storm::utility::resources::resetTerminate();
        if (!PyErr_Occurred()) {
            PyErr_SetNone(PyExc_KeyboardInterrupt);
        }
        // Discards the partial result or the abort exception from Storm
        throw py::error_already_set();
    }
    if (error) {
        std::rethrow_exception(error);
    }
    if constexpr (!std::is_void_v<Result>) {
        return std::move(*result);
    }
}

}  // namespace detail

/*!
 * Wrap a free function such that it runs without the GIL and can be interrupted by Python signals.
 * Use instead of py::call_guard<py::gil_scoped_release>() for long-running computations in Storm.
 */
template<typename Return, typename... Args>
auto interruptible(Return (*function)(Args...)) {
    return [function](Args... args) -> Return { return detail::invokeInterruptible(function, std::forward<Args>(args)...); };
}

/*!
 * Wrap a member function such that it runs without the GIL and can be interrupted by Python signals.
 */
template<typename Return, typename Class, typename... Args>
auto interruptible(Return (Class::*function)(Args...)) {
    return [function](Class& self, Args... args) -> Return { return detail::invokeInterruptible(function, self, std::forward<Args>(args)...); };
}

/*!
 * Wrap a const member function such that it runs without the GIL and can be interrupted by Python signals.
 */
template<typename Return, typename Class, typename... Args>
auto interruptible(Return (Class::*function)(Args...) const) {
    return [function](Class const& self, Args... args) -> Return { return detail::invokeInterruptible(function, self, std::forward<Args>(args)...); };
}
}  // namespace stormpy
