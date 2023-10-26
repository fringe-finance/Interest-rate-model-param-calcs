from web3 import Web3
import time

# Initialize web3
w3 = Web3(
    Web3.HTTPProvider(
        "https://eth-goerli.g.alchemy.com/v2/EkJ6KVy7Q1Cu77daPHQo8VVn20m55pzJ"
    )
)

# ABI for BlendingTokenProxy
blendingTokenProxy_abi = """
[
    {
        "constant": true,
        "inputs": [],
        "name": "getCash",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "totalBorrowsCurrent",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function"
    }
]
"""

# ABI for JumpRateModelV3Proxy
jumpRateModelV3Proxy_abi = """
[
    {
        "constant": true,
        "inputs": [
            {"name": "cash", "type": "uint256"},
            {"name": "borrows", "type": "uint256"},
            {"name": "reserves", "type": "uint256"},
            {"name": "blendingToken", "type": "address"}
        ],
        "name": "getBorrowRate",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function"
    }
]
"""

# Contract addresses (replace these with actual values)
blendingTokenProxy_address = "0xcB034b9A387DA193F524aB9E222f909dfEDC08c9"
jumpRateModelV3Proxy_address = "0xDaad874Ec0dd2345F1Ec05959CFfBb7906fB4F9d"
blocksPerYear = 2102400


# Initialize contract instances
blendingTokenProxy_contract = w3.eth.contract(
    address=blendingTokenProxy_address, abi=blendingTokenProxy_abi
)
jumpRateModelV3Proxy_contract = w3.eth.contract(
    address=jumpRateModelV3Proxy_address, abi=jumpRateModelV3Proxy_abi
)

# Get market data from BlendingTokenProxy
cash = blendingTokenProxy_contract.functions.getCash().call()
borrows = blendingTokenProxy_contract.functions.totalBorrowsCurrent().call()

# Get current block number
current_block = w3.eth.get_block("latest")["number"]

# Calculate utilization rate
utilization_rate = borrows / (cash + borrows)  # Assuming no reserves for simplification

# Calculate and store new borrow rate
new_borrow_rate = jumpRateModelV3Proxy_contract.functions.getBorrowRate(
    cash, borrows, 0, blendingTokenProxy_address
).call()  # Assuming no reserves for simplification


# Print calculated values
print(f"Cash: {cash}")
print(f"Borrows: {borrows}")
print(f"Current Block: {current_block}")
print(f"Utilization Rate: {utilization_rate}")
print(f"New Borrow Rate: {(new_borrow_rate*blocksPerYear*100)/10**18}%")
