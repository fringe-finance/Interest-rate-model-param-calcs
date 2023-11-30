import argparse
from web3 import Web3

# Create the argument parser
parser = argparse.ArgumentParser(description="Script to calculate APYs")

# Define arguments
parser.add_argument("--rpc", required=True, help="The RPC URL")
parser.add_argument("--blend", required=True, help="Blending token contract address")
parser.add_argument(
    "--jumpRate", required=True, help="Jump rate model contract address"
)
parser.add_argument(
    "--blocksPerYear", type=int, required=True, help="Number of blocks per year"
)

# Parse the arguments
args = parser.parse_args()
# Initialize web3
w3 = Web3(Web3.HTTPProvider(args.rpc))

# ABI for BlendingTokenProxy
blendingTokenProxy_abi = """
[
    {"constant": true, "inputs": [], "name": "getCash", "outputs": [{"name": "", "type": "uint256"}], "type": "function"},
    {"constant": true, "inputs": [], "name": "totalBorrowsCurrent", "outputs": [{"name": "", "type": "uint256"}], "type": "function"},
    {"constant": true, "inputs": [], "name": "totalReserves", "outputs": [{"name": "", "type": "uint256"}], "type": "function"},
    {"constant": true, "inputs": [], "name": "reserveFactorMantissa", "outputs": [{"name": "", "type": "uint256"}], "type": "function"}
]
"""

# ABI for JumpRateModelV3Proxy
jumpRateModelV3Proxy_abi = """
[
    {"constant": true, "inputs": [{"name": "cash", "type": "uint256"},{"name": "borrows", "type": "uint256"},{"name": "reserves", "type": "uint256"},{"name": "blendingToken", "type": "address"}],"name": "getBorrowRate","outputs": [{"name": "", "type": "uint256"}], "type": "function"},
    {"constant": true, "inputs": [{"name": "cash", "type": "uint256"},{"name": "borrows", "type": "uint256"},{"name": "reserves", "type": "uint256"},{"name": "reserveFactorMantissa", "type": "uint256"},{"name": "blendingToken", "type": "address"}],"name": "getSupplyRate","outputs": [{"name": "", "type": "uint256"}], "type": "function"}
]
"""

blendingTokenProxy_address = args.blend
jumpRateModelV3Proxy_address = args.jumpRate
blocksPerYear = args.blocksPerYear
daysPerYear = 365
blocksPerDay = blocksPerYear / daysPerYear


# Initialize contract instances
blendingTokenProxy_contract = w3.eth.contract(
    address=blendingTokenProxy_address, abi=blendingTokenProxy_abi
)
jumpRateModelV3Proxy_contract = w3.eth.contract(
    address=jumpRateModelV3Proxy_address, abi=jumpRateModelV3Proxy_abi
)

# Fetch market data
cash = blendingTokenProxy_contract.functions.getCash().call()
borrows = blendingTokenProxy_contract.functions.totalBorrowsCurrent().call()
reserves = blendingTokenProxy_contract.functions.totalReserves().call()
reserveFactorMantissa = (
    blendingTokenProxy_contract.functions.reserveFactorMantissa().call()
)

# Calculate utilization rate
utilization_rate = borrows / (cash + borrows + reserves)

# Fetch and calculate borrow rate
new_borrow_rate = jumpRateModelV3Proxy_contract.functions.getBorrowRate(
    cash, borrows, reserves, blendingTokenProxy_address
).call()
borrowAPY = ((((new_borrow_rate / 1e18 * blocksPerDay) + 1) ** daysPerYear) - 1) * 100

# Fetch and calculate supply rate
new_supply_rate = jumpRateModelV3Proxy_contract.functions.getSupplyRate(
    cash, borrows, reserves, reserveFactorMantissa, blendingTokenProxy_address
).call()
supplyAPY = ((((new_supply_rate / 1e18 * blocksPerDay) + 1) ** daysPerYear) - 1) * 100

# Display results
print(f"Cash: {int(cash/1e18*10)/10}")
print(f"Borrows: {int(borrows/1e18*10)/10}")
print(f"Reserves: {int(reserves/1e18*10)/10}")
print(f"Reserve Factor: {int(reserveFactorMantissa/1e18*100*10)/10}%")
print(f"Utilization Rate: {int(utilization_rate*1000)/10}%")
print(f"Borrow APY: {int(borrowAPY * 10) / 10}%")
print(f"Supply APY: {int(supplyAPY * 10) / 10}%")
print(f"RAW New Borrow Rate: {borrowAPY}%")
