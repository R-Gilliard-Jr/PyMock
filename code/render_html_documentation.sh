# Upgrade pip
pip install -U pip
pip install .[development]

# Use make to render documentation
cd documentation
make html