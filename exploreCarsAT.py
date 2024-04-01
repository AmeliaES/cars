import pandas as pd
import plotly.express as px

def main():
    df = pd.read_csv('carsAT.csv')

    fig = px.scatter(df, x="year", y="mileage", color="price")

    # Change axis labels
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Mileage",
        font=dict(
            size=18  # Increase text size
        )
    )

    # Increase point size
    fig.update_traces(marker=dict(size=8))

    # Use reversed Viridis color scale
    fig.update_traces(marker=dict(color=df["price"], colorscale='Viridis_r'))

    # Save as PNG
    # fig.write_image("carsAT.png")

    # Save as HTML
    fig.write_html("carsAT.html")

    # Show the plot
    fig.show()

if __name__ == "__main__":
    main()
