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
    "--targetUtil",
    type=float,
    required=True,
    help="Target utilisation rate. I.e. passing a value of 0.5 = 50% target utilisation rate",
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
    help="(read/write) Whether to return values corresponding to those stored in the JumpRateModel v3 contract (read) or values passed to updateJumpRateModel when deploying or modifying parameters (write)",
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
timePeriodInYears = period / 365


### see gist for explanation of the below logic

# Downwards gain calculations
maxDownwardsUtilRateError = targetUtilRate
originalMaxDecreasePerYear = maxDownwardsUtilRateError * blocksPerYear * blocksPerYear
originalMaxDecreasePerPeriod = originalMaxDecreasePerYear * timePeriodInYears
downwardsGain = desiredMaxDecreasePerPeriod / originalMaxDecreasePerPeriod

# Upwards gain calculations
maxUpwardsUtilRateError = 1 - targetUtilRate
originalMaxIncreasePerYear = maxUpwardsUtilRateError * blocksPerYear * blocksPerYear
originalMaxIncreasePerPeriod = originalMaxIncreasePerYear * timePeriodInYears
upwardsGain = desiredMaxIncreasePerPeriod / originalMaxIncreasePerPeriod

# Final gain and jumpGain calculations
gain = downwardsGain
jumpGain = upwardsGain / downwardsGain

targetUtilRate18 = targetUtilRate * 10**18

# Apply adjustments to produce values stored in smart contract
READgainPerBlock18 = gain * 10**18
READjumpGainPerBlock18 = jumpGain * 10**18


# Apply adjustments to produce values used to configure deployment scripts
WRITEgainPerYear18 = gain * blocksPerYear * 10**18
WRITEjumpGainPerYear18 = jumpGain * blocksPerYear * 10**18

if format == "read":
    print("(Read) gain per block: {}".format(int(READgainPerBlock18)))
    print("(Read) jump gain per block: {}".format(int(READjumpGainPerBlock18)))
    print("(Read) target utilisation rate: {}".format(int(targetUtilRate18)))
elif format == "write":
    print("(Write) gain per year: {}".format(int(WRITEgainPerYear18)))
    print("(Write) jump gain per year: {}".format(int(WRITEjumpGainPerYear18)))
    print("(Write) target utilisation rate: {}".format(int(targetUtilRate18)))
