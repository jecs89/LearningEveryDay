cd ~/
mkdir python_env
cd python_env
sudo apt-get install python-virtualenv
virtualenv env
source ./env/bin/activate
pip install -U numpy
pip install -U cython
sudo apt-get install libatlas-base-dev
sudo apt-get install gfortran
pip install -U scipy
pip install -U scikit-learn
pip install -U matplotlib
