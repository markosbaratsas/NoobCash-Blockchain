from ctypes import addressof
import requests
import sys
from time import sleep, time


# the addresses are hardcoded here because this script will only run in a
# specific network with those addresses
addresses = {
    0: "192.168.0.2:5000",
    1: "192.168.0.3:5000",
    2: "192.168.0.4:5000",
    3: "192.168.0.5:5000",
    4: "192.168.0.1:5000"
}

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

        r = requests.post(f"http://{addresses[from_wallet]}/new_transaction", json={
            "receiver": addresses[to_wallet],
            "amount": amount
        })

        print(f"Sent request to {to_wallet} with amount = {amount}")
        print("Request content", r.content)
        sleep(0.5)

    print("Execution time:", time()-start_time)
