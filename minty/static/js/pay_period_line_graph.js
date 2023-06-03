function createPayPeriodLineGraph(url) {
  $.ajax(url)
    .done(function (pay_period_data) {
      const labels = pay_period_data.map((e) => e.date_actual);
      const rolling_net = pay_period_data.map(
        (e) => e.rolling_transactions_amounts
      );
      const break_even = pay_period_data.map((e) => e.break_even);

      const config = {
        type: "line",
        data: {
          labels: labels,
          datasets: [
            {
              label: "Net Income",
              data: rolling_net,
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
