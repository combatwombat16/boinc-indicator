from gridcoin.rpc._Struct import _Struct
from gridcoin.rpc.StakeWeight import StakeWeight
from gridcoin.rpc.StakeSplitting import StakeSplitting
from gridcoin.rpc.SideStaking import SideStaking
from gridcoin.rpc.Difficulty import Difficulty
from gridcoin._Helpers import clean_dict


class MiningInfo(_Struct):
    def __init__(self
                 , blocks=0
                 , stakeweight=None
                 , netstakeweight=0.0
                 , netstakingGRCvalue=0.0
                 , staking=True
                 , mining_error=""
                 , time_to_stake_days=0.0
                 , expectedtime=0
                 , mining_version=0
                 , mining_created=0
                 , mining_accepted=0
                 , mining_kernels_found=0
                 , masked_time_intervals_covered=0
                 , masked_time_intervals_elapsed=0
                 , staking_loop_efficiency=0.0
                 , actual_cumulative_weight=0
                 , ideal_cumulative_weight=0
                 , staking_efficiency=0.0
                 , stake_splitting=None
                 , side_staking=None
                 , difficulty=None
                 , errors=""
                 , pooledtx=0
                 , testnet=False
                 , CPID=""
                 , current_magnitude=0
                 , Magnitude_Unit=0.0
                 , BoincRewardPending=0.0
                 , researcher_status=""
                 , current_poll=""
                 ):
        self.blocks = blocks
        if stakeweight is None:
            stakeweight = dict()
        self.stakeweight = StakeWeight(**clean_dict(stakeweight))
        self.netstakeweight = netstakeweight
        self.netstakingGRCvalue = netstakingGRCvalue
        self.staking = staking
        self.mining_error = mining_error
        self.time_to_stake_days = time_to_stake_days
        self.expectedtime = expectedtime
        self.mining_version = mining_version
        self.mining_created = mining_created
        self.mining_accepted = mining_accepted
        self.mining_kernels_found = mining_kernels_found
        self.masked_time_intervals_covered = masked_time_intervals_covered
        self.masked_time_intervals_elapsed = masked_time_intervals_elapsed
        self.staking_loop_efficiency = staking_loop_efficiency
        self.actual_cumulative_weight = actual_cumulative_weight
        self.ideal_cumulative_weight = ideal_cumulative_weight
        self.staking_efficiency = staking_efficiency
        if stake_splitting is None:
            stake_splitting = dict()
        self.stake_splitting = StakeSplitting(**clean_dict(stake_splitting))
        if side_staking is None:
            side_staking = dict()
        self.side_staking = SideStaking(**clean_dict(side_staking))
        if difficulty is None:
            difficulty = dict()
        self.difficulty = Difficulty(**clean_dict(difficulty))
        self.errors = errors
        self.pooledtx = pooledtx
        self.testnet = testnet
        self.CPID = CPID
        self.current_magnitude = current_magnitude
        self.Magnitude_Unit = Magnitude_Unit
        self.BoincRewardPending = BoincRewardPending
        self.researcher_status = researcher_status
        self.current_poll = current_poll
