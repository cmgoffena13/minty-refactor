function createLineGraph(url) {
  $.ajax(url)
    .done(function (net_worth_data) {
      const labels = net_worth_data.map((e) => e.net_worth_date);
      const assets = net_worth_data.map((e) => e.assets_amount);
      const debts = net_worth_data.map((e) => e.debts_amount);
      const net_worths = net_worth_data.map((e) => e.net_amount);

      const config = {
        type: "line",
        data: {
          labels: labels,
          datasets: [
            {
              label: "Assets",
              data: assets,
            },
            {
              label: "Debts",
              data: debts,
            },
            {
              label: "Net Worth",
              data: net_worths,
            },
          ],
        },
      };

      const elem = document
        .getElementById("net_worth_line_graph")
        .getContext("2d");
      new Chart(elem, config);
    })
    .fail(function () {
      const elem = document
        .getElementById("net_worth_line_graph")
        .getContext("2d");
      elem.text = "Cannot access net worth data";
    });
}
