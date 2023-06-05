function createPayPeriodLineGraph(url) {
  $.ajax(url)
    .done(function (pay_period_data) {
      const labels = pay_period_data.map((e) => e.date_actual);
      const rolling_net_current = pay_period_data.map(
        (e) => e.rolling_transactions_amounts_p1
      );
      const rolling_net_previous = pay_period_data.map(
        (e) => e.rolling_transactions_amounts_p2
      )
      const break_even = pay_period_data.map((e) => e.break_even);

      const config = {
        type: "line",
        data: {
          labels: labels,
          datasets: [
            {
              label: "Net Income Current",
              data: rolling_net_current,
            },
            {
              label: "Net Income Previous",
              data: rolling_net_previous,
            },
            {
              label: "Break Even",
              data: break_even,
            },
          ],
        },
      };
      const elem = document
        .getElementById("pay_period_line_graph")
        .getContext("2d");
      new Chart(elem, config);
    })
    .fail(function () {
      const elem = document
        .getElementById("pay_period_line_graph")
        .getContext("2d");
      elem.text = "Cannot access pay period data";
    });
}
