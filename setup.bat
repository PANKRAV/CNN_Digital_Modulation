chdir %~dp0
git clone https://github.com/PANKRAV/CNN_Digital_Modulation.git
chdir CNN_Digital_Modulation
REM python -m pip.exe install venv
python -m venv ergasia --prompt vlakas-xristos
ergasia\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cmd /k