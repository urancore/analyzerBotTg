import json
import datetime
import logging
from matplotlib import pyplot as plt
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class DataPlotter:
    def __init__(
        self,
        data_file_name: str,
        save_file_name: str,
        graph_title: str = "Channel Data"
    ):
        self.data_file_name = data_file_name
        self.save_file_name = save_file_name
        self.graph_title = graph_title

        self.daily_averages = {}  # {date: avg_views}

    def load_and_aggregate_data(self):
        try:
            with open(self.data_file_name, "r", encoding="utf-8") as f:
                data_list = json.load(f)
        except FileNotFoundError:
            logging.error(f"File not found: {self.data_file_name}")
            return
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {e}")
            return

        day_views = defaultdict(list)

        for item in data_list:
            views = item.get("views")
            date_str = item.get("date")

            if views is None or date_str is None:
                continue

            try:
                date = datetime.datetime.fromisoformat(date_str)
            except ValueError:
                try:
                    date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    continue

            day = date.date()
            day_views[day].append(views)

        self.daily_averages = {
            day: sum(views) / len(views) for day, views in sorted(day_views.items())
        }

        logging.info(f"Calculated averages for {len(self.daily_averages)} days.")

    def create_plot(self):
        if not self.daily_averages:
            logging.warning("No data to plot.")
            return

        dates = list(self.daily_averages.keys())
        avg_views = list(self.daily_averages.values())

        plt.style.use("seaborn-v0_8-darkgrid")
        fig, ax = plt.subplots(figsize=(10, 5))

        ax.plot(dates, avg_views, color="tab:blue", linewidth=2, label="Average daily views")

        ymax = max(avg_views)
        xmax = dates[avg_views.index(ymax)]
        ax.annotate(f"Max: {int(ymax)}", xy=(xmax, ymax), xytext=(xmax, ymax + ymax * 0.05),
                    arrowprops=dict(arrowstyle="->", color="gray"), fontsize=10)

        fig.autofmt_xdate()
        ax.set_xlabel("Date")
        ax.set_ylabel("Average Views per Post")
        ax.set_title(f"{self.graph_title} — Average Daily Views")
        ax.legend()
        ax.grid(True, which="major", linestyle="--", linewidth=0.7)

        # save
        plt.tight_layout()
        plt.savefig(self.save_file_name)
        plt.close(fig)

        logging.info(f"Graph saved to: {self.save_file_name}")


def draw(data_file_name: str, save_file_name: str, graph_title: str):
    plotter = DataPlotter(
        data_file_name=data_file_name,
        save_file_name=save_file_name,
        graph_title=graph_title
    )
    plotter.load_and_aggregate_data()
    plotter.create_plot()
