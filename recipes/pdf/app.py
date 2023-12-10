import csv

import matplotlib.pyplot as plt
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from matplotlib.ticker import FuncFormatter

import load_pdf


def write_to_csv(billing_data):
    csv_file = "invoices.csv"
    header = billing_data[0].keys()
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(billing_data)


def draw_graph(filename):
    df = pd.read_csv(filename, thousands=",")
    df["日付"] = pd.to_datetime(
        df["日付"].str.replace("年", "-").str.replace("月", "-").str.replace("日", ""),
        format="%Y-%m-%d",
    )

    fig, ax = plt.subplots()
    ax.bar(df["日付"], df["請求金額（合計）"])
    ax.set_xlabel("date")
    ax.set_ylabel("price")
    ax.set_xticks(df["日付"])
    ax.set_xticklabels(df["日付"].dt.strftime("%Y-%m-%d"), rotation=45)
    ax.set_ylim(0, max(df["請求金額（合計）"]) + 100000)
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ",")))

    plt.tight_layout()
    plt.show()


def main():
    billing_data = load_pdf.load_all_pdfs("data")
    print("Finished reading pdf files.")

    write_to_csv(billing_data)
    print("Finished writing a csv file.")

    draw_graph("invoices.csv")


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    main()
