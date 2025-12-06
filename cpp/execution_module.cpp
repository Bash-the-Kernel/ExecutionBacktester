// C++ execution accelerator module using pybind11

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <random>
#include <cmath>

namespace py = pybind11;

class FastExecutionSimulator {
private:
    double slippage_bps;
    double commission_bps;
    std::mt19937 rng;
    std::uniform_real_distribution<double> dist;

public:
    FastExecutionSimulator(double slippage, double commission) 
        : slippage_bps(slippage / 10000.0), 
          commission_bps(commission / 10000.0),
          rng(std::random_device{}()),
          dist(0.5, 1.5) {}

    std::tuple<double, double, double> execute_order(
        double base_price, 
        double quantity, 
        const std::string& direction
    ) {
        // Calculate slippage
        double slippage_factor = dist(rng) * slippage_bps;
        double slippage = (direction == "BUY") ? 
            base_price * slippage_factor : 
            -base_price * slippage_factor;
        
        double fill_price = base_price + slippage;
        
        // Calculate commission
        double commission = quantity * fill_price * commission_bps;
        
        return std::make_tuple(fill_price, std::abs(slippage), commission);
    }

    std::vector<double> calculate_portfolio_values(
        const std::vector<double>& cash_flows,
        const std::vector<double>& position_values
    ) {
        std::vector<double> portfolio_values;
        portfolio_values.reserve(cash_flows.size());
        
        for (size_t i = 0; i < cash_flows.size(); ++i) {
            portfolio_values.push_back(cash_flows[i] + position_values[i]);
        }
        
        return portfolio_values;
    }

    double calculate_sharpe_ratio(
        const std::vector<double>& returns,
        double risk_free_rate = 0.02,
        int periods_per_year = 252
    ) {
        if (returns.empty()) return 0.0;
        
        double mean = 0.0;
        for (double r : returns) mean += r;
        mean /= returns.size();
        
        double variance = 0.0;
        for (double r : returns) {
            double diff = r - mean;
            variance += diff * diff;
        }
        variance /= returns.size();
        double std_dev = std::sqrt(variance);
        
        if (std_dev == 0.0) return 0.0;
        
        double excess_return = mean - (risk_free_rate / periods_per_year);
        return std::sqrt(periods_per_year) * excess_return / std_dev;
    }
};

PYBIND11_MODULE(execution_cpp, m) {
    m.doc() = "Fast execution simulation module";

    py::class_<FastExecutionSimulator>(m, "FastExecutionSimulator")
        .def(py::init<double, double>())
        .def("execute_order", &FastExecutionSimulator::execute_order)
        .def("calculate_portfolio_values", &FastExecutionSimulator::calculate_portfolio_values)
        .def("calculate_sharpe_ratio", &FastExecutionSimulator::calculate_sharpe_ratio);
}
