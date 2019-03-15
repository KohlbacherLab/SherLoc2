import os
from subprocess import PIPE, Popen

f = file("/var/www/html/cgi-bin/sl2config.py", "w")

if os.environ.get("SL_CONTACT_EMAIL") != None:
    f.write("contact_email = '" + os.environ.get("SL_CONTACT_EMAIL") + "'\n")
else:
    f.write("contact_email = 'abi-services@informatik.uni-tuebingen.de'\n")

if os.environ.get("SL_IMPRINT_URL") != None:
    f.write("imprint_url = '" + os.environ.get("SL_IMPRINT_URL") + "'\n")
else:
    f.write("imprint_url = 'https://abi.inf.uni-tuebingen.de/impressum'\n")

if os.environ.get("SL_GDPR_URL") != None:
    f.write("gdpr_url = '" + os.environ.get("SL_GDPR_URL") + "'\n")
else:
    f.write("gdpr_url = 'https://abi.inf.uni-tuebingen.de/datenschutzerklaerung'\n")

if os.path.isfile("/interproscan/interproscan.sh"):
    p = Popen("/interproscan/interproscan.sh -version", shell=True, stdout=PIPE, stderr=PIPE);
    stdout, stderr = p.communicate();

    f.write("ips_version = '" + stdout.split("\n")[0].strip() + "'\n")
    f.write("ips_build = '" + stdout.split("\n")[1].strip() + "'\n")
else:
    f.write("ips_version = ''\n")

f.close()
