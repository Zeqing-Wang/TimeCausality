# deploy the vlms

# deploy the llm on port 23333 with command:
# CUDA_VISIBLE_DEVICES=0 lmdeploy serve api_server Llama-3.1-8B-Instruct --backend turbomind --server-port 23333"


model_root='' # Your model root path

vlm_port=23351

vlm_names=('InternVL2-8B' 'InternVL2_5-4B' 'InternVL2_5-8B' 'Phi-3.5-vision-instruct' 'Qwen2-VL-2B-Instruct' 'Qwen2-VL-7B-Instruct' 'InternVL2_5-26B')



vlm_names=('InternVL2-4B')

for vlm_name in "${vlm_names[@]}"
do
    model_path="${model_root}/${vlm_name}"
    # question setting
    question_template='Question: In the given image, the bottom and top sides depict the states of the same {} at different points in time. Based on the progression of time, which sequence is correct?
                    Only consider natural, long-term changes (e.g., aging, oxidation, rust, or physical degradation). Ignore any possibilities of digital alterations, retouching, or external modifications.
                    Choices:
                    A. From bottom to top (Bottom happens first, top happens later). 
                    B. From top to bottom (Top happens first, bottom happens later). 
                    Output only in a single letter. (A or B) .'
    reason_question_template='Why does the {} in the scene on the top occur after the one on the bottom? Answer in one sentence.'
    infer_question_template='What caused the transition from the {} on the bottom to the {} on the top? Answer in one sentence.'
    
    
    version_name="{}"

    # image setting
    image_folder="{}"
    data_root="{}"
    saved_images="{}"
    json_ann_root="{}"
    # output setting
    output_root="./${version_name}"
    output_model_path="${output_root}/${vlm_name}"
    output_json="${output_model_path}/step_2.json"
    judged_json="${output_model_path}/step_2_judged.json"
    output_final="${output_model_path}/report.json"

    if [ ! -d "$output_root" ]; then
        mkdir -p "$output_root"
        echo "Make Dir: $output_root"
    else
        echo "Dir Existing: $output_root"
    fi

    if [ ! -d "$output_model_path" ]; then
        mkdir -p "$output_model_path"
        echo "Make Dir: $output_model_path"
    else
        echo "Dir Existing: $output_model_path"
    fi

    echo "CUDA_VISIBLE_DEVICES=0 lmdeploy serve api_server \"${model_path}\" --backend turbomind --server-port $vlm_port"

    CUDA_VISIBLE_DEVICES=0 lmdeploy serve api_server "${model_path}" --backend turbomind --server-port $vlm_port& # --session-len 4096& #  --cache-max-entry-count 0.25

    # exit 1
    LM_PID=$!


    sleep 30
    python unify_infer_benchmark_choice_args_gpt4o.py \
        --image_folder "${image_folder}" \
        --data_root "${data_root}" \
        --output_json "${output_json}" \
        --question_template "${question_template}"\
        --reason_question_template "${reason_question_template}"\
        --infer_question_template "${infer_question_template}"\
        --vlm_api_port "${vlm_port}" \
        --saved_images "${saved_images}"

    python infer_llm_score_args.py \
        --data_root "${json_ann_root}" \
        --judge_file "${output_json}" \


    python eval_benchmark_top_down_args_a_b.py \
        --ref_image_folder "${image_folder}" \
        --eval_json "${judged_json}" \
        --output_final "${output_final}" 

    kill $LM_PID
    sleep 20
done