from ctypes import addressof
import json
import requests
import sys
from time import sleep, time


with open('addresses.json') as json_file:
    addresses = json.load(json_file)


if __name__ == "__main__":
    """This script will be executed in each one of the nodes. It executes the
    following:
    1) Read transactions from given file for a specific node
    2) Execute the transactions by sending relevant requests to the recipients
    """

    if len(sys.argv) == 1:
        print(f"""To run the script execute the following command:
              python3 {sys.argv[0]} <path_to_file_with_transactions>""")
        sys.exit(1)

    print("Reading file:", sys.argv[1])
    from_wallet = int(sys.argv[1].split(".txt")[0][-1])
    print(f"Transactions for node:", from_wallet)
    transactions = []

    with open(sys.argv[1], "r") as f:
        for line in f:
            to_wallet, amount = line.split(" ")
            to_wallet = int(to_wallet.split("id")[1].split("\n")[0])
            amount = int(amount)
            transactions.append((from_wallet, to_wallet, amount))

    start_time = time()

    for transaction in transactions:
        from_wallet, to_wallet, amount = transaction

        r = requests.post(\
            f"http://{addresses[str(from_wallet)]}/new_transaction", json={
            "receiver": addresses[str(to_wallet)],
            "amount": amount
        })

        print(f"Sent request to {to_wallet} with amount = {amount}")
        print("Request content", r.content)

    print("Execution time:", time()-start_time)

    print("Press ENTER when mining has finished.")
    user_input = input()

    print("Execution time (including mining):", time()-start_time)

    r = requests.get(f"http://{addresses[str(from_wallet)]}/get_statistics")
    r = json.loads(r.content)
    print(r)
    print("Mining mean time:", sum(r["mining_times"])/len(r["mining_times"]))
