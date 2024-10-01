# dsa4262-genomesight


## DSA4262 Sense-making Case Analysis: Health and Medicine - Data Science in Genomics - 2024

### Genomics Project: Prediction of m6A RNA modifications from direct RNA-Seq data

#### Project Overview

In this project, you will develop a machine learning method to identify m6A RNA modifications from direct RNA sequencing data. The method will then be applied to analyze data from the SG-NEx project.

#### Task 1: Develop a machine learning method to identify RNA modifications from direct RNA-Seq data

Write a computational method that predicts m6A RNA modification from direct RNA-Seq data. The method should be able to train a new model and make predictions on unseen test data. Specifically, your method should fulfill the following requirements:

* **Two Scripts:** Your method should contain two scripts: one for model training and one for making predictions. The prediction script will be evaluated by other students.
* **Model Training Script:**
    * **Input:**
        * Direct RNA-Seq data processed by m6Anet (in JSON format, see below)
        * m6A labels (see below for format)
    * **Output:** The trained model (any format of your choice)
* **Prediction Script:**
    * **Input:**
        * Direct RNA-Seq data processed by m6Anet (in JSON format, see below)
        * Optional: The pre-trained model from the first script could be used as an input argument (it can also be accessed within the code directly instead)
    * **Output:** Predicted m6A sites (see below for specific output file requirements)
* **Code Availability and Documentation:**
    * **Public GitHub Repository:** The code needs to be accessible through a public GitHub repository at the time of submission.
    * **Executable Code:** The code needs to be executable.
    * **Documentation:** The repository needs to be documented.
        * **Installation:** How to install the code/software and any requirements
        * **Running:** How to run the code
        * **Test Data:** Provide a small test data set to run the code (for the prediction script only, this is not required for the training script).
        * **Evaluation:** The code and documentation will be evaluated by other students on an AWS Ubuntu machine.

#### Format Description

* **Direct RNA-Seq Data (data.json):**

Each line of data.json describes the nanopore direct RNA sequencing reads that are aligned to the reference transcript sequences. Each line corresponds to one position in a transcript and shows the data from all reads that are aligned to this position.

Each line is formatted as follows:

```json
{"ENST00000000233":{"244":{"AAGACCA":[[0.00299,2.06,125.0,0.0177,10.4,122.0,0.0093,10.9,84.1],[0.00631,2.53,125.0,0.00844,4.67,126.0,0.0103,6.3,80.9],[0.00465,3.92,109.0,0.0136,12.0,124.0,0.00498,2.13,79.6],[0.00398,2.06,125.0,0.0083,5.01,130.0,0.00498,3.78,80.4],[0.00664,2.92,120.0,0.00266,3.94,129.0,0.013,7.15,82.2],[0.0103,3.83,123.0,0.00598,6.45,126.0,0.0153,1.09,74.8],[0.00398,3.75,126.0,0.00332,4.3,129.0,0.00299,1.93,81.9],[0.00498,3.93,127.0,0.00398,2.51,131.0,0.0111,3.47,79.4] … }
```

Going from the start of the line to the end, we have the following quantities of interest:

* **ENST00000000233:** The transcript ID for this particular row of data.json
* **244:** Represents the position within transcript ENST00000000233 which is described by the features in this line.
* **AAGACCA:** Describes the combined nucleotides from the neighboring flanking position (positions 243, 244, and 245 of the transcript ENST00000000233). At each position, 5 nucleotides (5-mers) pass through the pore; the sequence of the corresponding 5-mers represented by AAGACCA will be AAGAC (position 243), AGACC (position 244), GACCA (position 245). The middle 5-mer of the sequence (in this case AGACC), will always be one of the 18 DRACH motifs (D=A,G, or T, R=A or G, while H is A, C, or T).
* **Nested List of Numbers:** Represents the features extracted from each read that is mapped to transcript ENST00000000233 at position 243 (1- flanking position), 244 (the central position), and 245 (the +1 flanking position). Each feature was summarized from the raw signal data corresponding to positions 243, 244, and 245 of the transcript. The features from the first read will be [0.00299,2.06,125.0,0.0177,10.4,122.0,0.0093,10.9,84.1], from the second read will be [0.00631,2.53,125.0,0.00844,4.67,126.0,0.0103,6.3,80.9], and so on.
* **Features:** Each position is described using 3 features: (1) length of the direct RNA-Seq signal of the 5-mer nucleotides (dwelling time), (2) standard deviation of the direct RNA-Seq signal, and (3) mean of the direct RNA-Seq signal.
* **Reads:** For each read, we have extracted features from segments corresponding to the -1 flanking position (243), the central position (244), and the +1 flanking position, resulting in a total of 9 features for each read (3 features for position 243, followed by 3 features for positions 244 and 245 respectively).

* **m6A Labels for Training (data.info):**

The m6A labels for training are given as a data.info file with the following format:

```
gene_id,transcript_id,transcript_position,label
ENSG00000004059,ENST00000000233,244,0
ENSG00000004059,ENST00000000233,261,0
ENSG00000004059,ENST00000000233,316,0
```

Each line describes the coordinates of one position in the transcriptome that can be modified by m6A, and the respective modification label:

* **gene_id:** The gene associated with the transcript (as given by the transcript_id)
* **transcript_id:** The transcript ID
* **transcript_position:** The position in the transcript
* **label:** Describes whether a specific position within a transcript has the m6A modification. The label will be 0 if the position is unmodified and 1 if the position has the m6A modification. Modification labels are obtained using m6ACE-Seq.

The labels (data.info) and the signal data (data.json) can be matched using the transcript_id and transcript_position columns.

* **Predicted m6A Sites:**

The following format is expected for the submitted predictions:

```
transcript_id,transcript_position,score
ENST00000005260,425,0.03794821493241728
ENST00000005260,467,0.03789510558677051
ENST00000005260,542,0.08970181109437239
ENST00000005260,585,0.014504787924707616
```

* **CSV Format:** The file has to be in csv format, separated by ",".
* **Matching Data:** The values from the columns transcript_id and transcript_position must exactly match the transcript ids and positions in data.json.
* **Score:** The column score describes the probability that the given site has the m6A modification, so it must be a floating point with a value between 0 and 1.

* **Model:**

You can save the model during model training in any format.

#### Training Data:

Training data from the Hct116 colon cancer cell line will be made available.

#### Task 2: Prediction of m6A sites in all SG-NEx direct RNA-Seq data sets

Predict m6A RNA modifications in all direct RNA-Seq data sets from the SG-NEx data using your method. Describe the results and compare them across the different cell lines. Summarize and visualize your observations.

All data is available as .json files through the SG-NEx project: [https://github.com/GoekeLab/sg-nex-data](https://github.com/GoekeLab/sg-nex-data) which is hosted on AWS ([https://registry.opendata.aws/sgnex/](https://registry.opendata.aws/sgnex/)).

Please refer to the data access tutorial for information on how to access these files.

#### Resources and Cloud Usage (AWS)

Please use AWS for the project as the evaluation will also be done on an AWS ubuntu instance. Each team will get US$100 AWS credit per student. The AWS credits need to be sufficient for the team project and for the student evaluation of other teams. The budget will only be managed at the team level, therefore any team member can use up all AWS credits for the team.

#### Submission and Assessment

##### Intermediate Leaderboard

There will be an intermediate submission and leaderboard. We will provide new data (json format) and evaluate your predictions (csv file, see format requirement above) on these data. Additional information will be made available with the evaluation data release.

* **Submissions are due:** Oct 16th, 23.59pm. No questions will be answered between Oct 14th 9pm and Oct 16th; please ask any questions during the class on October 14th.

##### Final Leaderboard

For the final submission, we will provide new data (json format) and evaluate your predictions (text file, see format requirement above) on these data. Additional information will be made available with the evaluation data release.

* **Submissions are due:** Nov 6th, 23.59pm. No questions will be answered between Nov 4th 9pm and Nov 6th; please ask any questions during the class on November 4th.

#### Project Team Submission Requirements

1. **Report**

Please submit a report that summarizes your work, methods, and results. The report should include the following sections:

* **Title**
* **Introduction**
    * **Problem Statement**
* **Methods**
    * Describe the machine learning model that was used for the final submission and data analysis task.
    * Describe the data sets that you analyzed for Task 2 and how they were analyzed.
* **Results (1): Model Evaluation**
    * Describe the performance of your model on the data that is provided for model training, using independent training and test data.
    * Compare the final model against a simple baseline model.
    * If you optimized your model, you can compare the final model against intermediate models that your team developed to show the improvements.
* **Results (2): Application on the SG-NEx data**
    * Describe the results obtained when you apply your model on the available SG-NEx data.
* **Discussion**
* **References**
* **Code Availability**
    * Please include the link to the code repository.
    * The link should include complete documentation to predict m6A probabilities on a test data set.
* **Use of AI Methods:** AI tools are allowed to be used for all tasks. If you use such a tool, please make sure that no code or text is copied from a public source without acknowledgment. Please document how AI tools were used as a table in the following format:

    | AI Tool used | Prompt and output | How the output was used in the assignment |
    |---|---|---|
    | Tool 1 | ... | ... |

The report should not exceed 5 pages, excluding the title page (optional), table of content (optional), and references. The report should be written in Arial font size 11 (Arial font size 9-11 for figure captions, tables, references).

2. **Reproducible Code**

Please make the final code, documentation, and test data set accessible through GitHub and provide full documentation on how to learn a model and how to make predictions.

The code to make m6A predictions will be tested by other students using an AWS ubuntu machine (the training script will not be tested).

3. **Presentation**

Please record a presentation of length 10 minutes. The presentation should cover the following:

* **Introduction:** Introduce your team and team members.
* **Background/Motivation**
* **Results Task 1:** Describe your approach and how you evaluated your method.
* **Results Task 2:** Describe 1 or 2 key findings.
* **Optional:** Include a short demo on how to run your method.
* **Summary:** Summarize your presentation.

The presentation will be made available to other teams that will test the code.

* **Submissions are due:** Nov 6th (Wednesday), 23.59pm. No questions will be answered after Nov 4th 9pm; please ask any questions during the class on November 4th.

#### Individual Submission Requirements

1. **Teamwork Summary (Canvas)**

This summary will be treated as confidential and will not be shared with any other student.

* Briefly describe the contribution for each team member in 1-3 sentences.
* Please rate each team member from 1-5:
    * 5: The team member was outstanding, leading the team effort, or contributing the most important ideas and solutions. Please rate one student with a 5.
    * 4: The team member was actively involved and contributed ideas and solutions that were essential to the team's final submission.
    * 3: The team member was actively involved and helped with tasks that were essential to the team's final submission.
    * 2: The team member was only passively involved in the team's solution with a smaller or minor contribution.
    * 1: Team member was not or only minimally involved, not cooperating, or frequently absent.

* **Submissions is due:** Nov 7th (Thursday), 23.59pm. (one day after the team submission)

2. **Student Evaluation**

Each student will be assigned to review a presentation, execute the code, and reproduce minimal results from another team. Please refer to the student evaluation guidelines.

#### Assessment Components (total: 80%)

* **Report (30%)**
* **Presentation (10 minutes, recorded) (10%)**
* **Documentation: Code needs to be executable and results need to be reproducible (10%)**
* **Model Performance:** Results will be evaluated using an unknown test dataset and compared against a random classifier and a simple baseline model (with ROC AUC and Precision-Recall AUC) (15%). The ranking in comparison with other teams will not be used for grading.
* **Class Participation by Team (10%)**
    * Participation in hackathon sessions
    * Each team has to submit at least 1 question live during each industry session.
    * Please ask the question live and post in the respective slack channel (announced on the day).
* **Individual Component (5%)**
    * Each student is expected to attend in person and actively contribute to the project solution.
    * Each student should have a specific contribution in report writing, model development, and implementation.
    * Evaluation will be based on confidential peer reports.
* **AWS overspending will lead to a deduction by 5%.**

The project will be evaluated based on the clarity and presentation, the domain understanding, the methodology, the innovativeness, and creativity. The final ranking in comparison with other teams will not be used for grading.

#### Tips, Further Reading, and Additional Information

Please refer to the slides from the project presentation, which highlights challenges, tips, and additional links. The SG-NEx project is described in this publication:

* **Chen, Ying, et al. "A systematic benchmark of Nanopore long read RNA sequencing for transcript level analysis in human cell lines." bioRxiv (2021). doi: [https://doi.org/10.1101/2021.04.21.440736](https://doi.org/10.1101/2021.04.21.440736)**

m6Anet is described in the following manuscript:

* **Hendra, C., Pratanwanich, P.N., Wan, Y.K. et al. Detection of m6A from direct RNA sequencing using a multiple instance learning framework. Nat Methods 19, 1590–1598 (2022). [https://doi.org/10.1038/s41592-022-01666-1](https://doi.org/10.1038/s41592-022-01666-1)** 
