dataset=NICOMixed
command=$1
data_dir=$2
gpu_id=$3

CUDA_VISIBLE_DEVICES=${gpu_id} \
python3 -m domainbed.scripts.sweep ${command}\
       --datasets ${dataset}\
       --algorithms W2D\
       --data_dir ${data_dir}\
       --command_launcher local\
       --fixed_val_envs 2\
       --fixed_test_envs 3\
       --steps 5001\
       --holdout_fraction 0.1\
       --n_hparams 10\
       --n_trials 3\
       --skip_confirmation\
       --hparams "$(<sweep/${dataset}/hparams.json)"\
       --output_dir "sweep/${dataset}/outputs"