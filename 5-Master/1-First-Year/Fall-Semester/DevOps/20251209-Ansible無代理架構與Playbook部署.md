# 🛡️ DEVOPS-01-ANSIBLE-AUTOMATION DevOps 自動化維運實務 Lesson 01：Ansible 無代理架構、Playbook 宣告式部署與 Docker 容器整合


> **課程主題**：Ansible 自動化組態管理、無代理架構（Agentless）、Playbook 語法、冪等性與容器化維運  
> **授課教授**：授課講師（系統架構授課教授）  
> **核心模組**：Ansible Architecture, Agentless SSH, Playbook YAML, Idempotency, Docker Deployment  
> **學習目標**：掌握 Ansible 基礎架構原理，理解宣告式語法與冪等性對大規模基礎架構維運（IaC）之關鍵價值  
> **關聯文件**：[📄 完整原話逐字稿 (2025-12-09-01-Ansible無代理架構與Playbook部署-proofread.md)](./2025-12-09-01-Ansible無代理架構與Playbook部署-proofread.md)

---

## 🏛️ Ansible 無代理 (Agentless) 自動化部署拓撲

```mermaid
flowchart TD
    ControlNode["Ansible 控制節點 (Control Node)<br/>安裝 Ansible, 存放 Inventory 與 Playbooks"]
    
    subgraph TargetHosts["受管節點叢集 (Managed Nodes / Target Hosts)"]
        Host1["Web Server 1<br/>(僅需 Python 與 SSH)"]
        Host2["Web Server 2<br/>(僅需 Python 與 SSH)"]
        Host3["Database Server<br/>(僅需 Python 與 SSH)"]
        DockerHost["Docker 容器主機<br/>(Container Runtime)"]
    end

    ControlNode -- "SSH (Port 22) / 宣告式 Playbook" --> Host1
    ControlNode -- "SSH (Port 22) / 宣告式 Playbook" --> Host2
    ControlNode -- "SSH (Port 22) / 宣告式 Playbook" --> Host3
    ControlNode -- "SSH (Port 22) / 宣告式 Playbook" --> DockerHost
```

---

## ⚙️ 冪等性 (Idempotency) 與宣告式狀態維護模型

```mermaid
flowchart LR
    Task["執行 Ansible Playbook 任務"]
    CheckState{"檢查目標主機目前狀態<br/>是否與 Playbook 定義一致?"}
    NoChange["狀態已符合 (OK)<br/>不做任何修改，系統保持原樣"]
    ApplyChange["狀態不符 (Changed)<br/>執行變更使其達到期望狀態"]

    Task --> CheckState
    CheckState -- "一致" --> NoChange
    CheckState -- "不一致" --> ApplyChange
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. Ansible 的四大核心技術特色
- **無代理架構 (Agentless)**：受管主機端完全不需要預先安裝專屬 Agent 或啟動背景守護程式（Daemon），僅需標準 OpenSSH 服務與 Python 直譯器即可受控。
- **宣告式 Playbook (YAML)**：以清晰結構化之 YAML 檔案描述基礎架構的「最終期望狀態（Desired State）」，而非傳統指令碼的程序式指令（Imperative Commands）。
- **冪等性 (Idempotency)**：重複執行相同的 Playbook 任意多次，系統狀態將始終保持一致且不會造成副作用或重複安裝錯誤。
- **豐富模組生態**：內建包含套件管理（apt/yum）、檔案模板（template/jinja2）、服務管理（systemd）、Docker/Kubernetes 等數千種官方模組。

### 2. 容器化環境與 Inventory 動態管理
- **Docker 整合**：透過 Ansible Docker 模組實現容器映像檔自動建置、環境變數注入與叢集服務編排。
- **AI 輔助維運指令碼生成評估**：小組專題探討利用本地大型語言模型生成自動化維運 YAML 指令碼，但需嚴防模型「幻覺（Hallucination）」所造成的無效指令或資安組態漏洞。
