from gridcoin.rpc._Struct import _Struct
from gridcoin.rpc.StakeWeight import StakeWeight
from gridcoin.rpc.StakeSplitting import StakeSplitting
from gridcoin.rpc.SideStaking import SideStaking
from gridcoin.rpc.Difficulty import Difficulty


class MiningInfo(_Struct):
    blocks = 0
    stakeweight = StakeWeight()
    netstakeweight = 0.0
    netstakingGRCvalue = 0.0
    staking = True
    mining_error = ""
    time_to_stake_days = 0.0
    expectedtime = 0
    mining_version = 0
    mining_created = 0
    mining_accepted = 0
    mining_kernels_found = 0
    masked_time_intervals_covered = 0
    masked_time_intervals_elapsed = 0
    staking_loop_efficiency = 0.0
    actual_cumulative_weight = 0
    ideal_cumulative_weight = 0
    staking_efficiency = 0.0
    stake_splitting = StakeSplitting()
    side_staking = SideStaking()
    difficulty = Difficulty()
    errors = ""
    pooledtx = 0
    testnet = False
    CPID = ""
    current_magnitude = 0
    Magnitude_Unit = 0.0
    BoincRewardPending = 0.0
    researcher_status = ""
    current_poll = ""
