import pandas as pd

def main():
    df = pd.read_csv('carsAT.csv')
    df[df.duplicated(subset=df.columns.difference(['link']))].to_csv("duplicated.csv")

if __name__ == "__main__":
    main()
