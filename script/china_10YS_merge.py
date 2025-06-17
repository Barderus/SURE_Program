import pandas as pd
import glob
import os

def load_china_10y(filepath):
    df = pd.read_excel(filepath)
    df = df[["Date", "10Y"]]
    df.columns = ["date", "10YS_CHI"]
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["10YS_CHI"] = pd.to_numeric(df["10YS_CHI"], errors="coerce")
    return df.dropna().sort_values("date").reset_index(drop=True)


def load_all_china_10y(directory):
    files = glob.glob(os.path.join(directory, "*.xlsx"))
    frames = [load_china_10y(file) for file in files]
    return pd.concat(frames).sort_values("date").reset_index(drop=True)

def main():
    df = load_all_china_10y("../data/China-10YS")

    output_path = "../data/raw/spread/China-10YS.csv"
    df.to_csv(output_path, index=False)
    print(f"\nFile saved on {output_path}")

if __name__ == "__main__":
    main()
