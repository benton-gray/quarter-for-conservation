import subprocess
def map_network():
  x = subprocess.check_output("arp -a".split())
  x = x.split('\n')
  ips = []
  for st in x:
    bg = st.find('192')
    ed = st.find(')', bg)
    if st != '':
      ips.append(st[bg:ed])
  return ips
print map_network()
