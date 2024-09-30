# paddlehelix
PaddleHelix平台API客户端

# HF3 OpenAPI

## 1. 准备工作

- 获取生成接口鉴权信息所需的访问密钥ID(AK)及秘密访问密钥(SK)，参考：[如何获取AKSK](https://cloud.baidu.com/doc/Reference/s/9jwvz2egb)﻿

- 开通 CHPC 服务：[开通页](https://console.bce.baidu.com/chpc/#/landing)﻿

## 2. 数据说明

```
{
  "name": "Protein-RNA-Ion: PDB 8AW3",           # string | 任务名，如未指定，则系统自动生成
  "recycle": 4,                                      # 可选，int | 范围[1,100]。模型推理参数，影响模型效果，越大越好。如果用户不设置，默认设为4。
	"ensemble": 1,                                     # 可选，int | 范围[1,100]。模型推理参数，影响模型效果，越大越好。如果用户不设置，默认设为1。
  "entities": [                                      # list | 定义各种实体。支持的实体类型：“protein”，“dna”，“rna”，“ion”，“ligand”。注：每个任务中所有实体加起来总token数量不能超过2000，不同实体的token计算方式见下方注释或参见HelixFold3 FAQ部分。
    {
      "type": "protein",                             # string | 实体类型（此处以蛋白为例）
      "sequence": "GPDSMEEVVVPEEPPKLVSALATYVQQERLCTMFLSIANKLLPLKP",    # string | 蛋白序列，仅支持20种标准氨基酸。一个氨基酸算做一个token，最大不可超过2000。
      "count": 1                                     # int | 实体复制数量
    },
    {
      "type": "ion",                                 # string | 实体类型（此处以离子为例）
      "ccd": "ZN",                                   # string | 离子的CCD标准名字。目前支持的离子列表请参考下一个代码块“离子CCD列表”。一个离子算作一个token。
      "count": 2                                     # int | 实体复制数量。实体为离子时，数量不可超过50。
    },
    {
      "type": "dna",                                 # string | 实体类型（此处以DNA为例）
      "sequence": "ACGTTTACGGGG",                    # string | DNA序列，仅支持4种标准脱氧核糖核酸ATCG。一个核苷酸算做一个token，最大不可超过2000。
      "count": 1                                     # int | 实体复制数量
    },
    {
      "type": "ligand",                              # string | 实体类型（此处以配体为例）
      "ccd": "ATP",                                  # string | 支持用户用CCD输入小分子配体，CCD和下方的SMILES只需输入其中一个即可。如果两个字段中都有输入，则以CCD的输入为准。配体中的一个原子算做一个token。注：水、助剂和少量特殊的配体目前是模型所不支持的，我们会将这些配体从CCD列表中除去，如果您通过输入SMILES的方式进行了这些输入，可能会造成结果的表现下降。具体不支持的配体的CCD列表参见[HelixFold3 FAQ]。
      "smiles": "CCccc(O)ccc",                       # string | 小分子的SMILES，重核数量需在50以内。SMILES和上方的CCD只需输入其中一个即可。如果两个字段中都有输入，则以CCD的输入为准。配体中的一个原子算做一个token。
      "count": 1                                     # int | 实体复制数量。实体为配体时，数量不可超过50。
    },
    {
      "type": "ion",                                 # 同上离子部分。
      "ccd": "ZN",
      "count": 1
    },
    {
      "type": "dna",                                 # 同上 dna 部分。
      "sequence": "CCCCGTAAACGT",
      "count": 1
    },
    {
      "type": "rna",                                 # string | 实体类型（此处以RNA为例）
      "sequence": "ACCCCCCC",                        # string | 序列，仅支持4种标准核糖核酸AUCG。一个核苷酸算做一个token，最大不可超过2000。
      "count": 1                                     # int | 实体复制数量。
    }
  ]
}
```

## 3. Open API

可参考或直接集成API客户端SDK，SDK使用见[PaddleHelix客户端](https://github.com/enginelong/paddlehelix)﻿

### 3.1 提交任务

#### 3.1.1 直接输入JSON数据

```python
from cli.client import APIClient

data = {
    "name": "7xwo_chain_F_22",
    "recycle": 4,
    "ensemble": 1,
    "entities": [
        {
            "type": "protein",
            "sequence": "HKTDSFVGLMA",
            "count": 2
        }
    ]
}
resp = APIClient.HelixFold3.submit(data)
print(f"code: {resp.code} msg: {resp.msg} taskID: {resp.data.task_id}")
# code: 0 msg:  taskID: 65676
```

#### 3.1.2 输入JSON文件路径

```python
from cli.client import APIClient

path = "xxx"
resp = APIClient.HelixFold3.submit(file_path=path)
print(f"code: {resp.code} msg: {resp.msg} taskID: {resp.data.task_id}")
# code: 0 msg:  taskID: 65677
```

### 3.2 批量提交任务

#### 3.2.1 直接输入JSON数据

```python
from cli.client import APIClient

data = [
    {
        "name": "7xwo_chain_F_22",
        "entities": [
            {
                "type": "protein",
                "sequence": "HKTDSFVGLMA",
                "count": 2
            }
        ]
    },
    {
        "name": "7xwo_chain_F_23",
        "entities": [
            {
                "type": "protein",
                "sequence": "HKTDSFVGLMA",
                "count": 4
            }
        ]
    }
]
resp = APIClient.HelixFold3.batch_submit(data)
for r in resp:
    print(f"code: {r.code} msg: {r.msg} taskID: {r.data.task_id}")
# code: 0 msg:  taskID: 65679
# code: 0 msg:  taskID: 65680
```

#### 3.2.2 输入JSON数据列表文件路径

```python
from cli.client import APIClient

path = "xxx"
resp = APIClient.HelixFold3.batch_submit(file_path=path)
for r in resp:
    print(f"code: {r.code} msg: {r.msg} taskID: {r.data.task_id}")
# code: 0 msg:  taskID: 65683
# code: 0 msg:  taskID: 65684
```

#### 3.2.3 输入文件目录（目录下包含多个3.1.2中的文件）

```python
from cli.client import APIClient

path = "xxx"
resp = APIClient.HelixFold3.batch_submit(file_dir=path)
for r in resp:
    print(f"code: {r.code} msg: {r.msg} taskID: {r.data.task_id}")
# code: 0 msg:  taskID: 65685
# code: 0 msg:  taskID: 65686
```

### 3.3 查询任务执行结果

```python
from cli.client import APIClient

task_id = 123
resp = APIClient.Common.query_task_info(task_id)
print(f"code: {resp.code} msg: {resp.msg} result: {resp.data.result}")
# code: 0 msg:  result: {"download_url":"", "file_url": "", "log_path":""}
```

### 3.4 批量查询任务执行结果

```python
from cli.client import APIClient

task_ids = [123, 124, 125]
resp = APIClient.Common.query_task_infos(task_ids)
for r in resp:
    print(f"code: {r.code} msg: {r.msg} result: {r.data.result}")
# code: 0 msg:  result: {"download_url":"", "file_url": "", "log_path":""}
# code: 0 msg:  result: {"download_url":"", "file_url": "", "log_path":""}
# code: 0 msg:  result: {"download_url":"", "file_url": "", "log_path":""}
```

### 3.5 取消任务

```python
from cli.client import APIClient

task_id = 65106
APIClient.Common.cancel_task(task_id)
```

### 3.6 批量取消任务

```python
from cli.client import APIClient

task_ids = [65106, 65107, 65108]
APIClient.Common.cancel_task(task_ids)
```

### 3.7 下载任务结果

```python
```

### 3.8 批量下载任务结果

```python
```





