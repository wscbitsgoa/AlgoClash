from src.market.market import Market


def main():
    market = Market(seed=42)

    print("Initial prices:")
    print(market.get_prices())

    print("\n--- TICK 1 ---")
    print(market.update())

    print("\n--- TICK 2 ---")
    print(market.update())

    print("\n--- TICK 3 ---")
    print(market.update())

    print("\n--- TECH CRASH ---")

    print(
        market.update(
            shocks={
                "TECH": -0.20
            }
        )
    )

    print("\n--- STK_7 RALLY ---")

    print(
        market.update(
            shocks={
                "STK_7": 0.10
            }
        )
    )


if __name__ == "__main__":
    main()