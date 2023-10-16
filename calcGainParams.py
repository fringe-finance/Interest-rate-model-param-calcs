import argparse

# Initialize argparse
parser = argparse.ArgumentParser(description="Calculate gain and jump gain values")

# Add command-line arguments
parser.add_argument(
    "--period",
    type=float,
    required=True,
    help="The length of the period referred to by maxIncreasePerPeriod and maxDecreasePerPeriod, in days",
)
parser.add_argument(
    "--maxIncrease",
    type=float,
    required=True,
    help="Maximum amount interest rate should be allowed to increase in one period (0.05 means interest rate increases by at most 5%)",
)
parser.add_argument(
    "--maxDecrease",
    type=float,
    required=True,
    help="Maximum amount interest rate should be allowed to decrease in one period (0.05 means interest rate decreases by at most 5%)",
)
parser.add_argument(
    "--targetUtil", type=float, required=True, help="Target utilisation rate"
)
parser.add_argument(
    "--blocksPerYear",
    type=int,
    required=True,
    help="Number of blocks per year (this will vary on a per chain basis)",
)

parser.add_argument(
    "--format",
    type=str,
    required=True,
    help="(stored/deploy) Whether to return values stored in the smart contract or values used in the deployment script",
)

# Parse arguments
args = parser.parse_args()

# Extract configuration parameters from command-line arguments
period = args.period
maxIncreasePerPeriod = args.maxIncrease
maxDecreasePerPeriod = args.maxDecrease
targetUtilRate = args.targetUtil
blocksPerYear = args.blocksPerYear
format = args.format

# Perform calculations
timePeriodInYears = period * 365

# Downwards gain calculations
maxDownwardsUtilRateError = targetUtilRate
originalMaxDecreasePerPeriod = maxDownwardsUtilRateError * timePeriodInYears
downwardsGain = maxDecreasePerPeriod / originalMaxDecreasePerPeriod

# Upwards gain calculations
maxUpwardsUtilRateError = 1 - targetUtilRate
originalMaxIncreasePerPeriod = maxUpwardsUtilRateError * timePeriodInYears
upwardsGain = maxIncreasePerPeriod / originalMaxIncreasePerPeriod

# Final gain and jumpGain calculations
gain = downwardsGain
jumpGain = upwardsGain / downwardsGain

# Apply adjustments to produce values stored in smart contract
STOREDgainPerBlock = gain
STOREDjumpGain18 = jumpGain * 10**18

# Apply adjustments to produce values used to deploy smart contract
DEPLOYgainPerYear = gain * blocksPerYear
DEPLOYjumpGain18PerYear = jumpGain * 10**18 * blocksPerYear


if format == "stored":
    print("(Stored) gain per block: {}".format(int(STOREDgainPerBlock)))
    print("(Stored) jump gain * 10e18: {}".format(int(STOREDjumpGain18)))
elif format == "deploy":
    print("(Deploy) gain per year: {}".format(int(DEPLOYgainPerYear)))
    print(
        "(Deploy) jump gain * 10e18 per year: {}".format(int(DEPLOYjumpGain18PerYear))
    )
