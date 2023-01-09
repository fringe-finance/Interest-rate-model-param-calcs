timePeriodDays = 1 / 48
blocksPerYear = 2102400  # correct value: 2628000, incorrect value: 2102400
daysPerYear = 365
maxIncreasePerPeriod = 0.05
maxDecreasePerPeriod = 0.05
targetUtilisationRate = 0.5

blocksPerPeriod = timePeriodDays * (blocksPerYear / daysPerYear)
maxDecreasePerBlock = maxDecreasePerPeriod / blocksPerPeriod
maxIncreasePerBlock = maxIncreasePerPeriod / blocksPerPeriod


#######################      GAIN      #######################
gain = (maxDecreasePerBlock * (365 / timePeriodDays) * (10**18)) / (
    blocksPerYear * targetUtilisationRate
)
HRgain = (maxDecreasePerPeriod * (365 / timePeriodDays)) / (targetUtilisationRate)


#######################      JUMP GAIN      #######################
jumpGain = (
    (maxIncreasePerBlock / maxDecreasePerBlock) * targetUtilisationRate * (10**18)
) / (1 - targetUtilisationRate)

HRjumpGain = ((maxIncreasePerPeriod / maxDecreasePerPeriod) * targetUtilisationRate) / (
    1 - targetUtilisationRate
)


#######################      TARGET UTILISATION      #######################
targetUtil = targetUtilisationRate * (10**18)
HRtargetUtil = targetUtilisationRate


print("\nFOR SMART CONTRACT:")
print("Gain:", round(gain, 1))
print("Jump gain:", round(jumpGain, 1))
print("Target utilisation rate:", round(targetUtil, 1))

print("\n\n\nFOR HUMANS:")
print("Gain:", round(HRgain, 3))
print("Jump gain:", round(HRjumpGain, 3))
print("Target utilisation rate:", round(HRtargetUtil, 3))
