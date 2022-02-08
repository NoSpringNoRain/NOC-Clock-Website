import diagnosis
import subprocess
process = subprocess.Popen(['python3', 'diagnosis.py', 'clock.png'],
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
print(float(stdout[1:-2]))
print(stderr)