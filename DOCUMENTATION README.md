# MySQL Data Retrieval

Please refer to the following files: `db/db_connect_nparallel.py` and `db/db_connect_parallel.py`. All testing actions utilize these two files. The purpose of the testing is to determine which performs better in terms of speed and efficiency.

## Background
In the pursuit of optimizing website performance for our final project in Python, we embark on a comprehensive testing strategy employing both parallel and non-parallel methodologies. Leveraging local MySQL and Flask as the foundational technologies, our objective is to assess and enhance the system's efficiency, speed, and overall responsiveness.

Parallel testing involves the simultaneous execution of multiple test cases, allowing us to uncover potential bottlenecks and identify areas for improvement in the system's parallel processing capabilities. By harnessing the power of parallelism, we aim to unlock greater computational resources and expedite the execution of tasks, ultimately leading to a more streamlined and responsive website.

In contrast, non-parallel testing serves as a baseline for comparison, representing the sequential execution of test cases. This approach helps us gauge the inherent performance of the system without the benefits of parallelization. By understanding the system's behavior in a non-parallel context, we can evaluate the impact and effectiveness of introducing parallel and distributed computing concepts.

Additionally, our exploration extends to the integration of distributed systems, as we delve into the realm of optimizing resource utilization across multiple nodes. This strategic approach aims to harness the collective processing power of a network of interconnected devices, promoting scalability and responsiveness in our website's final implementation.

Through this dual-pronged testing methodology, we endeavor to fine-tune our Python-based website, ensuring that it not only meets but exceeds performance expectations. The utilization of local MySQL and Flask, coupled with the incorporation of parallel and distributed computing principles, reflects our commitment to delivering a robust, efficient, and highly responsive web application for our final project.

---

### Testing Research
#### Parallel Use: ThredPoolExecutor

**Non Parallel**
- 0.0275 seconds (1st) ~2  data
- 0.0344 seconds (2nd) ~40 data
- 0.0415 seconds (3rd) ~143 data
- 0.0528 seconds (4th) ~302 data
- 0.1216 seconds (5th) ~938 data

**Double ID Non Parallel**
- 0.0300 seconds (1st) ~938 data
- 0.0257 seconds (2nd) ~938 data
- 0.0266 seconds (3rd) ~938 data
- 0.0275 seconds (4th) ~938 data

**Parallel**
- 0.0272 seconds (1st) ~2  data
- 0.0269 seconds (2nd) ~40 data
- 0.0295 seconds (3rd) ~143 data
- 0.0382 seconds (4th) ~302 data
- 0.0660 seconds (5th) ~938 data

**Double ID Parallel**
- 0.0505 seconds (1st) ~938 data
- 0.0296 seconds (2nd) ~938 data
- 0.1301 seconds (3rd) ~938 data

*Tested on: Visual Studio Code & MySQL via Ubuntu 23.04*

---

**Copyright © 2023 IKHSAN ASSIDIQIE. All rights reserved.**
Statement issued on December 13, 2023.