# TimeCausality: Evaluating the Causal Ability in Time Dimension for Vision Language Models

This repository contains the code and dataset for our paper:

**TimeCausality: Evaluating the Causal Ability in Time Dimension for Vision Language Models**  
Zeqing Wang*, Shiyuan Zhang*, Chengpei Tang, Keze Wang  
(*Equal contribution)

📑[[Preprint (arXiv:2505.15435)](https://arxiv.org/abs/2505.15435)]

🔥[[Data (Google Drive)](https://drive.google.com/drive/folders/1B-27lPEA8QSWH1Ta8OkZSXfkJCZCi051?usp=sharing)]

## 🔍 Overview

**TimeCausality** is a benchmark for evaluating Vision-Language Models (VLMs) on their ability to reason about **irreversible temporal changes** such as fruit spoilage, aging, and rusting.

We categorize causal transformations into five types:
- **Physical Change (PC)**
- **Chemical Change (CC)**
- **Natural Phenomenon (NP)**
- **Environmental Modification (EM)**
- **Artificial Processing (AP)**

Each sample includes:
- An image pair (before and after)
- Object name
- Causal type
- Reasoning rationale (Why)
- Inferring rationale (What caused it)

## 🧪 Evaluation Aspects

We assess models across **three key reasoning dimensions**:

| Aspect | Task Description |
|--------|------------------|
| Aspect I | Temporal Order Judgment: Which image came first? (Multi-choice) |
| Aspect II | Causal Reasoning: Why did the change happen? (Free-text) |
| Aspect III | Cause Inferring: What caused the change? (Free-text) |

---

## 📊 Model Performance Summary

### Overall Evaluation (Across All Types)

| Model Name              | ACC (I) | F1 Score (I) | Reasoning Score (II) | Inferring Score (III) |
|-------------------------|---------|--------------|------------------------|------------------------|
| **GPT-4o**              | 70.86%  | **67.83%**   | **2.45**               | **2.80**               |
| GPT-4o-mini             | 98.57%  | 34.56%       | 2.04                   | 2.37                   |
| Qwen2.5-VL-7B-Instruct  | 41.14%  | 55.13%       | 2.23                   | 2.29                   |
| LLaVA-v1.6-13B          | 50.00%  | 51.42%       | 1.01                   | 1.24                   |
| InternVL2.5-8B          | 26.57%  | 49.13%       | 1.59                   | 1.91                   |
| Llama3.2-Vision-11B     | 79.14%  | 29.67%       | 1.02                   | 2.38                   |
| Phi-3.5-Vision          | 69.71%  | 36.76%       | 0.44                   | 0.76                   |

---

### Breakdown by Causal Type (GPT-4o)

| Type                  | ACC (I) | F1 Score (I) | Reasoning Score (II) | Inferring Score (III) |
|-----------------------|---------|--------------|------------------------|------------------------|
| Chemical Change (CC)  | 83.33%  | 66.90%       | 2.85                   | 2.83                   |
| Environmental Mod. (EM)| 56.82% | 67.05%       | **3.05**               | **3.86**               |
| Artificial Processing (AP)| 75.00% | 68.63%    | 1.50                   | 2.50                   |
| Natural Phenomenon (NP)| 80.34% | 68.38%       | 1.39                   | 1.44                   |
| Physical Change (PC)  | 73.33%  | 66.52%       | **3.18**               | **3.24**               |

---

### Breakdown by Causal Type (Qwen2.5-VL-7B)

| Type                  | ACC (I) | F1 Score (I) | Reasoning Score (II) | Inferring Score (III) |
|-----------------------|---------|--------------|------------------------|------------------------|
| Chemical Change (CC)  | 25.00%  | 50.71%       | 2.67                   | 2.60                   |
| Environmental Mod. (EM)| 50.76% | 59.51%       | 2.72                   | **3.31**               |
| Artificial Processing (AP)| 62.50% | **80.57%** | 2.63                   | 2.50                   |
| Natural Phenomenon (NP)| 37.61% | 46.92%       | 1.32                   | 0.79                   |
| Physical Change (PC)  | 35.56%  | 61.21%       | **2.64**               | **2.84**               |

---


## 📁 Dataset

- **700 Image Pairs** across 5 causal categories
- Each sample includes temporal image pair, object name, type, reasoning, and inferring rationale
- All samples verified manually for quality

Data examples and generation pipeline are shown in the paper and appendix.

## 🧭Instruction for evaluation

### Step 1 Deploy your model
In our provided official script, we use deploy package (like [LM Deploy](https://github.com/InternLM/lmdeploy) or [VLLM](https://github.com/vllm-project/vllm/)) to server an openai-like api.

For example, the LM Deploy start with:
```
CUDA_VISIBLE_DEVICES=0 lmdeploy serve api_server \"${model_path}\" --backend turbomind --server-port $vlm_port
```


### Step 2 Download our TimeCasusality and Prepare the data format
Download the images with the corresponding annoataion file in [Data (Google Drive)](https://drive.google.com/drive/folders/1B-27lPEA8QSWH1Ta8OkZSXfkJCZCi051?usp=sharing)

All the images concat with the 'Modified Image' & 'Original Image'

### Step 2.5 Deploy the LLM Judger
In a similar method, you need to provide an api for revoking the LLM (we use Llama3 8B in the current leaderboard).

### Step 3 Invoke the deployed api servers
Benchmarking the VLM via the deployed api.


⚠️ [Note] You may need to refer the 'args_infer_and_eval_gpt4o.sh' for a better understanding.

## 💾 Coming Soon

- ~~Release the Dataset~~
- ~~Evaluation scripts for open-source VLMs~~
- ~~Instruction for evaluation~~

## 📊 Full Benchmark Results on TimeCausality

### Open-Source Vision Language Models

| Model                          | ACC    | ACC-R  | Group | F1     | Reasoning | Inferring |
|-------------------------------|--------|--------|-------|--------|-----------|-----------|
| Mono-InternVL-2B              | 62.86  | 34.57  | 20.00 | 47.67  | 0.83      | 1.34      |
| InternVL2-4B                  | 51.71  | 47.14  | 24.86 | 49.40  | 0.60      | 0.67      |
| InternVL2-8B                  | 62.86  | 36.00  | 22.00 | 48.50  | 0.57      | 1.02      |
| InternVL2.5-4B                | 45.43  | 45.71  | 24.86 | 45.57  | 1.12      | 1.16      |
| InternVL2.5-8B                | 26.57  | 78.57  | 20.86 | 49.13  | 1.59      | 1.91      |
| Qwen2-VL-2B-Instruct          | 43.71  | 59.14  | 27.71 | 51.14  | 0.76      | 1.13      |
| Qwen2-VL-7B-Instruct          | 21.43  | 78.29  | 16.00 | 45.45  | 0.87      | 1.31      |
| Qwen2.5-VL-3B-Instruct        | 49.43  | 52.29  | 26.29 | 50.85  | 1.55      | 1.58      |
| Qwen2.5-VL-7B-Instruct        | 41.14  | 71.14  | 28.00 | 55.13  | 2.23      | 2.29      |
| CogVLM2-LLaMA3-Chat-19B       | 50.86  | 22.00  | 12.86 | 35.08  | 0.62      | 1.11      |
| LLaMA3.2-Vision-11B           | 79.14  | 1.43   | 1.43  | 29.67  | 1.02      | 2.38      |
| LLaVA-v1.6-7B                 | 66.29  | 29.43  | 19.14 | 46.02  | 0.96      | 0.72      |
| LLaVA-v1.6-13B                | 50.00  | 52.86  | 25.43 | 51.42  | 1.01      | 1.24      |
| GLM4-9B                       | 59.71  | 27.14  | 14.29 | 41.89  | 1.32      | 1.76      |
| Phi-3-Vision-128k-Instruct    | 81.71  | 15.14  | 10.86 | 42.00  | 0.65      | 0.84      |
| Phi-3.5-Vision-Instruct       | 69.71  | 13.71  | 8.86  | 36.76  | 0.44      | 0.76      |

---

### Closed-Source Vision Language Models

| Model        | ACC    | ACC-R  | Group | F1     | Reasoning | Inferring |
|--------------|--------|--------|-------|--------|-----------|-----------|
| GPT-4o-mini  | 98.57  | 1.43   | 1.43  | 34.56  | 2.04      | 2.37      |
| GPT-4o       | 70.86  | 64.86  | 43.43 | 67.83  | 2.45      | 2.80      |

---

### Contrastive Learning Based VLMs (CLIP)

| Model                          | ACC    | ACC-R  | Group | F1     |
|--------------------------------|--------|--------|-------|--------|
| CLIP ViT-B/16                 | 42.86  | 56.86  | 9.14  | 49.61  |
| CLIP ViT-B/32                 | 32.29  | 60.86  | 8.29  | 45.46  |
| CLIP ViT-L/14-336             | 15.42  | 85.14  | 6.28  | 43.41  |

---

*ACC = Accuracy on original image pair  
*ACC-R = Accuracy on reversed image pair  
*Group Score = both orders correct  
*F1 Score = consistency-aware average  
*Reasoning / Inferring Scores ∈ [0, 5], rated by LLM-as-a-Judge

## 📌 Citation

If you find the code useful for your work, please star this repo and consider citing:

```bibtex
@misc{wang2024timecausality,
  title={TimeCausality: Evaluating the Causal Ability in Time Dimension for Vision Language Models},
  author={Zeqing Wang and Shiyuan Zhang and Chengpei Tang and Keze Wang},
  year={2024},
  eprint={2505.15435},
  archivePrefix={arXiv},
  primaryClass={cs.CV}
}