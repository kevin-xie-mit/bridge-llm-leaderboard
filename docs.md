<!-- ----------  Global Styles  ---------- -->
<style>
  /* 1. Center content and limit max width for readability */
  /* .wrapper{
    width:100%;
    max-width:1111px;
    margin:0 auto;
    padding:0 1rem;
  } */

  /* 2. Logo bar (top row) */
  .logo-bar{
    display:flex;
    align-items:center;
    justify-content:space-between;
    height:50px;
    margin-bottom:25px;
  }
  .logo-bar img{
    height:100%;
    max-width:100%;
    object-fit:contain;
  }

  /* 3. Generic paragraph spacing */
  p{line-height:1.6;}

  /* 4. Re-usable image section */
  .section-img{
    display:flex;
    justify-content:center;
    align-items:center;
    margin:25px 0;        /* vertical breathing room */
  }
  .section-img img{
    max-width:80%;
    height:auto;
    object-fit:contain;   /* avoid distortion */
  }

  /* 5. Make long BibTeX lines wrap instead of widening page */
  pre code{
    white-space:pre-wrap;
    word-break:break-word;
  }
</style>

<!-- ----------  Page Content  ---------- -->
<div class="wrapper">

<!-- Top logos ------------------------------------------------------------>
<div class="logo-bar">
<img src="https://cdn-uploads.huggingface.co/production/uploads/67a040fb6934f9aa1c866f99/1bNk6xHD90mlVaUOJ3kT6.png" alt="HMS" />
<img src="https://cdn-uploads.huggingface.co/production/uploads/67a040fb6934f9aa1c866f99/ZVx7ahuV1mVuIeygYwirc.png" alt="MGB" />
<img src="https://cdn-uploads.huggingface.co/production/uploads/67a040fb6934f9aa1c866f99/TkKKjmq98Wv_p5shxJTMY.png" alt="Broad" />
<img src="https://cdn-uploads.huggingface.co/production/uploads/67a040fb6934f9aa1c866f99/UcM8kmTaVkAM1qf3v09K8.png" alt="YLab" />
</div>

<!-- Background ----------------------------------------------------------->
<h2>📜 Background</h2>
<p>Recent advances in <strong>Large Language Models (LLMs)</strong> have demonstrated transformative potential in <strong>healthcare</strong>,  yet concerns remain around their reliability and clinical validity across diverse clinical tasks, specialties, and languages. To support timely and trustworthy evaluation, building upon our <a href="https://ai.nejm.org/doi/full/10.1056/AIra2400012">systematic review</a> of global clinical text resources, we introduce <a href="https://arxiv.org/abs/2504.19467">BRIDGE</a>, <strong>a multilingual benchmark that comprises 87 real-world clinical text tasks spanning nine languages and more than one million samples</strong>. Furthermore, we construct this leaderboard of LLM in clinical text understanding by systematically evaluating <strong>52 state-of-the-art LLMs</strong> (by 2025/04/28).</p>
This project is led and maintained by the team of <a href="https://ylab.top/">Prof. Jie Yang</a> and <a href="https://www.drugepi.org/team/joshua-kueiyu-lin">Prof. Kueiyu Joshua Lin</a> at Harvard Medical School and Brigham and Women's Hospital. 

<!-- Dataset illustration ------------------------------------------------->
<div class="section-img">
<img src="https://cdn-uploads.huggingface.co/production/uploads/633c70c4ccce04161f841c30/OLN3J8_Yq8dx_LrgjYSsC.png" alt="dataset" />
</div>

<!-- Leaderboard description --------------------------------------------->
<h2>🏆 BRIDGE Leaderboard</h2>
<p>BRIDGE features three leaderboards, each evaluating LLM performance in clinical text tasks under a distinct inference strategy:</p>
<ul>
    <li><strong>Zero shot</strong>: Only the task instructions and input data are  provided. The LLM is prompted to directly produce the target answer without any support.</li>
    <li><strong>Chain-of-Thought (CoT)</strong>: Task instructions explicitly guide the LLM to generate a step-by-step explanation of its reasoning process before providing the final answer, enhancing interpretability and reasoning transparency.</li>
    <li><strong>Few-shot</strong>: Five independent samples serve as examples, which leverage the LLM's capability of in-context learning to guide the model to conduct tasks. </li>
</ul>
<p>In addition, BRIDGE offers multiple <strong>model filters</strong> and <strong>task filters</strong> to enable users to explore LLM performance across <strong>different clinical contexts</strong>, empowering researchers and clinicians to make informed decisions and track model advancements over time.</p>

<!-- Leaderboard illustration -------------------------------------------->
<div class="section-img">
<img src="https://cdn-uploads.huggingface.co/production/uploads/633c70c4ccce04161f841c30/7EvHvtnfDPnzzHdPDi0L9.png" alt="model" />
</div>


<!-- Key Features --------------------------------------------------------->
<h2>🌍 Key Features</h2>
<ul>
    <li><strong>Real-world Clinical Text</strong>: All tasks are sourced from real-world medical settings, such as electronic health records (EHRs), clinical case reports, or healthcare consultations</li>
    <li><strong>Multilingual Context</strong>: 9 languages: English, Chinese, Spanish, Japanese, German, Russian, French, Norwegian, and Portuguese</li>
    <li><strong>Diverse Task Types</strong>: 8 task types: Text classification, Semantic similarity, Normalization and coding, Named entity recognition, Natural language inference, Event extraction, Question answering, and Text summarization</li>
    <li><strong>Broad Clinical Applications</strong>: 14 Clinical specialties, 7 Clinical document types, 20 Clinical applications covering 6 clinical stages of patient care</li>
    <li><strong>Advanced LLMs (52 models)</strong>:
    <ul>
        <li><strong>Proprietary models</strong>: GPT-4o, GPT-3.5, Gemini-2.0-Flash, Gemini-1.5-Pro ...</li>
        <li><strong>Open-source models</strong>: Llama 3/4, QWEN2.5, Mistral, Gemma ...</li>
        <li><strong>Medical models</strong>: Baichuan-M1-14B, meditron, MeLLaMA... </li>
        <li><strong>Reasoning models</strong>: Deepseek-R1(671B), QWQ-32B, Deepseek-R1-Distll-Qwen/Llama ...</li>
    </ul>
    </li>
</ul>
More Details can be found in our <a href="https://arxiv.org/abs/2504.19467">BRIDGE paper</a> and <a href="https://ai.nejm.org/doi/full/10.1056/AIra2400012">systematic review</a>.

<!-- Dataset access / submission ----------------------------------------->
<h2>🛠️ How to Evaluate Your Model on BRIDGE ?</h2>
<h4>📂 Dataset Access</h4>
<p>All fully open-access datasets in BRIDGE are available in <a href="https://huggingface.co/datasets/YLab-Open/BRIDGE-Open">BRIDGE-Open</a>. To ensure the fairness of this leaderboard, we publicly release the following data for each task:
Five completed samples serve as few-shot examples, and all testing samples with instruction and input information.</p>

<p>Due to privacy and security considerations of clinical data, regulated-access datasets can not be directly published. However, all detailed task descriptions and their corresponding data sources are available in our <a href="https://arxiv.org/abs/2504.19467">BRIDGE paper</a>.
Importantly, all 87 datasets have been verified to be either fully open-access or publicly accessible via reasonable request in our <a href="https://ai.nejm.org/doi/full/10.1056/AIra2400012">systematic review</a>.</p>

<h4>🔥 Result Submission and Model Evaluation</h4>
<p>If you would like to see how an unevaluated model perform on BRIDGE, please follow these steps:</p>
<ul> 
    <li><strong>Run model inference:</strong> This can be done by you locally or by us. 
        <li><strong>If you want to do inference locally:</strong> Download the <a href="https://huggingface.co/datasets/YLab-Open/BRIDGE-Open">BRIDGE-Open</a> dataset and perform inference locally. Save the generated output of each sample in its "pred" field for each dataset file. Then send your results to us via <a href="https://forms.gle/gU3GjSn9SqJRvs3b9">the Google Form</a></li>
        <li><strong>If you want us to do model inference:</strong></li> Send the link of the model to us via <a href="https://forms.gle/gU3GjSn9SqJRvs3b9">the Google Form</a>.
    <li><strong>Code Reference:</strong> About LLM inference, result extraction, and evaluation scheme, please refer to our <a href="https://github.com/YLab-Open/BRIDGE">BRIDGE GitHub repo</a>.</li> 
</ul>
We will review and evaluate your submission and update the leaderboard accordingly. 

<!-- Updates -------------------------------------------------------------->
<h2>📢 Updates</h2>
<ul>
    <li>🗓️ 2025/04/28: BRIDGE Leaderboard V1.0.0 is now live!</li>
    <li>🗓️ 2025/04/28: Our paper <a href="https://arxiv.org/abs/2504.19467">BRIDGE</a> is now available on arXiv!</li>
</ul>

<!-- Contributing --------------------------------------------------------->
<h2>🤝 Contributing</h2>
<p>We welcome and greatly value contributions and collaborations from the community!
If you have clinical text datasets that you would like to add to the BRIDEG benchmark, please fill in <a href="https://forms.gle/gU3GjSn9SqJRvs3b9">the Google Form</a> and let us know!</p>
<p>We are committed to expanding BRIDGE while strictly adhering to appropriate data use agreements and ethical guidelines. Let's work together to advance the responsible application of LLMs in medicine!</p>

<!-- Donation ------------------------------------------------------------->
<h2>🚀 Donation</h2>
<p>BRIDGE is a non-profit, researcher-led benchmark that requires substantial resources (e.g., high-performance GPUs, a dedicated team) to sustain. To support open and impactful academic research that advances clinical care, we welcome your contributions. Please contact Prof. Jie Yang at <a href="mailto:jyang66@bwh.harvard.edu">jyang66@bwh.harvard.edu</a> to discuss donation opportunities.</p>

<!-- Contact -------------------------------------------------------------->
<h2>📬 Contact Information</h2>
<p>If you have any questions about BRIDGE or the leaderboard, feel free to contact us!</p>
<ul>
    <li><strong>Leaderboard Managers</strong>: Jiageng Wu (<a href="mailto:jiwu7@bwh.harvard.edu">jiwu7@bwh.harvard.edu</a>), Kevin Xie (<a href="mailto:kevinxie@mit.edu">kevinxie@mit.edu</a>), Bowen Gu (<a href="mailto:bogu@bwh.harvard.edu">bogu@bwh.harvard.edu</a>)</li>
    <li><strong>Benchmark Managers</strong>: Jiageng Wu, Bowen Gu</li>
    <li><strong>Project Lead</strong>: Jie Yang (<a href="mailto:jyang66@bwh.harvard.edu">jyang66@bwh.harvard.edu</a>)</li>
</ul>

<!-- Citation ------------------------------------------------------------->
<h2>📚 Citation</h2>
<p>If you find this leaderboard useful for your research and applications, please cite the following papers:</p>
<pre style="white-space: pre-wrap; overflow-wrap: anywhere;"><code>@article{BRIDGE-benchmark,
    title={BRIDGE: Benchmarking Large Language Models for Understanding Real-world Clinical Practice Text},
    author={Wu, Jiageng and Gu, Bowen and Zhou, Ren and Xie, Kevin and Snyder, Doug and Jiang, Yixing and Carducci, Valentina and Wyss, Richard and Desai, Rishi J and Alsentzer, Emily and Celi, Leo Anthony and Rodman, Adam and Schneeweiss, Sebastian and Chen, Jonathan H. and Romero-Brufau, Santiago and Lin, Kueiyu Joshua and Yang, Jie},
    year={2025},
    journal={arXiv preprint arXiv: 2504.19467},
    archivePrefix={arXiv},
    primaryClass={cs.CL},
    url={https://arxiv.org/abs/2504.19467},
}
@article{clinical-text-review,
    title={Clinical text datasets for medical artificial intelligence and large language models—a systematic review},
    author={Wu, Jiageng and Liu, Xiaocong and Li, Minghui and Li, Wanxin and Su, Zichang and Lin, Shixu and Garay, Lucas and Zhang, Zhiyun and Zhang, Yujie and Zeng, Qingcheng and Shen, Jie and Yuan, Changzheng and Yang, Jie},
    journal={NEJM AI},
    volume={1},
    number={6},
    pages={AIra2400012},
    year={2024},
    publisher={Massachusetts Medical Society}
}</code></pre>
<p>If you use the datasets in BRIDGE, please also cite the original paper of datasets, which can be found in our BRIDGE paper.</p>

</div>
<!-- ----------  End of Page Content  ---------- -->