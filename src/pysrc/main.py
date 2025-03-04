from pysrc.logging.logging_config import setup_logging
from pysrc.calculate_corr_pybind import calculate_corr, run_iterations


def main() -> None:
    setup_logging()

    TIMESTAMP = 1740757948  # This morning

    run_iterations(TIMESTAMP, 100, "output.csv")
    corr = calculate_corr("output/output.csv")
    print(f"Correlation: {corr}")


if __name__ == "__main__":
    main()
