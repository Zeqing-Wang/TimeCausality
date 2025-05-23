JUDGE_PROMPT = """
You will be given a ground truth and model output couple.
Your task is to provide a 'total rating' scoring how well the model output matches the semantic meaning of the ground truth.
Give your answer as an integer on a scale of 0 to 5, where 0 means that the model output is completely unrelated to the ground truth, and 5 means that the model output perfectly matches the semantic meaning of the ground truth.

Provide your feedback as follows:

Feedback:::
Total rating: (your rating, as an integer between 0 and 5)

Now here are the ground truth and model output.

Ground Truth: {ground_truth}
Model Output: {model_output}

Feedback:::
Total rating: """
import argparse
import os
import json
import re
import pandas as pd
from tqdm.auto import tqdm
from datasets import load_dataset
from openai import OpenAI
from huggingface_hub import InferenceClient, notebook_login
client = OpenAI(api_key='YOUR_API_KEY', base_url='http://0.0.0.0:23333/v1')
model_name = client.models.list().data[0].id
def request_single(prompt):
    response = client.chat.completions.create(
        model=model_name,
        messages=[{
            'role':
            'user',
            'content': [{
                'type': 'text',
                'text': prompt,
            }],
        }],
        temperature=0.8,
        top_p=0.8)
    return response.choices[0].message.content

def extract_judge_score(answer: str, split_str: str = "Total rating:") -> int:
    try:
        if split_str in answer:
            rating = answer.split(split_str)[1]
        else:
            rating = answer
        digit_groups = [el.strip() for el in re.findall(r"\d+(?:\.\d+)?", rating)]
        return float(digit_groups[0])
    except Exception as e:
        print(e)
        return None
    
def judge_two_sentence(label, output):
    JUDGE_PROMPT_SEND = JUDGE_PROMPT.format(ground_truth = label, model_output = output)
    res = request_single(prompt=JUDGE_PROMPT_SEND)
    res = extract_judge_score(answer=res)
    return res
    pass

def parse_args():
    parser = argparse.ArgumentParser(description="Visual Common Sense Evaluation Script")
    
    parser.add_argument("--data_root", type=str, required=True,
                       help="Path to the folder containing input images")
    parser.add_argument("--judge_file", type=str, required=True,
                       help="Root directory containing the concat_images folders")
    return parser.parse_args()


# Test your LLM client
def main():
    args = parse_args()
    data_root = args.data_root
    judge_file = args.judge_file
    res = json.load(open(judge_file, "r"))
    output_path = judge_file.replace('.json','_judged.json')
    res_output = []
    for r in tqdm(res):
        # coco_num = r['image_name'].split('_')[0]
        # coco_object = r['image_name'].split('_')[1].split('.jpg')[0]
        
        coco_num = r['image_name']['coco_number']
        coco_object = r['image_name']['label']
        
        
        anno_json_path = os.path.join(data_root, coco_num, 'casual_formmoted_res_v2_gpt-4o.json')
        annos_json = json.load(open(anno_json_path, "r"))
        # print('coco object:',coco_object)
        # print('annos_json:', annos_json)
        for anno_json_ in annos_json:
            # print('label:', anno_json_['label'])
            if anno_json_['label'] == coco_object:
                anno_json = anno_json_
                break
            # assert False, 'No Label'
        answer_reason_label = anno_json["rationales"]
        answer_infer_label = anno_json["operation"]
        answer_reason = r['answer_reason']
        answer_infer = r['answer_infer']
        
        answer_reason_score = judge_two_sentence(label=answer_reason_label, output=answer_reason)
        answer_infer_score = judge_two_sentence(label=answer_infer_label, output=answer_infer)
        
        r['answer_reason_label'] = answer_reason_label
        r['answer_infer_label'] = answer_infer_label
        
        r['reason_score'] = answer_reason_score
        r['infer_score'] = answer_infer_score
        res_output.append(r)
    
        
    # print(judge_two_sentence(label=label, output=output))
    json.dump(res_output, open(output_path, "w"))
    pass

if __name__ == "__main__":
    main()