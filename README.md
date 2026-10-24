# Auto-download-Superstars


# SurveyStars Auto Downloader - Setup Guide

Vere system lo ee tool ni run cheyyadaniki kindha steps follow avvandi:

### Prerequisites
* System lo **Google Chrome** browser install ayyi undali.

### Step-by-Step Setup

1. **Install Python:**
   * [python.org/downloads](https://www.python.org/downloads/) nundi latest Python download cheyyandi.
   * **Important:** Install chesetappudu kindha unde **"Add Python to PATH"** ane checkbox ni khachitamga **Tick (Select)** chesi, *Install Now* nokkandi.

2. **Install Selenium:**
   * Keyboard lo `Win + R` nokki, `cmd` ani type chesi Enter nokkandi.
   * Kindha command run cheyyandi:
     ```bash
     pip install selenium
     ```

3. **Configure Login Details:**
   * `download.py` file ni **Desktop** meeda copy cheyyandi.
   * File meeda Right-Click ichi Notepad lo open chesi, `USERNAME` mariyu `PASSWORD` daggara mee login details enter chesi save (`Ctrl + S`) cheyyandi.

4. **Run the Script:**
   * Command Prompt (`cmd`) open chesi ee command run cheyyandi:
     ```bash
     python Desktop\download.py
     ```

### Output
* Anni files automatic ga download ayyi, unzip & rename ayyi mee Desktop meeda **`SurveyStars_Downloads`** ane folder lo save avtayi.

