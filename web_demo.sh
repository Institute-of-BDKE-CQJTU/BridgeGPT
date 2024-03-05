PRE_SEQ_LEN=128

CUDA_VISIBLE_DEVICES=0 python web_demo.py \
    --model_name_or_path ./models/chatglm2-6b \
    --ptuning_checkpoint ./checkpoint-300 \
    --pre_seq_len $PRE_SEQ_LEN