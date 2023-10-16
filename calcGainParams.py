timePeriodDays = 1 / 48
maxIncreasePerPeriod = 0.05
maxDecreasePerPeriod = 0.05
targetUtilisationRate = 0.5
blocksPerYear = 2102400  # correct value: 2628000, incorrect value: 2102400


# calculate time period as a fraction of one year
timePeriodInYears = timePeriodDays * 365


## calculate downwards gain
maxDownwardsUtilRateError = targetUtilisationRate
originalMaxDecreasePerPeriod = maxDownwardsUtilRateError * timePeriodInYears
downwardsGain = maxDecreasePerPeriod / originalMaxDecreasePerPeriod

## calculate upwards gain
maxUpwardsUtilRateError = 1 - targetUtilisationRate
originalMaxIncreasePerPeriod = maxUpwardsUtilRateError * timePeriodInYears
upwardsGain = maxIncreasePerPeriod / originalMaxIncreasePerPeriod

# calculate final values for gain and jumpGain
gain = downwardsGain
jumpGain = upwardsGain / downwardsGain

gainPerBlock = gain * blocksPerYear
jumpGain18 = jumpGain * 10**18

print(f"Gain: {gainPerBlock}")
print(f"Jump gain: {jumpGain18}")
