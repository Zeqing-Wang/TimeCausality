import json
import os
import re
import argparse

def extract_and_uppercase_letter(text):
    match = re.search(r'[A-Da-d]', text)
    if match:
        return match.group().upper()
    else:
        return None  

def parse_args():
    parser = argparse.ArgumentParser(description="Visual Common Sense Evaluation Metrics Calculator")
    parser.add_argument("--ref_image_folder", type=str, required=True,
                       help="Path to the reference image folder for filtering")
    parser.add_argument("--eval_json", type=str, required=True,
                       help="Path to the evaluation JSON file containing results")
    parser.add_argument("--output_final", type=str, required=True,
                       help="report results")
    return parser.parse_args()

def main():
    args = parse_args()
    
    res = json.load(open(args.eval_json, "r"))
    
    total_reason_score = 0
    total_infer_score = 0
    total_acc_a = 0
    total_acc_b = 0
    total_group_acc = 0
    total_eval_count = 0
    
    # ref_images = os.listdir(args.ref_image_folder)
    for r in res:

            
        re_answer_simple_gt_a = extract_and_uppercase_letter(r['answer_simple_gt_a'])
        re_answer_simple_gt_b = extract_and_uppercase_letter(r['answer_simple_gt_b'])
        
        if re_answer_simple_gt_b == 'B':
            total_acc_b += 1
        if re_answer_simple_gt_a == 'A':
            total_acc_a += 1
        if re_answer_simple_gt_b == 'B' and re_answer_simple_gt_a == 'A':
            total_group_acc += 1
            
            
        total_reason_score += r['reason_score']
        total_infer_score += r['infer_score']
            
            
        total_eval_count += 1
        
        



    tp_a = total_acc_a
    fp_a = total_eval_count - total_acc_b  
    fn_a = total_eval_count - total_acc_a  


    tp_b = total_acc_b
    fp_b = total_eval_count - total_acc_a  
    fn_b = total_eval_count - total_acc_b  

    def calculate_f1(tp, fp, fn):
        if tp + fp == 0 or tp + fn == 0:
            return 0.0  # 避免除零错误
        precision = tp / (tp + fp) if (tp + fp) != 0 else 0
        recall = tp / (tp + fn) if (tp + fn) != 0 else 0
        if precision + recall == 0:
            return 0.0
        return 2 * (precision * recall) / (precision + recall)


    f1_a = calculate_f1(tp_a, fp_a, fn_a)
    f1_b = calculate_f1(tp_b, fp_b, fn_b)


    macro_f1 = (f1_a + f1_b) / 2
    
    # Report the Benchmark
    print("*"*30)
    print("Acc B: ", total_acc_b/total_eval_count)
    print("Acc A: ", total_acc_a/total_eval_count)
    print("Acc Group: ", total_group_acc/total_eval_count)
    print(f"Macro-F1: {macro_f1:.4f}")
    print("Avg. Reason Score: ", total_reason_score/total_eval_count)
    print("Avg. Infer Score: ", total_infer_score/total_eval_count)
    print("*"*30)

    report = {
        'acc_a' : total_acc_a/total_eval_count,
        'acc_b' : total_acc_b/total_eval_count,
        'acc_group' : total_group_acc/total_eval_count,
        'Macro-F1' : macro_f1,
        'Avg_Reason_Score' : total_reason_score/total_eval_count,
        'Avg_Infer_Score' : total_infer_score/total_eval_count
    }
    json.dump(report, open(args.output_final, "w"))
    
if __name__ == '__main__':
    main()