import pandas as pd

def main():
    df = pd.read_csv('carsAT.csv')
    df.drop_duplicates(subset=df.columns.difference(['link'])).to_csv("duplicatedDropped.csv", index = False)
    df[df.duplicated(subset=df.columns.difference(['link']))].to_csv("duplicated.csv", index = False)
    pass

if __name__ == "__main__":
    main()
