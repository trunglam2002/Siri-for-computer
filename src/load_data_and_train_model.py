import subprocess

# Thực thi file python thứ nhất
subprocess.run(["python", "load_data_and_train_model/02_load_data.py"])

# Thực thi file python thứ hai
subprocess.run(["python", "load_data_and_train_model/03_train_model.py"])
