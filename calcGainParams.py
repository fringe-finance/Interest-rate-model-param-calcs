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
    help="Maximum amount interest rate should be allowed to increase in one period 0.05 means interest rate increases by at most 5 percent",
)
parser.add_argument(
    "--maxDecrease",
    type=float,
    required=True,
    help="Maximum amount interest rate should be allowed to decrease in one period. 0.05 means interest rate decreases by at most 5 percent",
)
parser.add_argument(
    "--targetUtil", type=float, required=True, help="Target utilisation rate"
)
parser.add_argument(
    "--blocksPerYear",
    type=int,
    required=True,
    help="Number of blocks per year. This will vary on a per chain basis.",
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
desiredMaxIncreasePerPeriod = args.maxIncrease
desiredMaxDecreasePerPeriod = args.maxDecrease
targetUtilRate = args.targetUtil
blocksPerYear = args.blocksPerYear
format = args.format

# Perform calculations
timePeriodInYears = period * 365

# Downwards gain calculations
maxDownwardsUtilRateError = targetUtilRate
originalMaxDecreasePerPeriod = maxDownwardsUtilRateError * timePeriodInYears
downwardsGain = desiredMaxDecreasePerPeriod / originalMaxDecreasePerPeriod

# Upwards gain calculations
maxUpwardsUtilRateError = 1 - targetUtilRate
originalMaxIncreasePerPeriod = maxUpwardsUtilRateError * timePeriodInYears
upwardsGain = desiredMaxIncreasePerPeriod / originalMaxIncreasePerPeriod

# Final gain and jumpGain calculations
gain = downwardsGain
jumpGain = upwardsGain / downwardsGain

# Apply adjustments to produce values stored in smart contract
STOREDgainPerBlock18 = gain * 10**18
STOREDjumpGainPerBlock18 = jumpGain * 10**18

# Apply adjustments to produce values used to configure deployment scripts
DEPLOYgainPerYear18 = gain * blocksPerYear * 10**18
DEPLOYjumpGainPerYear18 = jumpGain * blocksPerYear * 10**18


if format == "stored":
    print("(Stored) gain per block: {}".format(int(STOREDgainPerBlock18)))
    print("(Stored) jump gain {}".format(int(STOREDjumpGainPerBlock18)))
elif format == "deploy":
    print("(Deploy) gain per year: {}".format(int(DEPLOYgainPerYear18)))
    print("(Deploy) jump gain per year: {}".format(int(DEPLOYjumpGainPerYear18)))
