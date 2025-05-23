import os
import json
from typing import Dict, List
import json
from openai import OpenAI
import base64
import os
from tqdm import tqdm

import os
import json
import argparse
from typing import List, Dict
from tqdm import tqdm



def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')  
    
def request_single(image_path, prompt, client, model_name):
    base64_image = encode_image(image_path=image_path)
    response = client.chat.completions.create(
        model=model_name,
        messages=[{
            'role':
            'user',
            'content': [{
                'type': 'text',
                'text': prompt,
            }, {
                'type': 'image_url',
                'image_url': {
                    'url':
                    f"data:image/jpeg;base64,{base64_image}",
                    # "max_pixels": 1000000
                },
            }],
        }],
        temperature=0.8,
        top_p=0.8)
    return response.choices[0].message.content
    
    pass


def parse_args():
    parser = argparse.ArgumentParser(description="Visual Common Sense Evaluation Script")
    
    parser.add_argument("--image_folder", type=str, required=True,
                       help="Path to the folder containing input images")
    parser.add_argument("--data_root", type=str, required=True,
                       help="Root directory containing the concat_images folders")
    parser.add_argument("--saved_images", type=str, required=True,
                       help="Root directory containing the concat_images folders")
    parser.add_argument("--output_json", type=str, required=True,
                       help="Path to the output JSON file for saving results")
    parser.add_argument("--question_template", type=str, required=True,
                       help="Question template with {} placeholder for content")
    parser.add_argument("--reason_question_template", type=str, required=True,
                       help="Question template with {} placeholder for content")
    parser.add_argument("--infer_question_template", type=str, required=True,
                       help="Question template with {} placeholder for content")
    parser.add_argument("--vlm_api_port", type=str, required=True,
                       help="vlm server api")
    return parser.parse_args()

def main():
    args = parse_args()
    client = OpenAI(api_key='YOUR_API_KEY', base_url='http://0.0.0.0:{}/v1'.format(args.vlm_api_port))
    model_name = client.models.list().data[0].id
    # 用于存储所有结果的列表
    results: List[Dict] = []
    data_root = args.data_root
    saved_images = args.saved_images
    image_folder = args.image_folder
    output_json = args.output_json
    json_content = json.load(open(data_root, 'r'))
    # 遍历图像文件夹
    image_names = os.listdir(args.image_folder)
    from tqdm import tqdm
    for image_name in tqdm(json_content):
        content = image_name['label'].replace(' ','_')
        saved_image_path = os.path.join(saved_images, image_name['coco_number']+'_'+image_name['label'].replace(' ','_')+'.jpg')
        # if image_name['coco_number'] == '000000000776':
        #     print('saved_image_path:', saved_image_path)
        if not os.path.exists(saved_image_path):
            continue
        
        # concat_images_dir = os.path.join(image_folder, base_name, "concat_images")
        image_left = os.path.join(image_folder, f"{image_name['coco_number']}_{content}_concat_h_after_first.jpg")
        image_right = os.path.join(image_folder, f"{image_name['coco_number']}_{content}_concat_h_first_after.jpg")
        
        # 检查图像是否存在
        if not os.path.exists(image_left) or not os.path.exists(image_right):
            print(image_left, image_right)
            print(f"Skipping {image_name}: Images not found.")
            continue
        
        
        current_question = args.question_template.format(content)
        reason_question = args.reason_question_template.format(content)
        infer_question = args.infer_question_template.format(content, content)
        print('For Multi Choice Eval:',current_question)
        print('For Reason Eval:', reason_question)
        print('For Infer Eval:', infer_question)

        

        answer_simple_gt_a = request_single(image_path=image_left, prompt = current_question, client=client,model_name=model_name)
        answer_simple_gt_b = request_single(image_path=image_right, prompt = current_question,client=client, model_name=model_name)
        print('answer simple gt_a:', answer_simple_gt_a)
        
        answer_reason = request_single(image_path=image_left, prompt=reason_question, client=client,model_name=model_name)
        answer_infer = request_single(image_path=image_left, prompt=infer_question, client=client,model_name=model_name)
        

        result = {
            "image_name": image_name,
            "answer_simple_gt_b": answer_simple_gt_b.lower(),
            "answer_simple_gt_a": answer_simple_gt_a.lower(),
            "answer_reason": answer_reason,
            "answer_infer": answer_infer
        }
        

        results.append(result)
        

        if len(results) % 10 == 0:
            with open(output_json, "w") as f:
                json.dump(results, f, indent=4)
            print(f"Saved results for {len(results)} images.")

    # 最终保存所有结果
    with open(output_json, "w") as f:
        json.dump(results, f, indent=4)
    print(f"All results saved to {output_json}.")

if __name__ == "__main__":
    main()